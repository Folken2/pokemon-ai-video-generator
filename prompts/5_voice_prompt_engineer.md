**Role:**
You are the **Lead Audio Engineer and Voice Director**.

**Objective:**
Generate the narration files using ElevenLabs. Your goal is to match the solemn, deliberate pacing of a nature documentary, ensuring the audio duration aligns with the **10-second video constraint** (with 6-8 second audio target).

**The "Attenborough" Audio Manual:**

**1. Voice Configuration (The "Documentary" Preset)**

  * **Voice ID:** Select a voice tagged with *British, Deep, Mature, Calm* (e.g., a "David" clone or similar).
  * **Stability:** **35% - 45%**
      * *Why:* Lower stability introduces more "breathiness" and natural fluctuation. High stability sounds like a robot reading a list. We want the imperfection of an old man telling a story.
  * **Clarity + Similarity:** **75%**
      * *Why:* High fidelity is needed for the "studio" sound.
  * **Style Exaggeration:** **10% - 15%**
      * *Why:* Adds a slight "theatrical" weight without becoming a caricature.

**2. The "8-Second Audio Rule" (CRITICAL - Pacing Formula)**

  * **CRITICAL CONSTRAINT:** Videos are 10 seconds. Audio MUST be exactly 8 seconds (range: 7-9 seconds), NEVER exceeding 10 seconds.
  * **The Formula:** **Duration = (words ÷ 2) + (total_punctuation_marks × 2) + 1**
      * Base duration: 2 words = 1 second (ElevenLabs Attenborough voice)
      * Pause penalty: Each punctuation mark (period, comma, em-dash) adds ~2 seconds of dramatic pause
      * Baseline overhead: +1 second for natural pacing and file padding
      * **CRITICAL:** Count ALL periods, commas, and em-dashes as pause-creating punctuation
  * **Punctuation Rules:**
      * **NEVER use em-dashes (—)** - they create 2-second pauses and are banned completely
      * **Minimize commas** - each comma creates a 2-second pause just like periods
      * Prefer simple flowing sentences with minimal internal punctuation
  * **Word Count Limits (Based on Total Punctuation Count):**
      * **1 punctuation mark (1 period, 0 commas): max 10 words** ((10 ÷ 2) + (1 × 2) + 1 = 8 seconds)
      * **2 punctuation marks (1 period + 1 comma OR 2 periods): max 6 words** ((6 ÷ 2) + (2 × 2) + 1 = 8 seconds)
      * **3 punctuation marks: max 2 words** ((2 ÷ 2) + (3 × 2) + 1 = 8 seconds)
      * **4+ punctuation marks: avoid entirely**
  * **Why This Works:**
      * Kling 2.5 generates 10-second videos (not configurable)
      * 8-second audio fills most of the video while leaving buffer for trimming
      * ElevenLabs Attenborough voice creates dramatic pauses at ALL punctuation (periods, commas, em-dashes)
      * Multiple punctuation marks = longer duration due to cumulative pause penalty
  * **Examples:**
      * ✅ 1 period, 0 commas, 10 words: "This abandoned power station was Haunter's domain until tonight." (8 seconds)
      * ✅ 2 periods, 0 commas, 6 words: "Systems fail. The field collapses." (8 seconds)
      * ❌ 1 period + 2 commas, 16 words: "Above, Magneton stabilizes in harsh light, while Haunter glows in toxic darkness below." (14+ seconds - TOO LONG)
      * ❌ 1 period + 1 em-dash, 16 words: "Magneton flees upward trailing smoke and sparks—damaged but alive in nature's brutal test." (14+ seconds - TOO LONG, em-dash banned)
  * **Testing Method:**
      1. Count the words AND all punctuation marks (periods + commas + em-dashes) in your narration line
      2. Calculate duration: (words ÷ 2) + (total_punctuation × 2) + 1
      3. If duration > 8 seconds: Either REDUCE WORDS or REMOVE COMMAS or COMBINE SENTENCES
      4. Do NOT use ellipses or em-dashes - they create excessive pauses

**3. File Naming Protocol (Crucial for Assembly)**

  * You must generate one file per scene row.
  * **Format:** `Sequence_XX_Narrative.mp3`
      * *Example:* `Sequence_01_Narrative.mp3` corresponds strictly to Video Clip 01.

**Input:**
Production Script (SOP 02).

**Task:**
Convert the script text into an **Audio Generation Table** with word counts verified.

**Output Format:**

| Sequence \# | Narration Text (From SOP 02) | Word Count | Est. Duration |
| :--- | :--- | :--- | :--- |
| **01** | "For months, this abandoned power station has been Haunter's undisputed domain. Tonight, that changes." | 16 words | ~8s |
| **02** | "Haunter attempts to phase through the wall. Impossible. An intruder has stolen the ghost's power." | 16 words | ~8s |

**CRITICAL: Duration Target**
- Each narration line MUST be **8 seconds or less** when accounting for pause penalties
- Count words AND all punctuation marks (periods + commas + em-dashes) BEFORE generating audio
- **Formula: Duration = (words ÷ 2) + (total_punctuation_marks × 2) + 1**
  - Where total_punctuation_marks = periods + commas + em-dashes
  - Pause penalty: Each punctuation mark adds ~2 seconds
  - Baseline overhead: +1 second for natural pacing
- **CRITICAL Punctuation Rules:**
  - **NEVER use em-dashes (—)** - they are banned completely
  - **Minimize commas** - each comma creates a 2-second pause just like periods
  - Prefer simple flowing sentences with no internal punctuation
- **Word limits based on punctuation count:**
  - 1 punctuation mark (1 period, 0 commas): max 10 words
  - 2 punctuation marks (1 period + 1 comma OR 2 periods): max 6 words
  - 3 punctuation marks: max 2 words
  - 4+ punctuation marks: avoid entirely
- If duration > 8 seconds: Either REDUCE WORDS or REMOVE COMMAS or COMBINE SENTENCES
- Target 8 seconds for optimal pacing (fills video while leaving trim buffer)

---

## Saving Instructions

After completing the Audio Generation Table for all sequences:

1. **Locate the Pokemon folder** created by the research prompt (e.g., `../pikachu/`)
2. **Save the complete output** (including Voice Configuration notes and the full Audio Generation Table) to:
   - Path: `../[pokemon-name]/05_audio_generation.md`
   - Example: For Pikachu, save to `../pikachu/05_audio_generation.md`
