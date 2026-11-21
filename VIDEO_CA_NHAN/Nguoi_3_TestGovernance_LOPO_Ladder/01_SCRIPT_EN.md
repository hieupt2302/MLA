# Script: Role 3 (official test governance, prompt transfer, context ladder)

Target length about 7:30, about 1,050 spoken words. Lines starting with `>` are stage directions; do not read them aloud.

---

## [SLIDE 1] 0:00–0:10 — Title

Hello, I'm [tự điền: name], student ID [tự điền: ID], from Group 06, class CLC02. In this video I explain my part of our project: how we scored the official test, how the model transfers to unseen prompts, and what wider context does.

## [SLIDE 2] 0:10–0:45 — The problem (shared with teammates)

Teachers who mark argumentative essays want to know *which parts* of an essay do not work, not only an overall score. Our group used the PERSUADE 2.0 corpus: almost twenty-six thousand student essays, split by expert raters into about two hundred and thirty-eight thousand discourse units, such as claims, evidence and rebuttals. Each unit is labelled Ineffective, Adequate or Effective. Only four and a half percent are Ineffective, so a model that always says "Adequate" is eighty percent accurate and useless. That is why we report Macro-F1, which weights the three classes equally.

## [SLIDE 3] 0:45–1:15 — My contribution

In week nine I built the data pipeline and the essay-level split. In weeks ten and eleven my role was the test and the generalisation checks. I trained the final DeBERTa models, Level 0, Level 1 and Prompt-Aware, and scored the official test exactly once, behind a lock file, as this diagram shows. Then I ran a 31-item review of our report and code, re-ran the leave-one-prompt-out experiment, and built a context ladder that goes beyond Level 1, up to the whole essay.

## [SLIDE 4] 1:15–2:45 — One real unit, through the context ladder

> Point to the input column first, then to the bars.

This is case 2, one of the ten high-confidence failures our group selected before training any context model. Validation row index 10,303, an Evidence unit from a "Car-free cities" essay with holistic score 2. The expert label is Ineffective.

The unit is 244 words long. It quotes paragraph 36 of the source text accurately, and then it drifts into reasoning about learner's permits and driving tests, which does not support the writer's point. So the weakness is inside the unit, but you only see it if you know what the paragraph is supposed to support.

On the left is what the model reads at each level. Level 0 is the unit alone. Level 1 adds the previous unit, the Position "I don't buy it", and there is no next unit. Paragraph gives the whole paragraph. Level 2 adds a passage of the source text. Level 3 gives the whole essay, 388 words.

Each input goes through the same DeBERTa-v3 recipe, and the bars show the saved probability of Ineffective. Level 0: 0.001. Level 1: 0.008, still predicted *Effective*. With the paragraph it jumps to 0.83. With the source passage, 0.54. With the whole essay, 0.73 after three epochs and 0.92 after seven. All four wider inputs predict Ineffective, which is correct.

## [SLIDE 5] 2:45–3:30 — What the data shows: no free lunch from wider context

One case is an illustration, not evidence. This chart is the whole validation set. With the normal argmax rule, no input beyond Level 1 is clearly better on Macro-F1. The wider inputs raise Ineffective recall to between 54 and 59 percent, but they flag more units and lose precision. Paragraph is worse than Level 1, minus 0.012.

And there is a check for case 2: if I lower Level 1's threshold until it flags as many units as the wider models, it still flips none of the ten cases. So the wider inputs carry real information, but the aggregate gain is unclear. After the same calibration correction for every model, the whole-essay model is plus 0.025, but that is post-hoc, on validation, one run.

## [SLIDE 6] 3:30–4:15 — Prompt transfer: leave-one-prompt-out

The second question is generalisation. In leave-one-prompt-out, a prompt is removed from training and the model is scored on that prompt. I compared it with the in-domain model on the *same* validation essays.

An unseen prompt costs Macro-F1: minus 0.092 on "A Cowboy Who Rode the Waves", minus 0.048 on "Distance learning", and minus 0.025 on "Summer projects", where the interval includes zero.

## [SLIDE 7] 4:15–4:20 — Demo transition

Let me check all of this from the saved outputs.

## [DEMO] 4:20–6:15 — Lock, recompute, trace

> Terminal in `MLA_Final/Code`, font 18–20pt.

First, the group's reproduction script.

> Run `python reproduce_results.py`. [CUT] the wait. Highlight the Test rows of TABLE 1, then TABLE 3.

These are the official test rows, Level 1 locked at 0.577, and here is Table 3, the leave-one-prompt-out gaps. All match the paper.

> Switch to the repo root. Run `python VIDEO_CA_NHAN/Nguoi_3_TestGovernance_LOPO_Ladder/demo/demo_nguoi3.py`. [CUT] the hashing wait.

My demo script checks the test governance. Part one hashes the official test file and compares it with the hash in the lock file, written on 28 October before scoring. They match, so the file has not changed. It does this without reading any labels. Part two recomputes test Macro-F1 for Level 0, Level 1 and Prompt-Aware from the saved per-unit predictions, and they equal the paper's table.

> Highlight part three.

Part three prints case 2 across the ladder, the numbers from my slide.

> Switch to the browser: `VAN_DAP_4_TIEU_CHI/trace_mau_that/TRACE_MAU_THAT_PIPELINE.html`, zoom 150%, scroll to the case 2 section.

And this is my trace notebook. It follows the same unit from the raw CSV row through the input text at each level, the token count, and the saved probabilities. The probabilities are saved outputs, because we no longer have the checkpoints.

## [SLIDE 8] 6:15–7:10 — Interpreting one error: the first LOPO run leaked

> Back to slides.

I want to interpret one error, because it was mine to find and fix. Our week-ten LOPO run picked the best epoch *using the held-out prompt itself*. That is test information leaking into model selection, and it also ran on a library version that we later found broke DeBERTa training.

I re-ran it with a fixed three epochs and the working version. The numbers went down, which is the direction you expect when a leak is removed: on "Distance learning", the old run showed no loss at all, plus 0.004, and the corrected run shows minus 0.048.

The remaining limitation: three prompts and one run per fold. So the link between source-based prompts and larger losses is an interpretation, not a tested cause.

## [SLIDE 9] 7:10–7:35 — Summary and evidence

To sum up: the official test was scored once, under a lock, and every number can be recomputed from saved predictions. Unseen prompts cost DeBERTa between 0.025 and 0.092 Macro-F1. Wider context helps some single cases, but it is not yet a proven aggregate gain, and the next step would be a pre-registered test. My files are listed here. Thank you.
