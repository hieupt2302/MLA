# Script, 5-minute version: Role 1 (data, classical models, essay length)

Follows the group timeline in `requirement video.md`: five parts, about 5:00, about 700 spoken words. Lines starting with `>` are stage directions; do not read them aloud.

---

## [SLIDE 1] 0:00–0:10 — Part 1: Title

Hello, I'm [tự điền: name], student ID [tự điền: ID], from Group 06, class CLC02.

## [SLIDE 2] 0:10–0:45 — Part 1: The problem

Teachers want to know *which parts* of an argumentative essay do not work, not only the overall score. We used PERSUADE 2.0: about twenty-six thousand student essays, split by expert raters into two hundred and thirty-eight thousand discourse units, each labelled Ineffective, Adequate or Effective. Only four and a half percent are Ineffective, so we report Macro-F1, which weights the three classes equally.

## [SLIDE 3] 0:45–1:30 — Part 2: My contribution and method

My role was the data side and the classical models. The units are split by essay, so no essay appears in two sets, and the official test file is scored only once. In weeks ten and eleven I did three things. I re-built our Random Forest on Feature Set B, two hundred trees with balanced class weights so that mistakes on the rare class cost more, and checked that it reproduced its validation score, 0.526, before scoring the test once. I ran leave-one-prompt-out for the forest on all fifteen prompts, from 0.35 to 0.50 Macro-F1. And I built the tables that check whether essay length is confounded with student proficiency.

## [SLIDE 4] 1:30–2:15 — Part 3: One real unit, from data to prediction

> Point to each box from left to right.

Here is a real unit from the test file: row index 47,059, a Position on "Facial action coding system": "That is all everything you need to know about Mona Lisa and her smile." The label string "Ineffective" is loaded as class zero. We join files by row index, never by discourse ID, because Excel had rounded those IDs. Feature Set B turns the unit into TF-IDF features, the unit type, and five structural features. This unit has 14 words, and its essay only 225. The forest outputs 0.54 for Ineffective, so it predicts Ineffective, which is correct.

## [SLIDE 5] 2:15–2:20 — Part 3: Demo transition

Let me show this from the saved outputs.

## [DEMO] 2:20–2:45 — Part 3: Demo

> Terminal, font 18–20pt. Run `python MLA_Final/Code/reproduce_results.py`. [CUT] the wait. Highlight the Random Forest rows.

Our reproduction script recomputes the paper's tables from the saved prediction files in about five seconds. Here is the forest: 0.510 Macro-F1 on the official test, but Ineffective recall of only 17.2 percent. At the bottom it confirms every number matches the paper.

> Run `python VIDEO_CA_NHAN/Nguoi_1_Data_Classical_Length/demo/demo_nguoi1.py --no-raw`. Highlight parts ② and ③.

My own script traces the same unit: label id zero, 225 words, so the shortest quartile, and forest probability 0.544. Part two confirms why we never join on discourse ID: 144,289 units share only 728 distinct values. Part three groups the test units by essay length and computes Ineffective recall for both models, directly from the saved predictions.

## [SLIDE 6] 2:45–4:00 — Part 4: Results: length goes with proficiency

Essay length and holistic score are strongly linked: Spearman 0.76 over all essays. In the shortest quarter of validation essays nine percent of units are Ineffective; in the longest, just over one percent.

So is a rising error rate with length only about proficiency? I compared length quartiles *within the same score*. For score-three essays, the locked DeBERTa model's error rate goes from 19.3 percent to 28.2 percent. Controlling for score, the odds of an error rise by a factor of 1.19 per quartile. So length still matters within the same score, although we have not identified the mechanism. Interestingly, Macro-F1 stays almost flat across quartiles, about 0.53 to 0.55 on validation. What changes is which class is hard: long essays have many more Effective units and very few Ineffective ones.

## [SLIDE 7] 4:00–5:00 — Part 5: One limitation and conclusion

Here is what my demo computed. The forest finds 23 percent of Ineffective units in the shortest essays, but only 0.6 percent, two out of 309, in the longest. DeBERTa drops much less, from 45 to 35 percent. The shortest quartile holds 2,384 gold Ineffective units; the longest only 309.

My interpretation: essay length is one of the forest's features, and length tracks proficiency, so the forest mostly learned "short essay, weak unit". This is consistent with the paper's finding that the length effect is strongest for the forest, an odds ratio of 1.31 after controlling for score. That got our example right, but it almost never flags a weak unit in a long essay. The limitation: I have not re-trained without the length feature, so this reliance is inferred, not tested.

Two of my first outputs had errors, a join on the rounded IDs and a test run that was not exactly Feature Set B; they were fixed in our 31 October review, and these are the corrected numbers. This tool is meant to help teachers decide what to read first, not to grade students automatically. Thank you.
