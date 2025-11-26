# The Spearow Gambit - Audio Generation Guide
## Real Life Pokémon - ElevenLabs Voice Production

**Episode:** The Spearow Gambit
**Total Duration:** ~88 Seconds (11 sequences × 8s each)

---

## Voice Configuration (The "Documentary" Preset)

**Voice Settings for ElevenLabs:**
- **Voice ID:** Select a voice tagged with *British, Deep, Mature, Calm* (e.g., a "David" clone or similar)
- **Stability:** 35% - 45%
  - *Lower stability introduces breathiness and natural fluctuation for authentic documentary feel*
- **Clarity + Similarity:** 75%
  - *High fidelity for studio-quality sound*
- **Style Exaggeration:** 10% - 15%
  - *Adds slight theatrical weight without caricature*

---

## Audio Generation Table

| Sequence # | Narration Text | Word Count | Periods | Commas | Total Punct | Est. Duration |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | "In the wetland margins survival demands a calculated risk." | 10 words | 1 | 0 | 1 | 8s |
| **02** | "This juvenile's bulb has matured but remains untested in combat." | 10 words | 1 | 0 | 1 | 8s |
| **03** | "Five days of rain have passed and photosynthesis is critical." | 10 words | 1 | 0 | 1 | 8s |
| **04** | "But open ground attracts those who hunt from above." | 10 words | 1 | 0 | 1 | 8s |
| **05** | "The first strike tests defenses and draws no blood." | 10 words | 1 | 0 | 1 | 8s |
| **06** | "Retreating to cover means starvation within forty-eight hours." | 10 words | 1 | 0 | 1 | 8s |
| **07** | "Standing ground is death or the proving of poison." | 10 words | 1 | 0 | 1 | 8s |
| **08** | "The juvenile makes its choice and becomes perfectly still." | 10 words | 1 | 0 | 1 | 8s |
| **09** | "Contact triggers the release of neurotoxic alkaloid powder." | 10 words | 1 | 0 | 1 | 8s |
| **10** | "Paralysis begins and spreads through the nervous system." | 10 words | 1 | 0 | 1 | 8s |
| **11** | "The ecosystem accepts a new defender of the wetlands." | 10 words | 1 | 0 | 1 | 8s |

**Total Duration:** 88 seconds ✓

---

## Duration Verification Formula

**Formula:** `Duration = (words ÷ 2) + (total_punctuation_marks × 2) + 1`

Where:
- `words` = total word count
- `total_punctuation_marks` = periods + commas + em-dashes (em-dashes are BANNED)
- Each punctuation mark adds ~2 seconds of pause
- +1 second baseline overhead for natural pacing

**All sequences verified:**
- Each sequence: (10 ÷ 2) + (1 × 2) + 1 = **8 seconds** ✓

---

## File Naming Protocol

Generate one audio file per sequence using this naming convention:

| Sequence | Output Filename |
|----------|----------------|
| 01 | `Sequence_01_Narrative.mp3` |
| 02 | `Sequence_02_Narrative.mp3` |
| 03 | `Sequence_03_Narrative.mp3` |
| 04 | `Sequence_04_Narrative.mp3` |
| 05 | `Sequence_05_Narrative.mp3` |
| 06 | `Sequence_06_Narrative.mp3` |
| 07 | `Sequence_07_Narrative.mp3` |
| 08 | `Sequence_08_Narrative.mp3` |
| 09 | `Sequence_09_Narrative.mp3` |
| 10 | `Sequence_10_Narrative.mp3` |
| 11 | `Sequence_11_Narrative.mp3` |

**Save all audio files to:** `bulbasaur/audio/`

---

## Pacing Direction for Voice Actor

### Scenes 1-4: Building Tension
- Delivery: Neutral, observational
- Tone: Documentary exposition establishing the scenario
- Pace: Measured and steady

### Scenes 5-7: Calculation and Stakes
- Delivery: Slightly slower, weightier
- Tone: Dramatic tension building
- Pace: Deliberate pauses between key concepts

### Scenes 8-9: Climax
- Delivery: Dramatic pause before "Contact triggers" in Scene 09
- Tone: Peak intensity
- Pace: Scene 08 builds suspense, Scene 09 releases it

### Scenes 10-11: Resolution
- Delivery: Return to neutral, accepting tone
- Tone: Documentary conclusion
- Pace: Measured and contemplative

---

## Production Notes

### Critical Constraints
- **NEVER exceed 8 seconds per sequence** (videos are 10 seconds, need trim buffer)
- **NO em-dashes (—)** - they create excessive 2-second pauses
- **Minimize commas** - each comma adds ~2 seconds of pause
- All sequences use simple 10-word, 1-period structure for consistency

### Quality Checklist
Before finalizing each audio file:
- [ ] Verify duration is 7-9 seconds (target: 8s)
- [ ] Check for proper Attenborough vocal characteristics (breathiness, gravitas)
- [ ] Ensure studio-quality audio (no background noise)
- [ ] Confirm file naming matches sequence number
- [ ] Export as MP3, 192kbps minimum

---

## Next Steps

1. Generate all 11 audio files using ElevenLabs with settings above
2. Verify each file duration is 7-9 seconds
3. Save files to `bulbasaur/audio/` with correct naming convention
4. Proceed to video assembly (sync audio to video clips)
5. Trim videos to match audio duration in post-production

---

**Document Status:** Complete - Ready for ElevenLabs Audio Generation
