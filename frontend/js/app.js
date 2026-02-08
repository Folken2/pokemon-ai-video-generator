/**
 * Main Application Logic for Pokemon Documentary Pipeline
 */

// --- State ---
let currentProject = null;
let currentStep = null;
let pollInterval = null;

// Step definitions with display info
const STEPS = [
    { name: 'research', label: 'Species Research', phase: 'Pre-Production' },
    { name: 'story_options', label: 'Story Options', phase: 'Pre-Production' },
    { name: 'story_script', label: 'Production Script', phase: 'Pre-Production' },
    { name: 'asset_planning', label: 'Asset Planning', phase: 'Art Direction' },
    { name: 'asset_generation', label: 'Asset Generation', phase: 'Art Direction' },
    { name: 'composite_generation', label: 'Composites', phase: 'Art Direction' },
    { name: 'video_prompts', label: 'Video Prompts', phase: 'Video Production' },
    { name: 'video_generation', label: 'Video Generation', phase: 'Video Production' },
    { name: 'audio_prompts', label: 'Narration Prompts', phase: 'Audio Production' },
    { name: 'audio_generation', label: 'Narration Audio', phase: 'Audio Production' },
    { name: 'sfx_prompts', label: 'SFX Prompts', phase: 'Audio Production' },
    { name: 'sfx_generation', label: 'SFX Generation', phase: 'Audio Production' },
    { name: 'final_assembly', label: 'Final Assembly', phase: 'Post-Production' },
];

const STATUS_CLASSES = {
    pending: 'badge-pending',
    running: 'badge-running',
    awaiting_approval: 'badge-awaiting',
    approved: 'badge-approved',
    failed: 'badge-failed',
    skipped: 'badge-pending',
};

const STATUS_LABELS = {
    pending: 'Pending',
    running: 'Running...',
    awaiting_approval: 'Review',
    approved: 'Done',
    failed: 'Failed',
    skipped: 'Skipped',
};

const STATUS_ICONS = {
    pending: '',
    running: '&#9654;',
    awaiting_approval: '!',
    approved: '&#10003;',
    failed: '&#10007;',
    skipped: '-',
};

// --- Initialization ---
document.addEventListener('DOMContentLoaded', async () => {
    await checkApiStatus();
    await loadProjects();

    // Handle project selection
    document.getElementById('project-select').addEventListener('change', (e) => {
        if (e.target.value) {
            loadProject(e.target.value);
        }
    });

    // Enter key on pokemon name input
    document.getElementById('pokemon-name-input').addEventListener('keydown', (e) => {
        if (e.key === 'Enter') createProject();
    });
});

async function checkApiStatus() {
    try {
        const health = await api.checkHealth();
        const el = document.getElementById('api-status');
        const configured = Object.values(health.api_keys).filter(v => v).length;
        const total = Object.keys(health.api_keys).length;

        if (configured === total) {
            el.textContent = `All APIs Connected`;
            el.className = 'text-xs px-2 py-1 rounded-full bg-green-900 text-green-300';
        } else {
            el.textContent = `${configured}/${total} APIs`;
            el.className = 'text-xs px-2 py-1 rounded-full bg-yellow-900 text-yellow-300';
        }
    } catch (e) {
        const el = document.getElementById('api-status');
        el.textContent = 'Server Error';
        el.className = 'text-xs px-2 py-1 rounded-full bg-red-900 text-red-300';
    }
}

async function loadProjects() {
    try {
        const projects = await api.listProjects();
        const select = document.getElementById('project-select');
        // Clear existing options except first
        select.innerHTML = '<option value="">Select Project...</option>';
        projects.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p.pokemon_name;
            opt.textContent = `${p.pokemon_name} (${p.progress})`;
            select.appendChild(opt);
        });

        // Show existing projects on welcome screen
        const container = document.getElementById('existing-projects');
        if (projects.length > 0) {
            container.innerHTML = `
                <p class="text-gray-500 text-sm mb-3">Or continue an existing project:</p>
                <div class="flex flex-wrap gap-2 justify-center">
                    ${projects.map(p => `
                        <button onclick="loadProject('${p.pokemon_name}')"
                                class="bg-gray-800 hover:bg-gray-700 border border-gray-700 px-4 py-2 rounded-lg text-sm">
                            ${p.pokemon_name} <span class="text-gray-500">(${p.progress})</span>
                        </button>
                    `).join('')}
                </div>
            `;
        }
    } catch (e) {
        console.error('Failed to load projects:', e);
    }
}

// --- Project Management ---
function showNewProjectModal() {
    document.getElementById('new-project-modal').style.display = 'flex';
    document.getElementById('pokemon-name-input').focus();
}

function hideNewProjectModal() {
    document.getElementById('new-project-modal').style.display = 'none';
}

async function createProject() {
    const name = document.getElementById('pokemon-name-input').value.trim();
    if (!name) return;

    try {
        await api.createProject(name);
        hideNewProjectModal();
        await loadProjects();
        await loadProject(name);
    } catch (e) {
        alert('Failed to create project: ' + e.message);
    }
}

async function loadProject(pokemonName) {
    currentProject = pokemonName;
    document.getElementById('project-select').value = pokemonName;
    document.getElementById('welcome-screen').style.display = 'none';
    document.getElementById('main-content').style.display = 'flex';

    await refreshPipeline();
}

// --- Pipeline UI ---
async function refreshPipeline() {
    if (!currentProject) return;

    try {
        const status = await api.getPipelineStatus(currentProject);
        renderStepList(status);

        if (currentStep) {
            await loadStepDetail(currentStep);
        }
    } catch (e) {
        console.error('Failed to refresh pipeline:', e);
    }
}

function renderStepList(status) {
    const container = document.getElementById('step-list');
    let html = '';
    let lastPhase = '';

    STEPS.forEach((step, index) => {
        const stepData = status.steps[step.name] || {};
        const stepStatus = stepData.status || 'pending';

        // Phase header
        if (step.phase !== lastPhase) {
            lastPhase = step.phase;
            html += `<div class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider ${index > 0 ? 'mt-2 border-t border-gray-800 pt-3' : ''}">${step.phase}</div>`;
        }

        const statusClass = stepStatus === 'approved' ? 'completed' :
                           stepStatus === 'running' ? 'running' :
                           stepStatus === 'awaiting_approval' ? 'awaiting' :
                           stepStatus === 'failed' ? 'failed' : '';
        const activeClass = currentStep === step.name ? 'active' : '';

        html += `
            <div class="step-item ${statusClass} ${activeClass}" onclick="selectStep('${step.name}')">
                <div class="step-icon">${STATUS_ICONS[stepStatus] || (index + 1)}</div>
                <div class="flex-1 min-w-0">
                    <div class="text-sm font-medium truncate">${step.label}</div>
                    <div class="text-xs text-gray-500">${STATUS_LABELS[stepStatus] || stepStatus}</div>
                </div>
                ${stepData.artifact_count > 0 ? `<span class="text-xs text-gray-500">${stepData.artifact_count}</span>` : ''}
            </div>
        `;
    });

    container.innerHTML = html;
}

async function selectStep(stepName) {
    currentStep = stepName;
    await refreshPipeline();
    await loadStepDetail(stepName);
}

async function loadStepDetail(stepName) {
    if (!currentProject) return;

    try {
        const detail = await api.getStepDetail(currentProject, stepName);
        renderStepDetail(detail);
    } catch (e) {
        console.error('Failed to load step detail:', e);
    }
}

function renderStepDetail(detail) {
    // Title and status
    document.getElementById('step-title').textContent = detail.display_name;
    const badge = document.getElementById('step-status-badge');
    badge.textContent = STATUS_LABELS[detail.status] || detail.status;
    badge.className = `text-xs px-2 py-0.5 rounded-full ${STATUS_CLASSES[detail.status] || ''}`;

    // Action buttons
    const actions = document.getElementById('step-actions');
    actions.innerHTML = '';

    if (detail.status === 'pending' || detail.status === 'failed') {
        const runBtn = document.createElement('button');
        runBtn.textContent = detail.status === 'failed' ? 'Retry' : 'Run Step';
        runBtn.className = 'bg-blue-600 hover:bg-blue-700 px-4 py-1.5 rounded text-sm font-medium';
        runBtn.onclick = () => runCurrentStep();
        actions.appendChild(runBtn);
    }

    if (detail.status === 'awaiting_approval') {
        if (detail.name === 'story_options') {
            // Special: story selection
            const selectBtn = document.createElement('button');
            selectBtn.textContent = 'Select Story';
            selectBtn.className = 'bg-green-600 hover:bg-green-700 px-4 py-1.5 rounded text-sm font-medium';
            selectBtn.onclick = () => {
                document.getElementById('story-select-modal').style.display = 'flex';
            };
            actions.appendChild(selectBtn);
        } else {
            const approveBtn = document.createElement('button');
            approveBtn.textContent = 'Approve';
            approveBtn.className = 'bg-green-600 hover:bg-green-700 px-4 py-1.5 rounded text-sm font-medium';
            approveBtn.onclick = () => approveCurrentStep();
            actions.appendChild(approveBtn);
        }
    }

    // Output content
    const outputEl = document.getElementById('step-output');
    if (detail.output) {
        outputEl.innerHTML = `<div class="markdown-content">${renderMarkdown(detail.output)}</div>`;
    } else if (detail.status === 'pending') {
        outputEl.innerHTML = '<p class="text-gray-500">Step has not been run yet. Click "Run Step" to begin.</p>';
    } else if (detail.status === 'running') {
        outputEl.innerHTML = `
            <div class="flex items-center gap-3 text-blue-400">
                <div class="animate-spin w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full"></div>
                <span>Running... This may take a while depending on the step.</span>
            </div>
        `;
    } else if (detail.error) {
        outputEl.innerHTML = `<div class="bg-red-900/30 border border-red-800 rounded-lg p-4 text-red-300">${escapeHtml(detail.error)}</div>`;
    } else {
        outputEl.innerHTML = '<p class="text-gray-500">No output yet.</p>';
    }

    // Artifacts
    const artifactSection = document.getElementById('artifacts-section');
    const gallery = document.getElementById('artifacts-gallery');
    if (detail.artifacts && detail.artifacts.length > 0) {
        artifactSection.style.display = '';
        gallery.innerHTML = detail.artifacts.map(a => {
            const fileUrl = `/files/${currentProject}/${a.path}`;
            if (a.type === 'image') {
                return `
                    <div class="group">
                        <img src="${fileUrl}" alt="${a.path}" class="artifact-thumb w-full"
                             onclick="window.open('${fileUrl}', '_blank')">
                        <p class="text-xs text-gray-500 mt-1 truncate">${a.path.split('/').pop()}</p>
                    </div>
                `;
            } else if (a.type === 'audio') {
                return `
                    <div class="bg-gray-800 rounded-lg p-3">
                        <p class="text-xs text-gray-400 mb-2 truncate">${a.path.split('/').pop()}</p>
                        <audio controls class="w-full h-8" preload="none">
                            <source src="${fileUrl}" type="audio/mpeg">
                        </audio>
                    </div>
                `;
            } else if (a.type === 'video') {
                return `
                    <div class="group">
                        <video class="artifact-thumb w-full" controls preload="none">
                            <source src="${fileUrl}" type="video/mp4">
                        </video>
                        <p class="text-xs text-gray-500 mt-1 truncate">${a.path.split('/').pop()}</p>
                    </div>
                `;
            } else {
                return `
                    <div class="bg-gray-800 rounded-lg p-3">
                        <p class="text-xs text-gray-400 truncate">${a.path.split('/').pop()}</p>
                        <p class="text-xs text-gray-500">${formatBytes(a.size)}</p>
                    </div>
                `;
            }
        }).join('');
    } else {
        artifactSection.style.display = 'none';
    }

    // Logs
    const logsSection = document.getElementById('logs-section');
    const logsContainer = document.getElementById('logs-container');
    if (detail.logs && detail.logs.length > 0) {
        logsSection.style.display = '';
        logsContainer.innerHTML = detail.logs.map(l =>
            `<div class="text-gray-400 leading-relaxed">${escapeHtml(l)}</div>`
        ).join('');
        logsContainer.scrollTop = logsContainer.scrollHeight;
    } else {
        logsSection.style.display = 'none';
    }
}

// --- Actions ---
async function runCurrentStep() {
    if (!currentProject || !currentStep) return;

    showLoading(`Running ${currentStep}...`);

    try {
        const result = await api.runStep(currentProject, currentStep);
        hideLoading();
        await refreshPipeline();
        await loadStepDetail(currentStep);
    } catch (e) {
        hideLoading();
        alert('Step execution failed: ' + e.message);
    }
}

async function approveCurrentStep() {
    if (!currentProject || !currentStep) return;

    try {
        const result = await api.approveStep(currentProject, currentStep);
        await refreshPipeline();

        // Auto-advance to next step
        if (result.next_step) {
            currentStep = result.next_step;
        }
        await refreshPipeline();
        if (currentStep) {
            await loadStepDetail(currentStep);
        }
    } catch (e) {
        alert('Approval failed: ' + e.message);
    }
}

async function approveStorySelection() {
    if (!currentProject) return;

    const option = parseInt(document.getElementById('story-option-input').value);
    const feedback = document.getElementById('story-feedback-input').value;

    if (option < 1 || option > 5) {
        alert('Please select option 1-5');
        return;
    }

    document.getElementById('story-select-modal').style.display = 'none';
    showLoading('Approving story selection...');

    try {
        await api.approveStep(currentProject, 'story_options', feedback, option);
        hideLoading();
        await refreshPipeline();
        // Move to story_script step
        currentStep = 'story_script';
        await loadStepDetail(currentStep);
    } catch (e) {
        hideLoading();
        alert('Story selection failed: ' + e.message);
    }
}

// --- Helpers ---
function showLoading(text) {
    document.getElementById('loading-text').textContent = text;
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

function renderMarkdown(text) {
    try {
        return marked.parse(text);
    } catch (e) {
        return `<pre>${escapeHtml(text)}</pre>`;
    }
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}
