"""
Telegram Bot service for mobile pipeline approvals and notifications.
Optional — only active when TELEGRAM_ENABLED=true and bot token is configured.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from backend.config import (
    PROJECT_ROOT,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)
from backend.models import AVAILABLE_THEMES, STEP_DISPLAY_NAMES, StepName, StepStatus

if TYPE_CHECKING:
    from backend.pipeline.orchestrator import PipelineOrchestrator

# python-telegram-bot is an optional dependency — import lazily
try:
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
    from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
    _HAS_TELEGRAM = True
except ImportError:
    _HAS_TELEGRAM = False

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Sends pipeline notifications and handles approval callbacks via Telegram."""

    def __init__(self):
        self.app: Application | None = None
        self._chat_id = TELEGRAM_CHAT_ID

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def start(self):
        """Build the bot application and start polling."""
        if not _HAS_TELEGRAM:
            raise RuntimeError(
                "python-telegram-bot not installed. Install with: uv pip install 'pokemon-natural-geo[telegram]'"
            )
        self.app = (
            Application.builder()
            .token(TELEGRAM_BOT_TOKEN)
            .build()
        )

        # Commands
        self.app.add_handler(CommandHandler("status", self._cmd_status))
        self.app.add_handler(CommandHandler("projects", self._cmd_projects))
        self.app.add_handler(CommandHandler("new", self._cmd_new))

        # Inline button callbacks
        self.app.add_handler(CallbackQueryHandler(self._callback_handler))

        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling(drop_pending_updates=True)
        logger.info("Telegram bot started")

    async def stop(self):
        """Gracefully stop the bot."""
        if self.app:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
            logger.info("Telegram bot stopped")

    # ------------------------------------------------------------------
    # Notifications (called from pipeline)
    # ------------------------------------------------------------------

    async def notify_step_complete(
        self,
        subject_name: str,
        step_name: StepName,
        status: StepStatus,
        preview_text: str = "",
    ):
        """Send a notification when a step finishes, with approve/reject buttons."""
        if not self.app:
            return

        display = STEP_DISPLAY_NAMES.get(step_name, step_name.value)
        status_emoji = {
            StepStatus.AWAITING_APPROVAL: "🔔",
            StepStatus.FAILED: "❌",
            StepStatus.APPROVED: "✅",
        }.get(status, "ℹ️")

        text = f"{status_emoji} *{subject_name}* — {display}\nStatus: `{status.value}`"
        if preview_text:
            text += f"\n\n{preview_text[:500]}"

        keyboard = None
        if status == StepStatus.AWAITING_APPROVAL:
            # Story options get per-option buttons
            if step_name == StepName.STORY_OPTIONS:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton(f"Story {i}", callback_data=f"story:{subject_name}:{i}") for i in range(1, 4)],
                    [InlineKeyboardButton(f"Story {i}", callback_data=f"story:{subject_name}:{i}") for i in range(4, 6)],
                ])
            else:
                keyboard = InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ Approve", callback_data=f"approve:{subject_name}:{step_name.value}"),
                    InlineKeyboardButton("🔄 Retry", callback_data=f"retry:{subject_name}:{step_name.value}"),
                ]])

        await self.app.bot.send_message(
            chat_id=self._chat_id,
            text=text,
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

    async def send_image_preview(self, subject_name: str, image_paths: list[str]):
        """Send a media group of generated asset images."""
        if not self.app or not image_paths:
            return

        project_dir = PROJECT_ROOT / subject_name.lower()
        media = []
        for rel_path in image_paths[:10]:  # Telegram max 10 per group
            full = project_dir / rel_path
            if full.exists() and full.suffix.lower() in (".png", ".jpg", ".jpeg"):
                media.append(InputMediaPhoto(media=full.open("rb")))

        if media:
            await self.app.bot.send_media_group(chat_id=self._chat_id, media=media)

    async def send_audio_preview(self, subject_name: str, audio_path: str):
        """Send an audio file for review."""
        if not self.app:
            return
        full = PROJECT_ROOT / subject_name.lower() / audio_path
        if full.exists():
            await self.app.bot.send_audio(chat_id=self._chat_id, audio=full.open("rb"))

    async def notify_progress(self, subject_name: str, step_name: StepName, message: str):
        """Send a lightweight progress update."""
        if not self.app:
            return
        display = STEP_DISPLAY_NAMES.get(step_name, step_name.value)
        await self.app.bot.send_message(
            chat_id=self._chat_id,
            text=f"⏳ *{subject_name}* — {display}\n{message}",
            parse_mode="Markdown",
        )

    # ------------------------------------------------------------------
    # Command handlers
    # ------------------------------------------------------------------

    async def _cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status — show current pipeline status for all projects."""
        projects = self._list_projects()
        if not projects:
            await update.message.reply_text("No projects found.")
            return

        lines = ["*Pipeline Status*\n"]
        for p in projects:
            step_display = STEP_DISPLAY_NAMES.get(
                StepName(p["current_step"]) if isinstance(p["current_step"], str) else p["current_step"],
                str(p["current_step"]),
            )
            lines.append(f"• *{p['subject_name']}* [{p['theme']}] — {step_display} ({p['progress']})")

        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

    async def _cmd_projects(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /projects — list all projects with quick-action buttons."""
        projects = self._list_projects()
        if not projects:
            await update.message.reply_text("No projects. Use /new <subject> <theme> to create one.")
            return

        text = "*Projects*\n" + "\n".join(
            f"• {p['subject_name']} [{p['theme']}] ({p['progress']})" for p in projects
        )
        await update.message.reply_text(text, parse_mode="Markdown")

    async def _cmd_new(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /new <subject> [theme] — create a new project."""
        args = context.args or []
        if not args:
            await update.message.reply_text(
                "Usage: `/new <subject_name> [theme]`\n"
                f"Themes: {', '.join(AVAILABLE_THEMES)}",
                parse_mode="Markdown",
            )
            return

        subject = args[0].lower().strip()
        theme = args[1].lower().strip() if len(args) > 1 else "pokemon"

        if theme not in AVAILABLE_THEMES:
            await update.message.reply_text(f"Invalid theme. Choose from: {', '.join(AVAILABLE_THEMES)}")
            return

        from backend.pipeline.orchestrator import PipelineOrchestrator
        orchestrator = PipelineOrchestrator(subject, theme=theme)
        state = orchestrator.get_state()
        await update.message.reply_text(
            f"✅ Created *{state.subject_name}* ({state.theme})",
            parse_mode="Markdown",
        )

    # ------------------------------------------------------------------
    # Callback handler (inline button presses)
    # ------------------------------------------------------------------

    async def _callback_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Route inline button callbacks."""
        query = update.callback_query
        await query.answer()

        data = query.data
        parts = data.split(":")

        if parts[0] == "approve" and len(parts) == 3:
            _, subject, step_val = parts
            await self._do_approve(query, subject, step_val)

        elif parts[0] == "retry" and len(parts) == 3:
            _, subject, step_val = parts
            await self._do_retry(query, subject, step_val)

        elif parts[0] == "story" and len(parts) == 3:
            _, subject, option = parts
            await self._do_story_select(query, subject, int(option))

    async def _do_approve(self, query, subject_name: str, step_value: str):
        """Approve a step via Telegram."""
        from backend.models import ApproveStepRequest
        from backend.pipeline.orchestrator import PipelineOrchestrator

        step = StepName(step_value)
        orchestrator = PipelineOrchestrator(subject_name)
        result = orchestrator.approve_step(ApproveStepRequest(step=step))
        emoji = "✅" if result else "❌"
        display = STEP_DISPLAY_NAMES.get(step, step_value)
        await query.edit_message_text(f"{emoji} *{subject_name}* — {display} approved", parse_mode="Markdown")

    async def _do_retry(self, query, subject_name: str, step_value: str):
        """Retry a step via Telegram."""
        from backend.pipeline.orchestrator import PipelineOrchestrator

        step = StepName(step_value)
        orchestrator = PipelineOrchestrator(subject_name)
        orchestrator.retry_step(step)
        display = STEP_DISPLAY_NAMES.get(step, step_value)
        await query.edit_message_text(f"🔄 *{subject_name}* — {display} retrying...", parse_mode="Markdown")

    async def _do_story_select(self, query, subject_name: str, option: int):
        """Select a story option via Telegram."""
        from backend.models import ApproveStepRequest
        from backend.pipeline.orchestrator import PipelineOrchestrator

        orchestrator = PipelineOrchestrator(subject_name)
        result = orchestrator.approve_step(
            ApproveStepRequest(step=StepName.STORY_OPTIONS, selected_option=option)
        )
        emoji = "✅" if result else "❌"
        await query.edit_message_text(
            f"{emoji} *{subject_name}* — Story option {option} selected",
            parse_mode="Markdown",
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _list_projects() -> list[dict]:
        """List projects from disk (same logic as projects router)."""
        from backend.models import PipelineState

        projects = []
        for path in sorted(PROJECT_ROOT.iterdir()):
            state_file = path / "pipeline_state.json"
            if path.is_dir() and state_file.exists():
                try:
                    state = PipelineState.load(path)
                    if state:
                        total = len(state.steps)
                        completed = sum(
                            1 for s in state.steps.values()
                            if s.status in (StepStatus.APPROVED, StepStatus.SKIPPED)
                        )
                        projects.append({
                            "subject_name": state.subject_name,
                            "theme": state.theme,
                            "current_step": state.current_step,
                            "progress": f"{completed}/{total}",
                        })
                except Exception:
                    continue
        return projects


# ------------------------------------------------------------------
# Singleton
# ------------------------------------------------------------------

_notifier: TelegramNotifier | None = None


def get_telegram_notifier() -> TelegramNotifier | None:
    """Get the global notifier instance (None if not enabled)."""
    return _notifier


def set_telegram_notifier(notifier: TelegramNotifier):
    """Set the global notifier instance (called from app startup)."""
    global _notifier
    _notifier = notifier


async def fire_telegram_notification(
    subject_name: str,
    step_name: StepName,
    status: StepStatus,
    preview_text: str = "",
):
    """Fire-and-forget notification helper safe to call from any context."""
    notifier = get_telegram_notifier()
    if not notifier:
        return
    try:
        await notifier.notify_step_complete(subject_name, step_name, status, preview_text)
    except Exception as e:
        logger.warning(f"Telegram notification failed: {e}")
