# Script, 5-minute version: Role 3 (official test governance, prompt transfer, context ladder)

Follows the group timeline in `requirement video.md`: five parts, about 5:00, about 700 spoken words. Lines starting with `>` are stage directions; do not read them aloud.

---

## [SLIDE 1] 0:00–0:10 — Part 1: Title

Hello, I'm [tự điền: name], student ID [tự điền: ID], from Group 06, class CLC02.

## [SLIDE 2] 0:10–0:45 — Part 1: The problem

Teachers want to know *which parts* of an argumentative essay do not work, not only the overall score. We used PERSUADE 2.0: about twenty-six thousand student essays, split by expert raters into two hundred and thirty-eight thousand discourse units, each labelled Ineffective, Adequate or Effective. Only four and a half percent are Ineffective, so we report Macro-F1, which weights the three classes equally.

## [SLIDE 3] 0:45–1:30 — Part 2: My contribution and method

In week nine I built the data pipeline and the essay-level split. In weeks ten and eleven my role was the test and the generalisation checks. I trained the final DeBERTa models, Level 0, Level 1 and Prompt-Aware, and scored the official test exactly once: every choice was made on validation, and the test file's hash was written to a lock file first. This matters because if you look at the test even once to choose a model, the test score is no longer an honest estimate. Locked Level 1 scores 0.577 Macro-F1. Then I re-ran the leave-one-prompt-out experiment, and built a context ladder up to the whole essay.

## [SLIDE 4] 1:30–2:15 — Part 3: One real unit, from data to prediction

> Point to the input column, then the bars.

This is case 2, an Evidence unit from a "Car-free cities" essay, labelled Ineffective. It quotes paragraph 36 of the source correctly, then drifts into driving tests, which do not support the point. The unit is 244 words long. The same DeBERTa recipe reads a different input at each level, and the bars are the saved probabilities of Ineffective. With the unit alone, 0.001; with the neighbours, Level 1, 0.008, still predicted Effective; Prompt-Aware and two neighbours each side also stay below 0.03. With the whole paragraph, 0.83, even though that input is 747 tokens and is cut at 512; with the whole essay, 0.73. The wider inputs predict Ineffective, which is correct.

## [SLIDE 5] 2:15–2:20 — Part 3: Demo transition

Let me check this from the saved outputs.

## [DEMO] 2:20–2:45 — Part 3: Demo

> Terminal, font 18–20pt. Run `python MLA_Final/Code/reproduce_results.py`. [CUT] the wait. Highlight the Test rows and TABLE 3.

The reproduction script recomputes the paper's tables from saved predictions. Here are the official test rows, Level 1 locked at 0.577, and Table 3 with the three leave-one-prompt-out gaps.

> Run `python VIDEO_CA_NHAN/Nguoi_3_TestGovernance_LOPO_Ladder/demo/demo_nguoi3.py`. [CUT] the hashing wait. Highlight ① and ③.

My script hashes the test file: it still matches the lock written on 28 October, without reading any labels. It then recomputes test Macro-F1 for all three models from per-unit predictions, equal to the paper, and prints case 2 across the ladder.

## [SLIDE 6] 2:45–4:00 — Part 4: Results: prompt transfer

The main result of my part is generalisation. In leave-one-prompt-out, a prompt is removed from training and the model is scored on it. I compared that with the in-domain model on the *same* validation essays.

An unseen prompt costs Macro-F1: minus 0.092 on "A Cowboy Who Rode the Waves", minus 0.048 on "Distance learning", and minus 0.025 on "Summer projects", where the interval includes zero. And for wider context, one case is not evidence: on the whole validation set, no input beyond Level 1 is clearly better under the normal argmax rule. The wider inputs raise Ineffective recall to 54 to 59 percent but lose precision. After the same calibration correction for every model, the whole-essay model is plus 0.025, but that is post-hoc, on validation, and one run.

## [SLIDE 7] 4:00–5:00 — Part 5: One error and conclusion

The error I want to interpret was ours, and I found it. Our week-ten LOPO run chose the best epoch *using the held-out prompt itself*, which leaks test information into model selection, and it ran on a library version that broke DeBERTa training. I re-ran it with a fixed three epochs. The numbers went down, as expected when a leak is removed: on "Distance learning" the old gap was plus 0.004, the corrected one minus 0.048.

The limitation: three prompts and one run each, so linking the larger loss to source-based prompts is an interpretation, not a tested cause. Two runs of the same configuration also differ by up to about 0.004, so I do not claim that Prompt-Aware beats Level 1. This tool is meant to help teachers decide what to read first, not to grade students automatically. Thank you.
