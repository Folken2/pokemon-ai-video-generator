# Audio Generation: "First Flight"

**Episode:** Real Life Pokémon: Charizard — First Flight
**Total Sequences:** 12
**Target Duration per Clip:** 8 seconds (7-9 second acceptable range)

---

## Voice Configuration (The "Documentary" Preset)

| Parameter | Value | Rationale |
| :--- | :--- | :--- |
| **Voice ID** | British, Deep, Mature, Calm (e.g., "David" clone) | Attenborough-style narration |
| **Stability** | 35% - 45% | Lower stability = more breathiness and natural fluctuation |
| **Clarity + Similarity** | 75% | High fidelity for studio-quality sound |
| **Style Exaggeration** | 10% - 15% | Slight theatrical weight without caricature |

---

## The "8-Second Audio Rule"

**Formula:** `Duration = (words ÷ 2) + (total_punctuation_marks × 2) + 1`

**Constraints:**
- Videos are 10 seconds. Audio MUST be 8 seconds (range: 7-9 seconds)
- NEVER use em-dashes (—) — they are banned completely
- Minimize commas — each creates a 2-second pause
- Word limits by punctuation count:
  - 1 punctuation mark (1 period, 0 commas): max 10 words
  - 2 punctuation marks: max 6 words
  - 3 punctuation marks: max 2 words

---

## Audio Generation Table

| Sequence # | Narration Text | Word Count | Punctuation | Est. Duration |
| :--- | :--- | :--- | :--- | :--- |
| **01** | "The young Charmeleon challenges the fire king of the mountain." | 10 | 1 (.) | 8s |
| **02** | "The fight is brief. Victory absolute." | 6 | 2 (. .) | 8s |
| **03** | "Defeated and bleeding the challenger is driven from the mountain." | 10 | 1 (.) | 8s |
| **04** | "Alone on a distant cliff something inside begins to change." | 10 | 1 (.) | 8s |
| **05** | "This is not the magic of fairy tales but metamorphosis." | 10 | 1 (.) | 8s |
| **06** | "The wings tear through flesh still wet and violently trembling." | 10 | 1 (.) | 8s |
| **07** | "For forty eight hours it does not sleep or eat." | 10 | 1 (.) | 8s |
| **08** | "At dawn something new and terrible stands at the edge." | 10 | 1 (.) | 8s |
| **09** | "Below this creature waits a thousand feet of empty air." | 10 | 1 (.) | 8s |
| **10** | "It makes its choice and steps forward off the edge." | 10 | 1 (.) | 8s |
| **11** | "Freefall. Then ancient instinct takes hold." | 6 | 2 (. .) | 8s |
| **12** | "The rematch will come. But not today." | 7 | 2 (. .) | 8.5s |

---

## Duration Verification

| Scene | Calculation | Result |
| :--- | :--- | :--- |
| 01 | (10 ÷ 2) + (1 × 2) + 1 = 5 + 2 + 1 | 8s ✓ |
| 02 | (6 ÷ 2) + (2 × 2) + 1 = 3 + 4 + 1 | 8s ✓ |
| 03 | (10 ÷ 2) + (1 × 2) + 1 = 5 + 2 + 1 | 8s ✓ |
| 04 | (10 ÷ 2) + (1 × 2) + 1 = 5 + 2 + 1 | 8s ✓ |
| 05 | (10 ÷ 2) + (1 × 2) + 1 = 5 + 2 + 1 | 8s ✓ |
| 06 | (10 ÷ 2) + (1 × 2) + 1 = 5 + 2 + 1 | 8s ✓ |
| 07 | (10 ÷ 2) + (1 × 2) + 1 = 5 + 2 + 1 | 8s ✓ |
| 08 | (10 ÷ 2) + (1 × 2) + 1 = 5 + 2 + 1 | 8s ✓ |
| 09 | (10 ÷ 2) + (1 × 2) + 1 = 5 + 2 + 1 | 8s ✓ |
| 10 | (10 ÷ 2) + (1 × 2) + 1 = 5 + 2 + 1 | 8s ✓ |
| 11 | (6 ÷ 2) + (2 × 2) + 1 = 3 + 4 + 1 | 8s ✓ |
| 12 | (7 ÷ 2) + (2 × 2) + 1 = 3.5 + 4 + 1 | 8.5s ✓ |

**Total Estimated Runtime:** ~96 seconds (12 sequences × 8 seconds)

---

## File Naming Protocol

Generated audio files should follow this format:
```
Sequence_01_Narrative.mp3
Sequence_02_Narrative.mp3
...
Sequence_12_Narrative.mp3
```

Each file corresponds strictly to its matching video clip number.

---

## Production Notes

### Pacing Guidance

| Act | Sequences | Emotional Tone |
| :--- | :--- | :--- |
| **Act 1: The Challenge** | 01-03 | Tension building to defeat |
| **Act 2: The Metamorphosis** | 04-08 | Quiet intensity, body horror |
| **Act 3: First Flight** | 09-12 | Rising tension to triumph |

### Special Delivery Notes

- **Sequence 02**: Two short sentences with punchy delivery — pause between "brief." and "Victory"
- **Sequence 06**: Visceral content — voice should convey discomfort without melodrama
- **Sequence 10-11**: Slight tempo increase for tension leading to the leap
- **Sequence 11**: "Freefall." should have weight, then pickup on "Then ancient instinct"
- **Sequence 12**: Final line needs closing weight/finality — the promise of continuation

### Quality Checklist

Before generating each audio clip:
- [ ] Verify word count matches table
- [ ] Confirm no em-dashes present
- [ ] Check comma count (minimize)
- [ ] Test calculated duration ≤ 8 seconds

---

*Audio generation specifications for "Real Life Pokémon: Charizard — First Flight"*
