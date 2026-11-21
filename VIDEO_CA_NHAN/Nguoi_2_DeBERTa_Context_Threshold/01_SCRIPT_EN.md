# Script: Role 2 (DeBERTa, local context L0 vs L1, decision threshold)

Target length about 7:30, about 1,050 spoken words. Lines starting with `>` are stage directions; do not read them aloud.

---

## [SLIDE 1] 0:00–0:10 — Title

Hello, I'm [tự điền: name], student ID [tự điền: ID], from Group 06, class CLC02. In this video I explain my part of our project: the transformer model, the context experiment, and the decision threshold.

## [SLIDE 2] 0:10–0:45 — The problem (shared with teammates)

Teachers who mark argumentative essays want to know *which parts* of an essay do not work, not only an overall score. Our group used the PERSUADE 2.0 corpus: almost twenty-six thousand student essays, split by expert raters into about two hundred and thirty-eight thousand discourse units, such as claims, evidence and rebuttals. Each unit is labelled Ineffective, Adequate or Effective. Only four and a half percent are Ineffective, so a model that always says "Adequate" is eighty percent accurate and useless. That is why we report Macro-F1, which weights the three classes equally.

## [SLIDE 3] 0:45–1:15 — My contribution

My role was the DeBERTa side. In week nine I trained a single DeBERTa-v3 model and showed, on the same validation units, that it beats the Random Forest by 0.054 Macro-F1, so we dropped the older ensemble. In week ten I designed the controlled context experiment on the right: Level 0 gives the model only the unit; Level 1 adds the unit just before and just after it, and *nothing else changes*. In week eleven I scanned the decision threshold for the Ineffective class and ran the linear SVM baseline, on the test and on three held-out prompts.

## [SLIDE 4] 1:15–2:45 — One real unit: what the model reads, and what it says

> Point to the L0 box, then the L1 box, then the probability bars.

Here is case 8 from our error analysis: validation row index 108,613, a Claim from an essay on "Cell phones at school". The expert label is Ineffective.

At Level 0 the model reads only: the type, "Claim", a separator, and the sentence "Some kids will ask there parents to transfer school."

At Level 1 the input is longer. Before the target, it reads the previous unit, the evidence saying students will hide their phones and skip school. After it, the next unit: "If you chose policy one you will make the student happy." The format is "Previous", "Target", "Next", separated by SEP tokens.

DeBERTa's tokenizer cuts this text into sub-word tokens, at most 512, and the encoder turns it into one vector. A small classification layer turns that vector into three probabilities with a softmax.

Here are the saved probabilities. Level 0 gives Ineffective 0.017. Level 1 raises it to 0.058, more than three times higher, but Adequate is still 0.94, so the prediction stays Adequate, and it is wrong.

Why is the label Ineffective? Reading the essay, this claim is an unsupported prediction, and the neighbouring units do not give a reason for it either. So the local context did not supply what was missing.

## [SLIDE 5] 2:45–3:30 — What the data shows: Level 1 versus Level 0, per class

That is one unit. Across all units, this chart compares Level 1 minus Level 0, per class, with ninety-five percent bootstrap intervals by essay. The models scored on the test were trained by my teammate in week eleven, with the same recipe.

On the official test, ninety-three thousand units, Level 1 is better on every class. Macro-F1 rises by 0.016, and the largest gain is on Ineffective F1, plus 0.029. On validation the direction is the same, but the intervals for Ineffective and Effective include zero.

## [SLIDE 6] 3:30–4:15 — Where the gain comes from

This table shows what context changes unit by unit, on the test. About fifteen percent of predictions change. 7,615 units become correct, but 6,401 become wrong, so it is not a free improvement. For gold Ineffective units, 519 are newly found and 335 are lost.

By type, the gain is largest for Counterclaim, Rebuttal and Claim, the types whose quality is defined relative to a neighbouring unit. That is what we expected from local context.

## [SLIDE 7] 4:15–4:20 — Demo transition

Let me show this from the saved outputs.

## [DEMO] 4:20–6:15 — Reproduce Table 2, then trace case 8 and move the threshold

> Terminal in `MLA_Final/Code`, font 18–20pt.

First, the group's reproduction script recomputes the paper's tables from the saved prediction files.

> Run `python reproduce_results.py`. [CUT] the wait. Highlight TABLE 2.

Table 2 is my comparison: Level 1 minus Level 0 on the same units, plus 0.0087 Macro-F1 on validation and plus 0.0159 on the test, both matching the paper.

> Switch to the repo root. Run `python VIDEO_CA_NHAN/Nguoi_2_DeBERTa_Context_Threshold/demo/demo_nguoi2.py --theta 0.10`.

Now my demo script. Part one rebuilds the exact Level 0 and Level 1 input strings for case 8 and prints the saved probabilities for both levels.

> Highlight the threshold block.

Part two asks a practical question. A teacher might say: "flag every unit whose probability of Ineffective is at least theta". With theta 0.10 on the locked Level 1 model, on validation, recall for Ineffective rises from 44.7 to 69.6 percent, but the number of flagged units goes from 1,761 to 4,633, and Macro-F1 falls from 0.581 to 0.535. The script also counts it: 330 extra correct flags, but 2,542 extra false alarms.

> Highlight the case 8 line.

And case 8, with probability 0.058, is still not flagged at 0.10.

## [SLIDE 8] 6:15–7:10 — Interpreting one result: a threshold moves the operating point

> Back to slides.

This figure shows the whole trade-off. As theta goes down, recall goes up, precision goes down, and Macro-F1 falls steadily. Every extra Ineffective unit we catch costs about eight false alarms.

So lowering the threshold does not make the classifier better. It only moves the operating point along the same curve. Whether a teacher wants to read about 4,600 flagged units to see seventy percent of the weak ones, or about 1,800 to see forty-five percent, is the user's decision. We did not choose it on the test.

I should also correct my own first version here. In week eleven I first reported 76.5 percent recall at theta 0.10 and said case 8 would be caught. The correct value was 73.0 percent, and it only held for the first Level 1 run. For the locked model, case 8 is flagged only if theta is 0.058 or lower.

## [SLIDE 9] 7:10–7:35 — Summary and evidence

To sum up: Level 1 helps a little and consistently, about 0.016 Macro-F1 on the test, mostly on relational types. But my first run gave only plus 0.002 on validation, so the gain is about the same size as run-to-run variation, and I call it "small", not "proven". The threshold is a user choice, not a model improvement. My files are listed here. Thank you.
