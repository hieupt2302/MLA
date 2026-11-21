# Script: Role 1 (data, classical models, essay length)

Target length about 7:30, about 1,050 spoken words. Lines starting with `>` are stage directions; do not read them aloud.

---

## [SLIDE 1] 0:00–0:10 — Title

> Slide 1. Look at the camera or the screen and smile briefly.

Hello, I'm [tự điền: name], student ID [tự điền: ID], from Group 06, class CLC02. In this video I explain my part of our project on predicting the effectiveness of argumentative discourse units.

## [SLIDE 2] 0:10–0:45 — The problem (shared with teammates)

Teachers who mark argumentative essays want to know *which parts* of an essay do not work, not only an overall score. Our group used the PERSUADE 2.0 corpus: almost twenty-six thousand student essays, split by expert raters into about two hundred and thirty-eight thousand discourse units, such as claims, evidence and rebuttals. Each unit is labelled Ineffective, Adequate or Effective. Only four and a half percent are Ineffective, so a model that always says "Adequate" is eighty percent accurate and useless. That is why we report Macro-F1, which weights the three classes equally.

## [SLIDE 3] 0:45–1:15 — My contribution

My role was the data side and the classical models. In weeks ten and eleven I did three things. First, I ran the Random Forest on Feature Set B, our strongest classical model, on the official test: I re-built it, checked that it reproduced its validation score, 0.526, and only then scored the test once. Second, I ran leave-one-prompt-out for the Random Forest on all fifteen prompts. That chart on the right shows the result: from 0.35 on the hardest prompt to 0.50 on the easiest. Third, I built the tables that check whether essay length is confounded with student proficiency.

## [SLIDE 4] 1:15–2:45 — One real unit, from raw data to a prediction

> Point to each box on the slide from left to right as you speak.

Here is one real unit from the official test file, so you can see how the data becomes a prediction.

It is raw record 57,633 in the test CSV. After we drop the rows without an effectiveness label, it becomes row index 47,059. It is a Position from an essay on the prompt "Facial action coding system", and the text is: "That is all everything you need to know about Mona Lisa and her smile."

The raw label string is "Ineffective". We encode the labels in a fixed order: Ineffective is zero, Adequate is one, Effective is two. So this unit is loaded as class zero.

One detail matters here. We always join files by this row index, never by the discourse ID, because Excel had rounded the discourse IDs. In the training file, 144,289 units share only 728 distinct ID values.

Next, Feature Set B turns the unit into numbers: word and bigram TF-IDF, at most fifteen thousand features; a one-hot code for the unit type; and five structural features. For this unit, the unit has 14 words, and the whole essay has only 225 words. Remember that number.

The Random Forest, two hundred trees with maximum depth thirty-five, outputs probabilities: 0.54 Ineffective, 0.34 Adequate, 0.11 Effective. The highest is Ineffective, so the prediction is Ineffective, which is correct. For comparison, our locked DeBERTa model gives this unit 0.98 Ineffective.

So the forest got this one right. But was it reading the sentence, or the length of the essay? The next two slides look at that.

## [SLIDE 5] 2:45–3:30 — What the data shows: length goes with proficiency

This chart shows every essay in the corpus: essay length against the holistic score the essay received. The correlation is strong, Spearman 0.76. The median score-2 essay has 229 words; the median score-6 essay has 824.

And the label mix moves with length. In the shortest quarter of validation essays, nine percent of units are Ineffective. In the longest quarter, just over one percent are. So "essay length" is partly "student level". And essay length is one of the five features we give the Random Forest.

## [SLIDE 6] 3:30–4:15 — Within the same score, errors still rise with length

So when the error rate rises with essay length, is it only because long essays come from stronger students? To separate the two, I compared length quartiles *within the same holistic score*.

This figure is for the locked DeBERTa model. For essays with score three, the error rate goes from 19.3 percent in the shortest quartile to 28.2 percent in the longest. A logistic regression that controls for the score gives an odds ratio of 1.19 per length quartile, with a confidence interval from 1.14 to 1.25. So proficiency does not explain all of it: length still matters within the same score.

## [SLIDE 7] 4:15–4:20 — Demo transition

> Show slide 7 for two seconds, then switch to the terminal.

Let me show this from the saved outputs.

## [DEMO] 4:20–6:15 — Reproduce and trace from saved outputs

> Terminal in `MLA_Final/Code`, font 18–20pt. Command already typed.

First, our reproduction script. It recomputes the main tables of the paper from the saved prediction files, in about five seconds.

> Run `python reproduce_results.py`. [CUT] any wait. Highlight the two Random Forest rows of Table 1.

Here is the Random Forest row: Macro-F1 0.523 on validation and 0.510 on the official test, with Ineffective recall of only 17.2 percent on the test. At the bottom, it confirms that every number matches the paper.

> Switch to the repo root. Run `python VIDEO_CA_NHAN/Nguoi_1_Data_Classical_Length/demo/demo_nguoi1.py`.

Now my own demo script. Part one traces the unit from the slide. If the raw test CSV is present, it reads the raw text; the label string becomes class zero; it shows the essay length, 225 words, so quartile one; and it prints the saved Random Forest probabilities, 0.544 for Ineffective.

> Highlight the "discourse_id" line.

Part two is the identifier check: 144,289 units, but only 728 distinct discourse IDs. That is why every join uses row index.

> Highlight the recall-by-quartile table.

Part three is new to this video, and it answers my question from slide four. It groups the test units by essay-length quartile and computes Ineffective recall for the Random Forest and for DeBERTa, directly from the saved predictions.

## [SLIDE 8] 6:15–7:10 — Interpreting one result: the forest leans on essay length

> Back to slides.

Here is the result as a chart. In the shortest essays, the Random Forest finds 23 percent of the Ineffective units. In the longest essays it finds almost none: 0.6 percent, two out of 309. DeBERTa also drops, but much less: from 45 to 35 percent.

My interpretation: because essay length is one of its features, and length tracks proficiency, the forest mostly learned "short essay means weak unit". That got our example right, but for a weak unit inside a long essay it almost never raises a flag. This is consistent with the paper's finding that the length effect is strongest for the Random Forest, an odds ratio of 1.31 after controlling for score. It is one reason a model that reads the text, DeBERTa, does better on the minority class.

The limitation is that this is a correlation on one split. I have not removed the essay-length feature and re-trained, so I cannot say how much of the forest's skill is only length. That would be my next controlled check.

## [SLIDE 9] 7:10–7:35 — Summary and evidence

To sum up my contribution: the Random Forest test run behind a validation gate, the fifteen-prompt LOPO baseline, and the length-by-score analysis. I should also say that two of my first outputs had errors, a join on the rounded IDs and a test script that was not exactly Feature Set B. They were caught in our group review on 31 October and re-run, and the numbers in this video are the corrected ones. My files are listed on this slide. Thank you.
