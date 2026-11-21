# Script, 5-minute version: Role 2 (DeBERTa, local context L0 vs L1, decision threshold)

Follows the group timeline in `requirement video.md`: five parts, about 5:00, about 700 spoken words. Lines starting with `>` are stage directions; do not read them aloud.

---

## [SLIDE 1] 0:00–0:10 — Part 1: Title

Hello, I'm [tự điền: name], student ID [tự điền: ID], from Group 06, class CLC02.

## [SLIDE 2] 0:10–0:45 — Part 1: The problem

Teachers want to know *which parts* of an argumentative essay do not work, not only the overall score. We used PERSUADE 2.0: about twenty-six thousand student essays, split by expert raters into two hundred and thirty-eight thousand discourse units, each labelled Ineffective, Adequate or Effective. Only four and a half percent are Ineffective, so we report Macro-F1, which weights the three classes equally.

## [SLIDE 3] 0:45–1:30 — Part 2: My contribution and method

My role was the transformer side. The model is DeBERTa-v3-base, fine-tuned for three epochs with a class-weighted loss, so mistakes on the rare Ineffective class cost more. In week nine I showed that a single DeBERTa-v3 model beats the Random Forest by 0.054 Macro-F1 on the same validation units. In week ten I designed a controlled context experiment: Level 0 gives the model only the unit; Level 1 adds the unit just before and just after it, and nothing else changes: same data, same recipe, same seed, same units. In week eleven I scanned the decision threshold for the Ineffective class and ran the linear SVM baseline.

## [SLIDE 4] 1:30–2:15 — Part 3: One real unit, from data to prediction

> Point to the L0 box, the L1 box, then the bars.

This is case 8, a Claim from an essay on "Cell phones at school": "Some kids will ask there parents to transfer school." The expert label is Ineffective. At Level 0 the model reads the type, a separator, and this sentence. At Level 1 it also reads the previous and next units, marked "Previous", "Target" and "Next". The tokenizer turns the text into sub-word tokens, and the encoder plus a softmax layer gives three probabilities. Level 0 gives Ineffective 0.017; Level 1 raises it to 0.058, but Adequate is still 0.94, so both predict Adequate, which is wrong. Reading the essay, this claim is an unsupported prediction, and the neighbouring units do not give a reason for it either, so local context could not supply what was missing.

## [SLIDE 5] 2:15–2:20 — Part 3: Demo transition

Let me show this from the saved outputs.

## [DEMO] 2:20–2:45 — Part 3: Demo

> Terminal, font 18–20pt. Run `python MLA_Final/Code/reproduce_results.py`. [CUT] the wait. Highlight TABLE 2.

The reproduction script recomputes Table 2 from the saved predictions: Level 1 minus Level 0 is plus 0.0087 on validation and plus 0.0159 on the test, matching the paper.

> Run `python VIDEO_CA_NHAN/Nguoi_2_DeBERTa_Context_Threshold/demo/demo_nguoi2.py --theta 0.10 --no-raw`. Highlight parts ② and ③.

My script prints the exact Level 0 and Level 1 strings for case 8 with their saved probabilities. Then it moves the threshold to 0.10: flagged units go from 1,761 to 4,633, with 330 extra correct flags and 2,542 extra false alarms. And case 8 is still not flagged.

## [SLIDE 6] 2:45–4:00 — Part 4: Results: Level 1 versus Level 0

Across all units, this chart shows Level 1 minus Level 0, per class, with bootstrap intervals by essay. The models scored on the test were trained by my teammate with the same recipe.

On the official test, Level 1 is better on every class: plus 0.016 Macro-F1, and the largest gain is Ineffective F1, plus 0.029. The gain is largest for Counterclaim, Rebuttal and Claim, whose quality is judged relative to a neighbouring unit. Unit by unit on the test, about fifteen percent of predictions change: 7,615 become correct, but 6,401 become wrong, so context is not a free improvement. And the gain is small: my first run gave only plus 0.002 on validation, so the gain is about the size of run-to-run variation.

## [SLIDE 7] 4:00–5:00 — Part 5: One limitation and conclusion

Now the threshold. A teacher could flag every unit whose probability of Ineffective is at least theta. With theta 0.10 on validation, recall rises from 45 to 70 percent, but Macro-F1 falls from 0.581 to 0.535, and every extra catch costs about eight false alarms. So a threshold does not make the classifier better; it only moves the operating point. Whether a teacher wants to read about 4,600 flagged units to see seventy percent of the weak ones, or about 1,800 to see forty-five percent, is their decision, and we did not choose it on the test.

I also have to correct my own first version: I first reported 76.5 percent recall at 0.10 and said case 8 would be caught. The correct value was 73.0 percent, for the first Level 1 run only. For the locked model, case 8, at 0.058, is not flagged. This tool should help teachers decide what to read first, not grade students automatically. Thank you.
