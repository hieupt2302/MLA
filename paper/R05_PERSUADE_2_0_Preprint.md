

## 1
Title: A large-scale corpus for assessing written argumentation: PERSUADE 2.0
Authors: Crossley, S. A, Baffour, P., Tian, Y., Franklin, A., Benner, M., & Boser., U.

Abstract: This research methods article introduces the open source PERSUADE 2.0 corpus. The
PERSUADE 2.0 corpus comprises over 25,000 argumentative essays produced by 6
th
## -12
th
grade
students in the United States for 15 prompts on two writing tasks: independent and source-based
writing. The PERSUADE 2.0 corpus also provides detailed individual and demographic
information for each writer. The goal of the PERSUADE 2.0 corpus is to advance research into
relationships between discourse elements, their effectiveness, writing quality, writing tasks and
prompts, and demographic and individual differences.



## 2

## Introduction
Argumentation is a logical appeal that involves stating claims and offering support to justify or
refute beliefs to influence others (Newell et al., 2011). The ability to persuade with good
argumentation skills lies at the core of critical thinking and has long been valued in personal,
professional, and academic contexts. Given the important role of argumentation in students’
cognitive development and academic learning, the K-12 Common Core State Standards (2010)
highlights the cultivation of argumentation skills in writing instruction and stipulates that
students need to achieve proficiency in using valid reasoning and relevant and sufficient
evidence to support claims. However, many students in the U.S. struggle to construct effective
arguments in writing due to the cognitively demanding nature of argumentation. According to
the 2012 National Assessment of Educational Progress (NAEP) Writing Report Card, only about
25% of students' argumentative essays were competent.
To better understand student difficulties in argumentation, it is necessary to
systematically analyze argument production in writing samples. One way to do this is through
large-scale corpus analyses wherein a collection of student essays are annotated for
argumentation, argumentation effectiveness, and overall writing quality. Quantitative analyses
can then be conducted to better understand links between the production of argumentative
elements, the effectiveness of these elements, and ratings of quality. These analyses can provide
information on argument construction and efficacy that inform classroom practices. Additionally,
computational modeling of argumentation and argumentative quality may provide opportunities
for learning platforms to provide students with granular feedback on writing quality which in
turn could lead to more deliberative practice and writing development.

## 3
This paper introduces a corpus that can help address research and pedagogical
interventions in student argumentation: the Persuasive Essays for Rating, Selecting, and
Understanding Argumentative and Discourse Elements (PERSUADE) corpus 2.0. PERSUADE
2.0 builds on the PERSUADE 1.0 corpus (Crossley et al., 2022), which comprises over 25,000
persuasive essays (both independent and dependent essays) annotated for discourse elements
(e.g., position, claims, and evidence) as well as hierarchical relationships between these
elements. The PERSUADE 1.0 corpus also includes detailed demographic information for the
writers.
The PERSUADE 2.0 corpus provides holistic essay scores for each persuasive essay as
well as effectiveness scores for each discourse element found in the PERSUADE 1.0 corpus.
Like PERSUADE 1.0, PERSUADE 2.0 is open source and freely available.
## 1
The purpose of the
PERSUADE 2.0 corpus is to provide a tool to increase knowledge of persuasive writing within
the research community and to advance the development of unbiased computational algorithms
that can predict overall writing quality and discourse element quality. The knowledge gleaned
from the corpus will help researchers and practitioners develop classroom interventions to
promote proficient writing skills. Algorithms developed from the corpus could inform automated
writing evaluation (AWE) systems to better assess student writing samples, provide more
focused feedback, and promote better revising practices. The corpus is discussed in depth below.
PERSUADE 2.0 Corpus
The PERSUADE corpus 2.0 corpus is an augmented version of the PERSUADE corpus 1.0,
which comprises source-based essays (n =12,875) and independent essays (n =13,121). The

## 1
The PERSUADE 2.0 dataset is available at https://anonymous.4open.science/r/persuade_corpus_2-
3329/README.md

## 4
source-based essays were written on seven different writing prompts and each prompt had a
single source. Writers were sampled from 6
th
to 10
th
grades. The source-based essays were
written on eight different writing prompts sampled from writers from the 8
th
to 12
th
grade.
The essays included in the PERSUADE 1.0 corpus reflect the diversity of the student
body found in the United States. Each essay is linked to the writers’ gender and race/ethnicity
with the majority of the writers identifying as White (45%) followed by Hispanic (25%) and
Black (19%). Most of the essays (n = 20,759) are also linked to student eligibility for federal
assistance programs that help identify students with economic disadvantages. The PERSUADE
1.0 essay contains annotations for discourse elements and includes relationships between the
elements. Discourse elements include leads, positions, claims, counterclaims, rebuttals, evidence
and concluding summaries. All annotations were provided by expert raters based on a
standardized rubric developed to identify common discourse elements similar to those found in
Toulmin’s argumentative framework (1958). More information about the PERSUADE 1.0
corpus is reported in Crossley et al., 2022.
The PERSUADE corpus 2.0 includes the same data as the PERSUADE corpus 1.0, but it
also includes effectiveness scores for the individual discourse elements along with holistic scores
for the overall quality of each essay.
Effectiveness scores for discourse elements. An outside consulting firm that specializes in
educational data hired all raters and completed all effectiveness ratings. All ratings were
conducted on a third-party annotation platform. Raters were trained on a standardized rubric
## 2
and
were asked to score each element as effective, adequate, or ineffective. A description was given
for each category along with an example of a discourse element that fit that categorical score.

## 2
See https://anonymous.4open.science/r/persuade_corpus_2-3329/README.md for rubrics.

## 5
The expert raters used a double-blind rating process and raters were trained by prompt. Raters
were trained on independent essays first followed by source-based essays. After training, raters
independently annotated essays for the discourse elements reported in the PERSUADE 1.0
corpus. They then provided effectiveness scores for each element.
Inter-rater reliability (IRR) is difficult to calculate for the effectiveness because raters
segmented essays into discourse elements before scoring those elements for effectiveness. In
many cases, the segmented elements between two raters do not overlap perfectly, making
alignment of annotations and effectiveness scores difficult. To calculate IRR, we examined
segments where the first and second rater had at least 50% overlap in the discourse elements they
annotated. Within the essays, there were 159,228 elements that had at least 50% overlap. Of
these, the raters scored ~120,000 segments as adequate, ~32,000 as effective, and ~6,000 as
ineffective. Two statistics were calculated: exact agreement and a weighted Cohen’s Kappa.
Exact agreement for all classes was .718. For specific classes, exact agreement was between .68
and .81. Exact agreement was generally higher in dependent essays as compared to independent
essays. Cohen’s Kappa was quite low for the quality ratings reporting κ between .17 and .38 for
specific classes. In general, Cohen's Kappa was higher in dependent essays in comparison to
independent essays. The overall Cohen’s Kappa for all classes was κ = .316, indicating fair
agreement. In the events of effectiveness rating difference, a third, expert rater served as the
adjudicator to make a final decision. All IRR statistics are reported in Table 1.
[Insert Table 1 here]
Holistic writing quality scores. The same raters that annotated the discourse elements for the
essays and scored each element for effectiveness also scored each essay holistically. For the
independent essays, raters were trained on a standardized SAT holistic essay scoring rubric. The

## 6
rubric used a 1 to 6 scale that has interval levels (i.e., the raters were told that the distance
between each grade was equal). A score of 6 indicates an essay that shows clear and consistent
mastery of writing. The same SAT rubric was slightly modified for the source-based essays. The
main difference was the inclusion of evidence taken from the source as a criterion for writing
quality
## 3
. To illustrate, the wording for an essay scored 6 from the independent rubric states “A
typical essay... (uses) clearly appropriate examples, reasons, and other evidence to support its
position.” For the dependent rubric, this wording was modified to state “A typical essay... uses
clearly appropriate examples, reasons, and other evidence taken from the source text(s) to
support its position.” The two rubrics were matched as closely as possible to ensure that
independent and source-based essays were comparable. Like the effectiveness rating, expert
raters used a double-blind rating process followed by 100 percent adjudication such that each
essay was scored holistically by two raters and adjudicated by a third rater if necessary. Raters
were trained by prompt and essay type (independent essays were scored first followed by source-
based essays). Inter-rater reliability before adjudication indicated strong agreement between the
expert raters (weighted κ = .745, r = .750).
## Possible Futures
Around 80% of the PERSUADE 2.0 corpus was released in a Kaggle competition in late 2022
## 4
## .
The competition asked data scientists to develop models to assign effectiveness ratings to
annotated discourse elements. The competition used a subset of the PERSUADE corpus (around
6,900 out of the 26,000 essays, or a little over one quarter). Essays were selected to ensure a
balance across effectiveness by discourse element. Feedback 2.0 prioritized computationally

## 3
See https://anonymous.4open.science/r/persuade_corpus_2-3329/README.md for the independent and dependent
scoring rubrics.
## 4
See https://www.kaggle.com/competitions/feedback-prize-effectiveness for competition details.

## 7
efficient algorithms that were simple and fast, but still achieved high accuracy because complex
models can negatively impact the environment through energy consumption. Additionally
complex models are less suitable for use in real-world applications. Over 1,500 teams and almost
2,000 competitors participated in this challenge, generating nearly 30,000 submissions. Winning
models were able to predict human judgments of discourse effectiveness at between ~.30% and
~90% accuracy. Accuracy was lowest for ineffective discourse elements which were often
predicted to be adequate. Accuracy was highest for effective discourse elements (see Figure 1)
While the entire corpus was not made available in the Kaggle competition, the entire
PERSUADE 2.0 corpus is now available including data for demographic information, individual
differences, and holistic writing quality. Our hope is that the open-source nature of the
PERSUADE 2.0 corpus will help advance research into relationships between argumentative and
discourse elements, their effectiveness, writing quality, writing tasks and prompts, and
demographic and individual differences. The size of the data along with the reliability of human
annotations should ensure that research findings derived from the data will forward our
knowledge of the writing product and how the written product interacts with a myriad of textual
and non-textual features.
It is important to note that the PERSUADE 2.0 corpus is the first large-scale corpus to
identify discourse elements in student writing in English. More importantly, these elements are
scored for effectiveness. The algorithms developed from the Kaggle competition can be
integrated into automatic writing evaluation (AWE) systems to help provide meaningful
feedback for students at the discourse level. Primarily, the algorithms can assist students in
identifying the presence or absence of important argumentative elements such as the use of
positions, claims, and evidence and, if present, the likely effectiveness of those elements. Of

## 8
secondary importance, the holistic scores can be used in AWE systems to provide summative
feedback to learners about the overall quality of their writing.
The PERSUADE 2.0 corpus also provides important research possibilities. Immediately,
the corpus can be used to compare differences in independent and dependent writing not only in
terms of holistic scores, but also with respect to the types of argumentation that each writing task
produces. Additionally, research could be carried out to examine differences in the linguistic
features produced within each task. Such studies have been carried out on non-native writers of
English (Guo, Crossley, & McNamara, 2013; Tywoniw & Crossley, 2019), but not with native
writers.
The demographic and individual difference measures in the PERSUADE 2.0 corpus also
allow for research that examines how these non-language features co-vary with assessment of
discourse element quality and overall holistic scores of quality. Importantly, the demographic
and individual difference measures can be used to assess whether models and algorithms derived
from the corpus suffer from bias. Initial analysis of the winning models from the Kaggle
competition based on predicting discourse element effectiveness indicate some bias in terms of
race/ethnicity, economic status, and English Language Learner (ELL) status (Baffour, Saxberg,
& Crossley, in press). Newly developed models can be developed specifically to avoid bias in
output.
## Connections
There are a few available corpora that focus on annotating argumentation in persuasive writing,
but none are annotated for discourse features like leads or concluding summaries. More
importantly, there are no corpora available that provide effectiveness scores for discourse
elements. While there are some available corpora that provide holistic scores for essay quality,

## 9
the corpora are problematic in terms of overlap in task, prompts, scoring mechanisms and none,
to our knowledge, include student meta-data (see the ASAP corpus, Shermis, 2014). While some
existing corpora provide annotations for discourse elements, the corpora are relatively small, are
annotated for only a few discourse features, do not provide effectiveness scores for those
features, and do not contain meta-data for the student writers (Stab and Gurevych, 2014; 2017).
## Limitations
The PERSUADE 2.0 corpus is the largest writing dataset in terms of size, types of annotations,
and available meta-data. However, there are still limitations. For example, the corpus only
focuses on 6-12
th
grade writers. Thus, intelligence gleaned from the corpus may not generalize to
younger writers that are just developing proficiency in writing skills and to older, more proficient
writers. The corpus also has a limited number of prompts (N = 15) and only focuses on
independent and integrated writing tasks. The corpus could be augmented in the future by
including essays from a greater number of prompts and a greater variety of writing tasks
including compare and contrast essays, analysis papers, and research reports.





## 10
## References
Baffour, P., Saxberg, T., & Crossley, S. (in press). Analyzing Bias in Large Language Model
Solutions for Assisted Writing Feedback Tools: Lessons from the Feedback Prize
Competition Series. In Proceedings of the 2023 BEA 18th Workshop on Innovative Use of
NLP for Building Educational Applications.
Common Core State Standards Initiative (2010). Common core state standards for English
language arts & literacy in history/social studies, science, and technical subjects.
Retrieved from http://www.corestan dards.org
Guo, L., Crossley, S. A., & McNamara, D. S. (2013). Predicting human judgments of essay
quality in both integrated and independent second language writing samples: A
comparison study. Assessing Writing, 18 (3), 218-238.
National Center for Education Statistics (2012). The Nation’s Report Card: Writing.
Washington, DC: NCES, Institute of Education Sciences, U.S. Department of Education.
Newell, G. E., Beach, R., Smith, J., & VanDerHeide, J., (2011). Teaching and learning
argumentative reading and writing: A review of research. Reading Research Quarterly,
## 46(3), 273-304.
Shermis, M.D. (2014). State-of-the-art automated essay scoring: Competition, results, and future
directions from a United States demonstration. Assessing Writing, 20, 53-76.
Stab, C. & Gurevych, I. (2014), October. Identifying argumentative discourse structures in
persuasive essays. In Proceedings of the 2014 Conference on Empirical Methods in
Natural Language Processing (EMNLP) (pp. 46-56).
Stab, C., & Gurevych, I., (2017). Parsing argumentation structures in persuasive essays.
## Computational Linguistics, 43(3), 619-659.

## 11
Toulmin, S. (1958). The uses of argument. Cambridge: Cambridge University Press.
Tywoniw, R., & Crossley, S. A. (2019). The effect of cohesive features in integrated and
independent L2 writing quality and text classification. Language Education &
## Assessment, 2 (3), 90-103.


## 1
## Table 1
IRR statistics for PERSUADE effectiveness ratings
## Discourse Element
## Exact Overlap
## All
## Exact Overlap
## Independent
## Exact Overlap
## Dependent
Cohen's κ
## All
Cohen's κ
## Independent
Cohen's κ
## Dependent
## Lead 0.725 0.710 0.744 0.378 0.385 0.353
## Position 0.807 0.809 0.804 0.274 0.241 0.303
## Claim 0.677 0.674 0.682 0.165 0.144 0.191
## Counterclaim 0.679 0.677 0.682 0.188 0.17 0.204
## Rebuttal 0.676 0.663 0.701 0.256 0.23 0.281
## Evidence 0.731 0.716 0.749 0.432 0.403 0.405
## Concluding Statement 0.738 0.729 0.747 0.370 0.359 0.375


## 1


Figure 1: Accuracy of winning algorithm to predict discourse effectiveness




