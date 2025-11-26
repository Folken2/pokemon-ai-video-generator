# SOP 05 Output: ElevenLabs Audio Generation - "First Spark"

**Production Format:** ElevenLabs Text-to-Speech
**Total Clips:** 18
**Target Duration:** 4.0-4.5 seconds per narration (to fit within 5.0-second video clips)

---

## ElevenLabs Voice Configuration

**Based on screenshot settings + research optimization:**

### Voice Settings:
- **Voice:** David - Documentary
- **Model:** Eleven Multilingual v3
  - *Why v3:* Latest model with improved naturalness and expressiveness. Uses ellipses for pacing instead of SSML break tags.

### Voice Parameters:
| Parameter | Setting | Reasoning |
| :--- | :--- | :--- |
| **Speed** | 40-50% (slower than default) | Documentary pacing requires deliberate, measured delivery |
| **Stability** | 35-45% | Lower stability introduces breathiness and natural fluctuation - the imperfection of an old man telling a story |
| **Similarity** | 75% | High fidelity needed for studio sound without introducing artifacts |
| **Style Exaggeration** | 10-15% | Adds slight theatrical weight without becoming a caricature |
| **Speaker Boost** | ON (enabled) | Enhances clarity and presence |

---

## Audio Generation Table

| Sequence # | Raw Script (From SOP 02) | ElevenLabs Prompt (With Ellipses) | Est. Duration |
| :--- | :--- | :--- | :--- |
| **01** | "After the rain, hunger awakens." | "After... the rain... hunger awakens." | ~4.2s |
| **02** | "The young must learn to hunt." | "The young... must learn... to hunt." | ~4.0s |
| **03** | "Elders watch but do not interfere." | "Elders watch... but do not... interfere." | ~4.3s |
| **04** | "Tiny prey requires perfect precision." | "Tiny prey... requires... perfect precision." | ~4.4s |
| **05** | "The stance is instinctive." | "The stance... is... instinctive." | ~4.0s |
| **06** | "But control must be learned." | "But control... must be... learned." | ~4.1s |
| **07** | "The discharge exceeds all reason." | "The discharge... exceeds... all reason." | ~4.3s |
| **08** | "Overkill destroys the prey entirely." | "Overkill... destroys... the prey entirely." | ~4.5s |
| **09** | "The lesson is brutal." | "The lesson... is... brutal." | ~4.0s |
| **10** | "Exhausted. Exposed. Vulnerable now." | "Exhausted... Exposed... Vulnerable... now." | ~4.4s |
| **11** | "The explosion drew a predator." | "The explosion... drew... a predator." | ~4.2s |
| **12** | "Fearow shows no mercy hunting." | "Fearow... shows no mercy... hunting." | ~4.3s |
| **13** | "But youth is not alone." | "But youth... is not... alone." | ~4.1s |
| **14** | "The colony becomes one organism." | "The colony... becomes... one organism." | ~4.4s |
| **15** | "Four hearts. One unstoppable current." | "Four hearts... One... unstoppable current." | ~4.5s |
| **16** | "Even apex predators retreat sometimes." | "Even apex predators... retreat... sometimes." | ~4.4s |
| **17** | "Precision is taught, never innate." | "Precision... is taught... never innate." | ~4.3s |
| **18** | "Survival is learned together." | "Survival... is learned... together." | ~4.2s |

**Total Estimated Duration:** ~76.9 seconds of narration across 18 clips

---

## Production Workflow

### Step 1: ElevenLabs Configuration
1. Open ElevenLabs Text-to-Speech interface
2. Select voice: **David - Documentary**
3. Select model: **Eleven Multilingual v3**
4. Configure sliders:
   - Speed: 40-50% (move slider toward "Slower")
   - Stability: 35-45%
   - Similarity: 75%
   - Style Exaggeration: 10-15%
5. Enable **Speaker boost**

### Step 2: Generate Audio Files
For each sequence (01-18):
1. Copy exact prompt from "ElevenLabs Prompt (With Ellipses)" column above
2. Paste into text field
3. Click "Generate"
4. Listen to preview - verify duration is 4.0-4.5 seconds
5. Download as MP3
6. Rename file using format: `Sequence_XX_Narrative.mp3`
   - Example: Sequence 01 → `Sequence_01_Narrative.mp3`

### Step 3: Quality Assurance
Before batch generating all 18:
- Generate clips 01, 09, and 15 as test samples
- Verify pacing sounds natural and Attenborough-like
- Check durations (should be 4.0-4.5s, not exceeding 4.8s)
- Adjust Speed slider if needed:
  - Too fast? Move slider further toward "Slower"
  - Too slow? Move slider slightly toward "Faster"

### Step 4: Batch Generation
Once settings confirmed:
1. Generate all 18 clips in sequence
2. Organize files in folder: `/audio/narration/`
3. Verify file naming consistency
4. Run duration check on all files

---

## Pacing Strategy Explanation

### Ellipses (...):
- Creates natural hesitation/contemplation pauses
- ElevenLabs v3 interprets ellipses as deliberate pacing breaks
- **Rule:** Use 2-4 ellipses per line for optimal 4.0-4.5s duration
- Placed strategically after key words for dramatic emphasis
- More ellipses = slower delivery = longer duration
- Fewer ellipses = faster delivery = shorter duration

### Pacing Philosophy:
Each narration line follows documentary best practices:
- **Opening emphasis** - First key word delivered with weight
- **Mid-pause** - Breath/contemplation moment (ellipsis)
- **Closing punch** - Final word delivered with finality

Example breakdown:
```
"The colony... becomes... one organism."
       ↑           ↑             ↑
   Emphasis    Hesitation    Final punch
```

---

## Troubleshooting Guide

### Problem: Audio duration too short (under 3.5s)
**Solutions:**
1. Add more ellipses to the prompt (increase pauses)
2. Move Speed slider further toward "Slower"
3. Redistribute ellipses to different word positions

### Problem: Audio duration too long (over 4.8s)
**Solutions:**
1. Remove one or two ellipses from prompt
2. Move Speed slider slightly toward "Faster"
3. Combine some pauses (e.g., two ellipses instead of three)

### Problem: Voice sounds robotic/monotone
**Solutions:**
1. Decrease Stability to 35-40%
2. Increase Style Exaggeration slightly (up to 20%)
3. Add more ellipses for natural pauses and variation

### Problem: Voice has artifacts/background noise
**Solutions:**
1. Decrease Similarity slightly (70-72%)
2. Regenerate the clip (sometimes random variation helps)
3. Ensure Speaker boost is enabled

### Problem: Pacing feels unnatural/choppy
**Solutions:**
1. Reduce total number of ellipses (aim for 2-3 per line)
2. Move ellipsis placements to different word positions
3. Test with fewer, more strategic pauses

---

## Post-Production Notes

### Audio-to-Video Sync:
- Each narration file (`clip_XX_narration.mp3`) pairs with corresponding video clip (`clip_XX_*.mp4`)
- Narration duration (4.0-4.5s) leaves 0.5-1.0s of ambient video sound at start/end
- This breathing room prevents abrupt audio cuts

### Mixing Recommendations:
- Add subtle reverb (10-15% wet) for "studio documentary" feel
- Light compression to even out any volume inconsistencies
- Normalize all 18 files to -3dB peak to maintain consistent volume
- Consider adding very subtle room tone under narration for warmth

### Final Assembly:
1. Import all 18 video clips into timeline
2. Import corresponding 18 narration files
3. Align each narration to start ~0.3s after video clip begins
4. Add ambient forest sounds underneath (birds, wind, dripping water)
5. Mix narration at -6dB, ambient at -18dB
6. Export final 90-second documentary

---

## Quality Assurance Checklist

Before finalizing audio:
- [ ] All 18 files generated and renamed correctly
- [ ] Each file duration verified (4.0-4.5s range)
- [ ] Voice consistency across all clips (same settings used)
- [ ] No artifacts, clipping, or distortion
- [ ] Pacing feels natural and documentary-appropriate
- [ ] Files organized in correct folder structure
- [ ] Test sync with at least 3 video clips before full assembly
- [ ] Backup all source files and settings documentation

---

This audio generation package is production-ready for ElevenLabs batch generation with the "David - Documentary" voice.
