## MLA Final Project Requirements and Rubric

61FIT4MLA and 62FIT4MLA | Labs 30% | Interview 30% | Report 40% | 26 Oct 2026

Week 10 is an in-class project review; individual interviews begin in Week 11. A strong project shows that you understand the problem defined by your data, compare methods fairly, and explain the results. Use a research-paper structure for the report. Publication and a new model are not required for high marks.

## Final assessment breakdown

| Component | Maximum points | Assessment unit |
| --- | --- | --- |
| Labs 7, 8, and 9 | 30 | Individual submitted work |
| Interview | 30 | Each student |
| Report and reproducibility materials | 40 | Group with contribution disclosure |

F = 0.30 × L + 0.30 × I + 0.40 × R, with L, I, and R on a 0–10 scale. The interview raw score is out of 30: I = S_I/3. The report raw score is out of 40: R = S_R/4. For L=7, S_I=18/30, and S_R=32/40, I=6, R=8, and F=7.1. The course grade is 0.10P + 0.30M + 0.60F, where P is participation and M is the midterm. Labs, interview, and report therefore contribute up to 18%, 18%, and 24% of the course grade; do not add another final-assessment component.

## Core requirements for every group

- Define one question, target population, and prediction time. State who will use the result.

- Use data with a clear source and permitted use. Explain the row unit, labels, split, and one real sample traced through the full pipeline.

- Include an appropriate baseline and at least two course model families, with an interpretable reference model. LLM prompting does not count as a model family.

- Beyond comparing models, conduct one controlled check: remove a feature, change the representation, test an assumption or label, examine a predefined subgroup, or assess sensitivity.

- Read at least 10 error or disagreement cases yourself. Record IDs, labels, predictions, evidence- based explanations, and a conclusion linked to the evidence.

- Provide code and lawfully accessible data to reproduce the main results table. Identify individual contributions and AI use.

These requirements apply to both classes when announced by the lecturer. Previously announced lab rubrics and deadlines remain in force; no new work is required to regrade old labs. The interview schedule and final report deadline are separate LMS announcements.


## Assessment of Labs 7 to 9

The three labs carry equal weight within the lab component unless your class has already received a different rule. Retain each lab’s published rubric and deadline and convert scores to a 0–10 scale. No new criteria or experiments will be added retrospectively. Any clarification of score conversion will use the rubrics and records already applied.

| Lab | Course evidence | Transfer to the project |
| --- | --- | --- |
| 7 Neural Networks | Forward/backward passes and gradient checks; train/validation curves; MLP versus LR on a fixed split. | Explain loss and model complexity. A simple model winning is a valid result. |
| 8 Probabilistic Models | MLE/MAP/posterior/predictive, assumptions and priors; Step 7 chooses an estimator and compares it with the pooled rate. | Reason about small-sample estimation and probability. Do not assume real data follow Beta-Bernoulli assumptions. |
| 9 Gaussians and GDA | Mean/covariance, distance, and shared- covariance assumptions; Step 7 selects a classifier against the baseline. | Connect feature shape to decisions. GDA is not required for sparse text or image features. |

Lab 7 uses training and validation sets only; do not rename validation as test. Labs 8 and 9 use synthetic data, so lab results do not establish effectiveness for real learners. Transfer the reasoning behind your choices; you do not need to put every algorithm from all three labs into the project.

## What counts as enough experimentation

A meaningful minimum experiment matrix contains a baseline, model A, model B, and A or B with one controlled change to test a hypothesis. For each row, record the question, change, configuration, split/seed, metric, run/output, and decision after inspection. Judge the experiments by the questions answered, not by model count or report length.

For models sensitive to initialization, three seeds are suggested if resources permit. For small datasets or repeated observations from people, use appropriate group-based folds. Seeds and folds containing overlapping samples are not independent datasets. Do not rerun an already stable model just to increase the count. With limited GPU access, use a development subset selected by a stated rule and report its scope.


## Report rubric out of 40 points

## Question and scope 4 points

Identify the user, decision, input/output, and prediction time. Ask a measurable question and limit conclusions to the relevant population.

Needs improvement: only a topic is given; the output, label, or prediction time is unclear.

## Understanding the data 8 points

Explain the source and conditions of use, row unit and independent groups, labels, distributions, missingness, duplicates, and one sample trace. Recognize measurement limitations.

Needs improvement: columns are described without checking labels; row count is confused with person count; feature availability is unclear.

## Methods and model selection 8 points

Use a suitable baseline and two model families appropriate for the data. Explain features, loss, assumptions, and model selection. Fit preprocessing within training data or each training fold.

Needs improvement: model names replace reasoning; two configurations of one family are counted as two families; choices are based on the test set.

## Experiments and comparisons 6 points

Compare methods on the same data, budget, and metrics. Save configurations, conduct a controlled check, and assess stability in a way suited to sample size and resources.

Needs improvement: only a favourable score table is shown; splits differ; the baseline is absent; run count replaces a reason for running.

## Error analysis and original work 6 points

Read at least 10 cases selected by a stated rule, including errors or disagreements. Group the errors, formulate and test a hypothesis on development data, and record the resulting decision.

Needs improvement: errors are listed without reading the data; AI-generated guesses are presented as explanations; outputs are copied without analysis.

## Reproducibility and evidence 4 points

Provide a command or notebook that produces the main table, with versions, seeds/splits, IDs, predictions, and environment details. Identify each member’s contribution.

Needs improvement: tables cannot be traced to runs; the notebook has not been executed; files or access permissions are missing.

## Report quality and responsible use 4 points

Connect problem → question → method → data → result → interpretation. Make figures and tables understandable on their own. Use sources that support the exact claims; state limitations, data permissions, and AI use.

Needs improvement: fluent prose lacks evidence; citations do not support the claims; conclusions exceed the evidence or treat a proxy as ground truth.

For each criterion, the reference levels are 0%, 50%, 75%, and 100% of its weight: no verifiable evidence; partial evidence with a material defect; meets requirements with minor gaps; complete and independently explained or checked. Intermediate marks require an evidence note. Model complexity, attractive scores, and paper-like prose do not earn marks by themselves.


## Individual interviews from Week 11

The interview assesses your ability to apply ML in your own project. Each student receives an individual mark, separate from the group report mark. Understand the overall pipeline and explain and check your own part in depth. Plan for approximately 6–8 minutes per student, according to the LMS schedule.

## What to prepare before your slot

- Your current report or draft with the question, data source, baseline, models, and a results table. The interview version is not the final report submission.

- The notebook/scripts, configurations, and predictions/logs behind the main table. Open them in advance and keep outputs that can be viewed offline.

- One sample with an ID traced from features  prediction  comparison with the label, and one error or disagreement you have examined. Display only data you are permitted to show.

- Your split diagram and prediction time. Record where preprocessing is fitted, which set selects the model/threshold, and how the test set has been used.

- Evidence of a task you personally own and how you used and checked AI assistance. Keep this in the existing report/repository; no additional long progress report is needed.

## Sequence of an interview

| Time | Focus | What you do |
| --- | --- | --- |
| 0–1 min | Data | Open a sample; state what is predicted, for whom, and what information is available. |
| 1–3 min | Model | Explain features, the baseline, and one prediction step of the main model. |
| 3–5 min | Evaluation | Read a table or error case and reason about a change in data, metric, or use conditions. |
| 5–7 min | Own work | Show individual evidence and perform or trace one small check. |
| Up to 1 extra min |   | Clarification Write/draw, clarify an answer, or record a check that needs follow-up. |

You may consult your own materials and code; teammates and AI tools must not answer or coach you. The lecturer selects samples or equivalent question variants. Full retraining is not required. Small checks use development data, saved outputs, or synthetic data; a sealed test set need not be opened.


## Interview rubric out of 30 points

| Criterion |   | Pts Evidence to demonstrate |
| --- | --- | --- |
| Data and labels | 8 | Open a sample with an ID. Explain the observation unit, label, feature availability, split, and one data risk. |
| Model reasoning and selection | 8 | Trace features to prediction. Explain the baseline, loss/assumptions, and model suitability; reason about a changed condition. |
| Evaluation and results 8 |   | Interpret a result against the baseline under the same conditions, a metric, an error case, and limitations. Explain test-set use. |
| Individual contribution and practical check | 6 | Show evidence of your own work. Perform or trace a small step and explain a decision checked or revised. |

## How to interpret the score levels

| Level | Out of 8 | Out of 6 | Observable evidence |
| --- | --- | --- | --- |
| Not demonstrated 0 |   | 0 | No relevant evidence, or a fundamental misunderstanding after clarification. |
| Partial understanding | 4 | 3 | Names terms or reads outputs without connecting them to samples and decisions. |
| Basic application 6 |   | 4.5 | Explains a real sample correctly; needs a short prompt or leaves a gap when conditions change. |
| Independent application | 8 | 6 | Connects the steps, checks evidence, reasons conditionally about changes, and identifies limitations. |

Apply these levels separately to each criterion. Intermediate marks require evidence. An 8-point criterion uses 0, 4, 6, 8; the 6-point criterion uses 0, 3, 4.5, 6. One incorrect answer does not make the entire interview zero. Conditional reasoning and recognizing insufficient evidence are valid; you do not need to guess a definite direction of performance change.

## Six questions to practise on your project

- 1. Choose one row. What does its label measure, which features exist at prediction time, and which groups must remain separate in the split?

- 2. For that row, what does the baseline predict, and how does the main model produce its prediction?

- 3. Choose an assumption or preprocessing step. What could change if you altered it, and what comparison would test your prediction?

- 4. Point to a result. Against the baseline on the same split and budget, what evidence supports your choice?

- 5. Choose an error or disagreement. What did you observe, which hypothesis remains untested, and what is a feasible next step?

- 6. Show your own work. Where is the evidence, how did you check it, and what decision did the result change?

You may answer in Vietnamese or English and write or draw when helpful. Marks assess correctness and application, not fluency. If access fails, use saved outputs or an equivalent check; the lecturer will arrange a follow-up if a technical problem still prevents sufficient evidence.


## Individual contribution and AI use

Identify at least one decision you owned: a data issue discovered, a comparison designed, a case examined, or a choice revised after inspecting results. Log the date, question, pre-run assumption, output, and change. Do not invent a history that was never recorded; start recording now and disclose the earlier gap.

Disclose AI tools used for explanations, writing, debugging, or data generation, and explain how you checked their help. If AI is part of the studied pipeline, also save the model/version, prompts, settings, and responses. Do not fabricate results or citations or repeat an unverified mechanism. Understanding is checked through data and traces; AI detectors are not used as proof of misconduct.

## Frequently asked questions

Must the report be finished before the interview? No. Use the current version saved before your slot. The final deadline will be announced separately on LMS. You may revise the report afterwards and record the changes.

Must I retrain everything in class? No. You may predict one sample, recalculate a small metric, or trace saved predictions/logs. Prepare evidence that supports an equivalent check without network access.

What if my model does not beat the baseline? Report the result honestly. Valid comparisons, data understanding, and justified limitations earn credit. Do not select a new model using the test set to obtain a better score.

What if I worked on only one part? Understand the overall pipeline and your own responsibility in depth. Report writing and error analysis count as contributions when supported by evidence and reasoning.

Does everyone in a group receive the same interview mark? No. Each person is questioned and marked individually. The group report or a teammate’s answer cannot replace your own demonstration of understanding.

What if access or equipment fails? Report it immediately and use saved outputs or an equivalent written, diagram-based, or numerical check. If evidence remains unavailable because of the failure, the lecturer records it and arranges an equivalent follow-up; technical failure is not automatically treated as lack of understanding.


## Valid evaluation and proportionate conclusions

Keep development separate from test. Fit scalers, TF-IDF, feature selection, and tuning within training data or each training fold. If the goal is to predict for new people, items, or documents, keep the relevant units separate. For future predictions, features must contain only information known at prediction time; time-based splits must match the question. See the official scikit-learn guidance on common pitfalls and cross-validation below.

[scikit-learn Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html)

[scikit-learn Cross validation grouped data and time series](https://scikit-learn.org/stable/modules/cross_validation.html)

Changing a seed or renaming a test set does not make it unseen again. Record when and why you used it; make subsequent choices on development data. If no independent confirmation set remains, describe results after repeated selection as exploratory. Do not create an inadequately small extra test set merely to use the word holdout.

Compare methods on the same units and metrics. For review-prioritization tasks, use the same K/budget and state tie-breaking rules. Report the base rate, case counts, and suitable metrics. If using bootstrap, resample at the relevant person/document/cluster level. A confidence interval for the paired difference addresses A versus B directly; overlap of separate intervals does not settle that comparison. No improvement can still earn high marks when evaluation and conclusions are sound.

## Pass threshold and missing evidence

Both LMS courses require F≥5/10 for the final assessment. This guide adds no separate interview or report pass threshold. Missing error analysis or reproducibility evidence affects the relevant criterion and is handled under the published course process. A broken link alone does not automatically mean zero or failure. Any misconduct decision requires specific evidence and the course procedure.

## A self-check before explaining a result

For this sample, what is known at prediction time? Which assumption distinguishes model A from the baseline? If the strongest feature is removed or the target population changes, what might change and why?


## Submission package and paper-style report

A suggested length is 6–8 main-text pages, plus references and appendices as needed, in a readable PDF. A venue template is not required. Write in Vietnamese or English according to the lecturer’s published rules. Previously announced mandatory requirements take precedence if they differ from this suggestion.

| Section | Minimum content |
| --- | --- |
|   | Abstract and Introduction One question, its purpose, data/scope, main finding, and limitation. |
| Data and Method | Source/permissions, units/labels, a real example; baseline, features, two model families, and assumptions. |
| Experimental setup | Splits/groups/time; preprocessing, metrics, tuning, configurations/seeds, and test- use history. |
|   | Results and Error analysis Fair comparison table, a hypothesis check, error cases and denominators; avoid cherry-picking. |
|   | Discussion and Conclusion What the results do and do not answer, comparison with sources read, and recommendations within scope. |
| References and appendices | Sources supporting exact claims; run table, AI disclosure, contributions, execution instructions, and predictions. |

Submit the PDF report, executed notebook/scripts, reproduction instructions, a permitted data link/version or sample, split IDs/configurations/seeds, predictions behind the main table, error table, experiment and contribution log, and AI disclosure. Do not put private or restricted data in a public repository.

## Potential for a research paper

This is an optional extension. A strong course report can receive full marks without novelty, a venue submission, private data, or paid APIs. Developing it into a paper additionally requires a specific contribution, comparison with the closest work, reproducible evidence and appropriate confirmation, data-use permission, and defensible conclusions. High marks or many models do not establish publication readiness.


## Week 10 review and interviews from Week 11

Week 10 introduces the requirements and provides in-class review. Individual interviews begin in Week 11. Named slots and the final report deadline will be announced separately on LMS.

| Stage | Task | Evidence |
| --- | --- | --- |
| Week 10 | In-class review and requirements | Bring the current work, a sample, a result, and a question. Agree on up to three actions, owners, and completion evidence. This is formative, not an interview mark. |
| Before your slot | Save the interview version | Share the current draft through the specified LMS channel and check access. Save report, code/configurations, and outputs. The final report need not be complete. |
| From Week 11 | Begin individual interviews | Follow the class schedule on LMS, approximately 6–8 minutes per student. Completion for everyone in Week 11 is not assumed. |
| After the interview | Complete the report | Record revisions after feedback. Submit the report and reproducibility materials by the separate LMS deadline. |

## Bring evidence to each meeting

In Week 10, use the start of your existing report to show what is done, the output link, one point you do not understand, and one decision needing feedback. Do not create another long report. Each member explains or writes one pipeline step. Finish with up to three actions, named owners, and completion evidence. This review does not earn an interview mark; grading starts in the scheduled individual interviews from Week 11.

Prepare two answers: Which result did your group check itself, and what decision changed? If you could keep only one table and one error case, which would best support your main conclusion?
