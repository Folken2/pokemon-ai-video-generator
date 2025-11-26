# Pokémon Natural Geographic - Asset Generator

Python CLI tool for generating photorealistic documentary assets using **Google Gemini 3 Pro Image** (Nano Banana Pro).

## Quick Start

### 1. Install Dependencies

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and create virtual environment
uv sync
```

### 2. Set Up API Key

1. Get your Gemini API key from: https://aistudio.google.com/app/apikey
2. Create a `.env` file in the `scripts/` directory:

```bash
cp .env.example .env
```

3. Edit `.env` and add your API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Generate Assets

#### Option A: Using the Agent (Recommended)

The easiest way is to use Claude Code with the agent instructions:

1. Open `prompts/3.5_generate_assets_agent.md` in Claude Code
2. Tell Claude: "Generate assets for pikachu"
3. The agent will automatically generate all 22 assets

#### Option B: Manual CLI Usage

Generate a single asset manually:

```bash
python generate_asset.py \
  --prompt "A hyper-realistic juvenile Pikachu in walking stance..." \
  --output "pikachu/assets/characters/pikachu_juvenile_walking.png" \
  --pokemon-path "pikachu"
```

## CLI Reference

### Command Structure

```bash
python generate_asset.py --prompt "COMPLETE_PROMPT" --output "path/to/output.png"
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--prompt` | ✅ | **COMPLETE** asset generation prompt (must already include Global Atmosphere Block prepended by calling agent) |
| `--output` | ✅ | Output file path relative to project root |

### Example Usage

**Important:** The prompt must be the FULL combined prompt (Global Atmosphere + Asset Description). The agent is responsible for combining these.

```bash
# Generate a character asset (prompt already combined by agent)
python generate_asset.py \
  --prompt "Early morning dawn light in temperate mixed forest, 15 minutes post-rainfall. Thick volumetric fog...

A hyper-realistic juvenile Pikachu in crouch position..." \
  --output "pikachu/assets/characters/pikachu_juvenile_crouch.png"
```

## How It Works

### Architecture

The Python script is a **simple CLI wrapper** around the Gemini API:
- Takes a complete prompt (pre-combined by the intelligent agent)
- Calls Gemini 2.5 Flash Image API
- Saves the generated image

**The agent does the smart work:**
- Reads `03_assets.md`
- Extracts Global Atmosphere Block
- Extracts individual asset prompts
- Combines them properly
- Calls this script with complete prompts

### API Call Flow

```
Agent reads 03_assets.md
    ↓
Agent extracts Global Atmosphere + Asset Prompts
    ↓
Agent combines: {atmosphere}\n\n{asset_prompt}
    ↓
Agent calls Python script with COMPLETE prompt
    ↓
Python script calls Gemini API
    ↓
Receive base64 image data
    ↓
Convert to PNG
    ↓
Save to specified output path
```

### Model Used

- **Model:** `gemini-2.5-flash-image` (Nano Banana)
- **Output Format:** PNG (highest quality, no compression artifacts)
- **Default size:** 1024x1024

## Directory Structure

After generation, your assets will be organized like this:

```
{pokemon_name}/
  assets/
    characters/
      pikachu_juvenile_walking.png
      pikachu_elder_defensive.png
      fearow_gliding.png
      ...
    props/
      beetles_living.png
      charred_beetles.png
      decaying_log.png
    environments/
      forest_dawn_mist.png
      smoking_crater.png
      electrical_flash.png
      ...
```

## Troubleshooting

### Error: `GEMINI_API_KEY not found`

**Solution:** Create a `.env` file in the `scripts/` directory with your API key:

```bash
cd scripts/
cp .env.example .env
# Edit .env and add your API key
```

### Error: `No image data in API response`

**Possible causes:**
- API rate limit reached (wait a few minutes)
- Prompt triggered content safety filters (review prompt)
- API service temporarily unavailable (retry later)

### Error: `ModuleNotFoundError: No module named 'google.genai'`

**Solution:** Install dependencies:

```bash
uv sync
```

## API Costs & Rate Limits

**Gemini 3 Pro Image (Nano Banana Pro):**
- Currently in paid preview
- Check latest pricing: https://ai.google.dev/pricing
- Typical asset generation: ~5-15 seconds per image
- Recommended batch size: 5-10 assets at a time to avoid rate limits

## Best Practices

### For Batch Generation

1. **Start small:** Generate 3-5 test assets first to verify quality
2. **Check atmosphere block:** Ensure Global Atmosphere Block matches your vision
3. **Monitor costs:** Track API usage for budget planning
4. **Save prompts:** The script logs all prompts for reproducibility

### For Quality Control

1. **Visual inspection:** Review each generated asset
2. **Consistency check:** Verify lighting and atmosphere match across assets
3. **Regeneration:** If an asset doesn't meet quality standards, regenerate with adjusted prompt
4. **Versioning:** Keep original prompts in `03_assets.md` for future reference

## Integration with Production Pipeline

This tool is **Step 3** in the production pipeline:

1. **SOP 01:** Species Research → `01_research.md`
2. **SOP 02:** Story Development → `02_story_script.md`
3. **SOP 03:** Asset Generation → `03_assets.md` + **THIS SCRIPT**
4. **SOP 04:** Kling AI Video Prompts → `04_kling_prompts.md`
5. **SOP 05:** ElevenLabs Audio → `05_audio_generation.md`

## Support

For issues or questions:
- Check the troubleshooting section above
- Review `prompts/3_character_generation.md` for prompt best practices
- Verify your Gemini API key is valid and has quota remaining

---

**Built for:** Real Life Pokémon - Nature Documentary Series
**Model:** Google Gemini 3 Pro Image (Nano Banana Pro)
**License:** Project-specific usage
