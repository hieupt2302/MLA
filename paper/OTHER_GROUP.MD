Argument-Structure-Based Feedback
Prioritisation for English Argumentative Essays
Teacher: Bùi Quốc Khánh
Group 04
    Member 1: Nguyễn Xuân Hòa - 2301140035
    Member 2: Hoàng Tùng - 2301140099
    Member 3: Nguyễn Duy Anh - 2301140006
1. Problem and user
2 / 8
Problem
• Teachers must read every essay to find the weak arguments
• Writing detailed comments for a whole class takes hours
• Learners get a score, but not which part to fix
User and decision
• User: a teacher of English argumentative writing
• Decision 1: which essays to read first
• Decision 2: which segments need comments
• Decision 3: which essays the tool is unsure about
• Learners see a diagnosis only after the teacher approves it
2. Data
3 / 8
Dataset
• PERSUADE CORPUS 2.0 (Crossley et al., 2024, Assessing
Writing)
• Route: public benchmark
• Argumentative essays by US students, grades 6–12
• Licence: CC BY-NC-SA 4.0 — academic, non-commercial
• In hand: official train set (15,594) and test set (10,402), no
overlap
Size and fields
25,996
essays · 15 prompts
~238,000
labelled segments
13,121
independent essays
• Segment: argument role + effectiveness (Ineffective /
Adequate / Effective)
• Essay: holistic score 1–6
• Prompt: used for prompt-based splitting
• Demographics (ELL, gender…): fairness checks only, never a
model input
3. ML task
4 / 8
Three-step pipeline
• Step 1 · Sentence role: 8-class classification
In: one sentence + its position in the essay
Out: Lead / Position / Claim / Counterclaim / Rebuttal / Evidence /
Concluding / none
• Step 2 · Feedback priority: 3-class classification
In: segment text + role from Step 1 + position
Out: Ineffective / Adequate / Effective
• Step 3 · Essay level: regression on 1–6
In: ~45 rubric features (structure from Steps 1–2)
Out: suggested level 1–6 + uncertainty
• Subjective: raters agree moderately on effectiveness (κ = 0.32), strongly
on score (weighted κ = 0.75)
• Imbalanced: Adequate 79%, Ineffective 4.5%; 11× more Claims than
Rebuttals
Two training examples, same prompt
Weak Strong
Essay 279E6B94B3C4 · 249
words
65B987E219BE · ~670
words
Sentence “ADD is a big reason too
for people have no choice
but to get distracted on
things which cause
crashes.”
“Cell phones are
extremely distracting
because of the large
amount of focus
operating one requires.”
Step 1 · role Claim Claim
Step 2 · priority Ineffective Effective
Step 3 · level 3 5
4. Model plan
5 / 8
Logistic Regression → Steps 1, 2
• Strong and fast on sparse TF-IDF text
• Readable weights show which words flagged a segment
• Balanced class weights for Rebuttal, Ineffective
Random Forest, Gradient Boosting → Step 3
• Scores 4–6 need every criterion strong: a threshold, not a line
• Feature importance shows which criterion pulls the level down
• Uncertainty = spread of predictions across trees
Why trees: essays with a Counterclaim
Score 2 Score 3 Score 4 Score 5 Score 6
19%
26% 26%
42%
85%
Independent prompts, train set. Jump from 26% to 85% suits tree models.
5. Evaluation plan
6 / 8
Split and baselines
• Essay-level split: No essay overlap between sets.
• Prompt-level split: Hold out one prompt at a time.
• Training set: 15,594 essays; 10,669 remaining after excluding
five prompts.
• Official test set (10,402) used once, at the end; 6,456 essays after
excluding source-based prompts
• Steps 1–2 baseline: majority class; LR on position + length
• Step 3 baseline M0: word count only (r = 0.76 with score)
• Step 3 baseline M1: linguistic features (Yang et al., 2024)
Metrics
• Steps 1–2: macro-F1, recall on Ineffective
• Step 3: QWK, MAE
• Fairness by ELL status: CSD, MAED
• Ceiling: human agreement, weighted κ = 0.75
Why accuracy is not enough
Always predicting "Adequate" is 79% accurate yet finds no
weak segment. Predicting 3 for a true 4 is not as bad as
predicting 1.
6. Risks and responsible use
7 / 8
What could go wrong
• Length shortcut: word count r = 0.76 with score → test by
duplicating paragraphs, stuffing connectives
• Unfair to ELL learners: mean 3.08 vs 3.73 → compare at the
same true score
• Noisy labels: κ = 0.32 on effectiveness → a flag is a suggestion,
not a verdict
• Different population: US grades 6–12 → no IELTS conversion,
no high-stakes use
What stays human
• The teacher assigns the final grade
• The teacher can override any suggestion
• Learners see a diagnosis only after approval
• Every suggestion shows its confidence
• Demographics are never a model input
7. Contribution and next steps
8 / 8
Gap and research questions
• Yang et al. (2024), Unveiling the Tapestry of Automated Essay Scoring,
AAAI: accuracy and fairness on unseen prompts, but no argument structure
• Wang et al. (2026), ArguLens, arXiv: argument structure, but gold labels
only, no subgroup analysis
• Chen, Wu & Zhang (2026), Assessing Fairness in AI-Assisted Writing
Scoring, Assessing Writing: fairness conditioned on proficiency, but one
prompt, no ELL status
• RQ1: how much does structure help on unseen prompts?
• RQ2: how much is lost with predicted instead of gold structure?
• RQ3: does structure increase or reduce bias against ELL learners?
Four versions of the Step-3 model
Input Role
M0 Word count only Minimum baseline
M1 Linguistic features Reproduces Yang et al.
M2 M1 + gold structure Upper bound
M3 M1 + predicted structure Our system
Same algorithm, same prompt-based split: only the inputs differ.
First step: build M0 and M1 with the prompt-based split