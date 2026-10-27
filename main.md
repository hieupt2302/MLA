Contents lists available at ScienceDirect [URL 🔗](www.sciencedirect.com/science/journal/10752935)

## Assessing Writing

journal homepage: www.elsevier.com/locate/asw [URL 🔗](https://www.elsevier.com/locate/asw)

## A large-scale corpus for assessing written argumentation: PERSUADE 2.0

S.A. Crossley a,*, Y. Tian b, P. Baffour c, A. Franklin c, M. Benner c, U. Boser c [URL 🔗](#page-0)

## ARTICLE INFO

Keywords: Corpus linguistics Writing assessment Argumentation

Individual differences

## ABSTRACT

This research methods article introduces the open source PERSUADE 2.0 corpus. The PERSUADE 2.0 corpus comprises over 25,000 argumentative essays produced by 6th-12th grade students in the United States for 15 prompts on two writing tasks: independent and source-based writing. The PERSUADE 2.0 corpus also provides detailed individual and demographic information for each writer. The goal of the PERSUADE 2.0 corpus is to advance research into relationships between discourse elements, their effectiveness, writing quality, writing tasks and prompts, and de­ mographic and individual differences.

## 1. Introduction

Argumentation is a logical appeal that involves stating claims and offering support to justify or refute beliefs to influence others (Newell, Beach, Smith & VanDerHeide, 2011). The ability to persuade with good argumentation skills lies at the core of critical thinking and has long been valued in personal, professional, and academic contexts. Given the important role of argumentation in students’ cognitive development and academic learning, the K-12 Common Core State Standards (CCCS, 2010) were developed in the United States to highlight the cultivation of argumentation skills in writing instruction. The CCCS for argumentative writing stipulate that students should be able to introduce claims, distinguish the claims from alternative claims, and organize the claims logically. Additionally, students should be able to support claims and counterclaims with logical reasoning and accurate data and evidence. However, many students in the United States still struggle to construct effective arguments in writing due to the cognitively demanding nature of argumentation. According to the 2012 National Assessment of Educational Progress (NAEP) Writing Report Card, a na­ tionally representative and continuing assessment of America’s students’ knowledge, only about 25 % of students’ argumentative essays were scored as competent. [URL 🔗](#page-0)

To better understand student difficulties in argumentation, it is necessary to systematically analyze argument production in writing samples. One way to do this is through large-scale corpus analyses wherein a collection of student essays is annotated for argumen­ tation, argumentation effectiveness, and overall writing quality. Quantitative analyses can then be conducted to better understand links between the production of argumentative elements, the effectiveness of these elements, and ratings of quality. These analyses can provide information on argument construction and efficacy that inform classroom practices. Additionally, computational modeling of argumentation and argumentative quality may provide opportunities for learning platforms to provide students with granular

[https://doi.org/10.1016/j.asw.2024.100865](https://doi.org/10.1016/j.asw.2024.100865)

Received 14 July 2023; Received in revised form 28 May 2024; Accepted 30 May 2024

Available online 26 June 2024

1075-2935/© 2024 The Author(s). Published by Elsevier Inc. This is an open access article under the CC BY-NC license (http://creativecommons.org/licenses/by-nc/4.0/). [URL 🔗](http://creativecommons.org/licenses/by-nc/4.0/)


feedback on writing quality which in turn could lead to more deliberative practice and writing development.

This paper introduces a corpus that can help address research and pedagogical interventions in student argumentation: the Persuasive Essays for Rating, Selecting, and Understanding Argumentative and Discourse Elements (PERSUADE) corpus 2.0. PERSUADE 2.0 builds on the PERSUADE 1.0 corpus (Crossley et al., 2022), which comprises over 25,000 persuasive essays (both independent and dependent essays) annotated for discourse elements (e.g., position, claims, and evidence) as well as hierarchical relationships between these elements. The PERSUADE 1.0 corpus also includes detailed demographic information for the writers.

The PERSUADE 2.0 corpus provides holistic essay scores for each persuasive essay as well as effectiveness scores for each discourse element found in the PERSUADE 1.0 corpus. Like PERSUADE 1.0, PERSUADE 2.0 is open source.1 The purpose of the PERSUADE 2.0 corpus is to provide a tool to increase knowledge of persuasive writing within the research community and to advance the development of unbiased computational algorithms that can predict overall writing quality and discourse element quality. The knowledge gleaned from the corpus will help researchers and practitioners develop classroom interventions to promote proficient writing skills. Algo­ rithms developed from the corpus could inform automated writing evaluation (AWE) systems to better assess student writing samples, provide more focused feedback, and promote better revising practices. The corpus is discussed in depth below. [URL 🔗](#page-0)

## 2. PERSUADE 2.0 corpus

The PERSUADE corpus 2.0 corpus is an augmented version of the PERSUADE corpus 1.0, which comprises source-based essays (n 12,875) and independent essays (n 13,121). The source-based essays were written on seven different writing prompts and each prompt had a single source. Writers were sampled from 6th to 10th grades. The source-based essays were written on eight different writing prompts sampled from writers from the 8th to 12th grade.

The essays included in the PERSUADE 1.0 corpus reflect the diversity of the student body found in the United States. Each essay is linked to the writers’ gender and race/ethnicity with the majority of the writers identifying as White (45 %) followed by Hispanic (25 %) and Black (19 %). Most of the essays (n 20,759) are also linked to student eligibility for federal assistance programs that help identify students with economic disadvantages. The PERSUADE 1.0 essay contains annotations for discourse elements and includes relationships between the elements. Discourse elements include leads, positions, claims, counterclaims, rebuttals, evidence and concluding summaries. All annotations were provided by expert raters based on a standardized rubric developed to identify common

discourse elements similar to those found in Toulmin’s argumentative framework (1958). corpus is reported in Crossley et al., 2022. [URL 🔗](#page-0)

The PERSUADE corpus 2.0 includes the same data as the PERSUADE corpus 1.0, but it also includes effectiveness scores for the individual discourse elements along with holistic scores for the overall quality of each essay.

More information about the PERSUADE 1.0

## 2.1. Effectiveness scores for discourse elements

An outside consulting firm that specializes in educational data hired all raters and completed all effectiveness ratings. All ratings were conducted on a third-party annotation platform. Raters were trained on a standardized rubric2 and were asked to score each element as effective, adequate, or ineffective. An effective score indicated that the writer successfully fulfilled the rhetorical or argumentative function of the element. Adequate indicated that the writer sufficiently fulfilled the function of the element while ineffective indicated that the writer did not successfully fulfill the function of the element. A description was given for each category along with an example of a discourse element that fit that categorical score. The expert raters used a double-blind rating process and raters were trained by prompt. Raters were trained on independent essays first followed by source-based essays. After training, raters independently annotated essays for the discourse elements reported in the PERSUADE 1.0 corpus. They then provided effectiveness scores for each element. [URL 🔗](#page-0)

Inter-rater reliability (IRR) is difficult to calculate for the effectiveness because raters segmented essays into discourse elements before scoring those elements for effectiveness. In many cases, the segmented elements between two raters do not overlap perfectly, making alignment of annotations and effectiveness scores difficult. To calculate IRR, we examined segments where the first and second rater had at least 50 % overlap in the discourse elements they annotated. Within the essays, there were 159,228 elements that had at least 50 % overlap. Of these, the raters scored ~120,000 segments as adequate, ~32,000 as effective, and ~6000 as ineffective. Two statistics were calculated: exact agreement and a weighted Cohen’s Kappa. Exact agreement for all classes was.718. For specific classes, exact agreement was between.68 and.81. Exact agreement was generally higher in dependent essays as compared to independent essays. Cohen’s Kappa was quite low for the quality ratings reporting κ between.17 and.38 for specific classes. In general, Cohen’s Kappa was higher in dependent essays in comparison to independent essays. The overall Cohen’s Kappa for all classes was κ .316, indicating fair agreement. In the events of effectiveness rating difference, a third, expert rater served as the adjudicator to make a final decision. All IRR statistics are reported in Table 1. [URL 🔗](#page-0)

## 2.2. Holistic writing quality scores

The same raters that annotated the discourse elements for the essays and scored each element for effectiveness also scored each


*Table 1 IRR statistics for PERSUADE effectiveness ratings.*

| Discourse Element Exact Overlap Exact Overlap Exact Overlap Cohen’s κ Cohen’s κ Cohen’s κ All Independent Dependent All Independent Dependent |
| --- |
| Lead 0.725 0.710 0.744 0.378 0.385 0.353 Position 0.807 0.809 0.804 0.274 0.241 0.303 Claim 0.677 0.674 0.682 0.165 0.144 0.191 Counterclaim 0.679 0.677 0.682 0.188 0.17 0.204 Rebuttal 0.676 0.663 0.701 0.256 0.23 0.281 Evidence 0.731 0.716 0.749 0.432 0.403 0.405 Concluding 0.738 0.729 0.747 0.370 0.359 0.375 Statement |

essay holistically. For the independent essays, raters were trained on a standardized SAT holistic essay scoring rubric. The rubric used a 1 to 6 scale that has interval levels (i.e., the raters were told that the distance between each grade was equal). A score of 6 indicates an essay that shows clear and consistent mastery of writing. The same SAT rubric was slightly modified for the source-based essays. The main difference was the inclusion of evidence taken from the source as a criterion for writing quality.3 To illustrate, the wording for an essay scored 6 from the independent rubric states “A typical essay… (uses) clearly appropriate examples, reasons, and other evidence to support its position.” For the dependent rubric, this wording was modified to state “A typical essay… uses clearly appropriate examples, reasons, and other evidence taken from the source text(s) to support its position.” The two rubrics were matched as closely as possible to ensure that independent and source-based essays were comparable. Like the effectiveness rating, expert raters used a double-blind rating process followed by 100 % adjudication such that each essay was scored holistically by two raters and adjudicated by a third rater if necessary. Raters were trained by prompt and essay type (independent essays were scored first followed by source- based essays). Inter-rater reliability before adjudication indicated strong agreement between the expert raters (weighted κ .745, r .750). [URL 🔗](#page-0)

## 3. Possible futures

Around 80 % of the PERSUADE 2.0 corpus was released in a Kaggle competition in late 2022.4 However, Kaggle competitors had no access to the holistic quality scores or the demographic and individual difference scores. The competition asked data scientists to develop models to assign effectiveness ratings to annotated discourse elements. The competition used a subset of the PERSUADE corpus (around 6900 out of the 26,000 essays, or a little over one quarter). Essays were selected to ensure a balance across effectiveness by discourse element. Feedback 2.0 prioritized computationally efficient algorithms that were simple and fast, but still achieved high accuracy because complex models can negatively impact the environment through energy consumption. Additionally complex models are less suitable for use in real-world applications. Over 1500 teams and almost 2000 competitors participated in this challenge, generating nearly 30,000 submissions. Winning models were able to predict human judgments of discourse effectiveness at between ~30 % and ~90 % accuracy. Accuracy was lowest for ineffective discourse elements which were often predicted to be adequate. Accuracy was highest for effective discourse elements (see Fig. 1). [URL 🔗](#page-0)

While the entire corpus was not made available in the Kaggle competition, the entire PERSUADE 2.0 corpus has been made available for researchers including data for demographic information, individual differences, and holistic writing quality. Our hope is that the PERSUADE 2.0 corpus will help advance research into relationships between argumentative and discourse elements, their effectiveness, writing quality, writing tasks and prompts, and demographic and individual differences. The size of the data along with the reliability of human annotations should ensure that research findings derived from the data will forward our knowledge of the writing product and how the written product interacts with a myriad of textual and non-textual features.

It is important to note that the PERSUADE 2.0 corpus is the first large-scale corpus to identify discourse elements in student writing in English. More importantly, these elements are scored for effectiveness. Research capitalizing on the PERSUADE 2.0 corpus should lead to more valid writing assessment over time. In terms of construct validity, we have confidence that the data contained in PERSUADE accurately represents written argumentation including annotations for argument elements, relationships among those elements, and the quality of those elements. Thus, we have some certainty that the labels in the PERSUADE corpus can be used to measure the construct of written argumentation. The PERSUADE corpus likely does not represent all aspects of written argumentation, and thus may have lower content validity. Additionally, models derived from the PERSUADE corpus that annotate discourse elements and their quality can be validated based on how well they predict overall essay quality using the holistic scores provided. The models can also be extended to other available corpora of scored essays to assess how well predicted discourse elements and their quality are related to holistic scores, providing additional validation checks.

The ability to assess the validity of models developed using the PERSUADE corpus should help develop more reliable and repre­ sentative writing interventions. For instance, models developed in the Kaggle competition can be validated internally and externally. Once validated, the models can be integrated into automatic writing evaluation (AWE) systems to help provide meaningful feedback


*Fig. 1. Accuracy of winning algorithm to predict discourse effectiveness.*

for students at the discourse level. Primarily, the algorithms can assist students in identifying the presence or absence of important

of

argumentative elements such as the use of positions, claims, and evidence and, if present, the likely effectiveness of those elements. Of

secondary importance, the holistic scores can be used in AWE systems to provide summative feedback to learners about the overall quality of their writing.

The PERSUADE 2.0 corpus also provides important research possibilities. Immediately, the corpus can be used to compare dif­ ferences in independent and dependent writing not only in terms of holistic scores, but also with respect to the types of argumentation that each writing task produces. Additionally, research could be carried out to examine differences in the linguistic features produced within each task. Such studies have been carried out on non-native writers of English (Guo, Crossley, & McNamara, 2013; Tywoniw & Crossley, 2019), but not with native writers. [URL 🔗](#page-0)

The demographic and individual difference measures in the PERSUADE 2.0 corpus also allow for research that examines how these

the

non-language features co-vary with assessment of discourse element quality and overall holistic scores of quality. Importantly, the

demographic and individual difference measures can be used to assess whether models and algorithms derived from the corpus suffer from bias. Initial analysis of the winning models from the Kaggle competition based on predicting discourse element effectiveness indicate some bias in terms of race/ethnicity, economic status, and English Language Learner (ELL) status (Baffour, Saxberg, & Crossley, in press). Newly developed models can be developed specifically to avoid bias in output. [URL 🔗](#page-0)

## 4. Connections

There are a few available corpora that focus on annotating argumentation in persuasive writing, but none are annotated for

discourse features like leads or concluding summaries. More importantly, there are no corpora available that provide effectiveness scores for discourse elements. While there are some available corpora that provide holistic scores for essay quality, the corpora are

for


problematic in terms of overlap in task, prompts, scoring mechanisms and none, to our knowledge, include student meta-data (see the ASAP corpus, Shermis, 2014). While some existing corpora provide annotations for discourse elements, the corpora are relatively small, are annotated for only a few discourse features, do not provide effectiveness scores for those features, and do not contain meta-data for the student writers (Stab and Gurevych, 2014, 2017). [URL 🔗](#page-0)

## 5. Limitations

The PERSUADE 2.0 corpus is the largest writing dataset in terms of size, types of annotations, and available meta-data. However, there are still limitations. For example, the corpus only focuses on 6–12th grade writers. Thus, intelligence gleaned from the corpus may not generalize to younger writers that are just developing proficiency in writing skills and to older, more proficient writers. The corpus also has a limited number of prompts (N 15) and only focuses on independent and integrated writing tasks. The corpus could be augmented in the future by including essays from a greater number of prompts and a greater variety of writing tasks including compare and contrast essays, analysis papers, and research reports. Lastly, inter-rater reliability for parts of the corpus was difficult to calculate because of segmentation differences among annotators and the difficulty in labeling discourse elements. This speaks to the general difficulty in annotating discourse elements in student writing because boundaries between the start and end of elements are nebulous and many discourse elements (e.g., positions, claims, and counterclaims) share similar semantics. These aspects of discourse make agreement for human raters difficult to obtain and may impact validity and fairness when modeling the data. Low reliability in the human ratings may transfer into automatic writing evaluation systems developed using the PERSUADE 2.0 corpus, potentially leading to bias or validity concerns in the feedback such systems provide. Initial analyses suggest some bias in the models developed from the Kaggle competition indicating the need for newer models that more strongly address these concerns. It will be of paramount importance to ensure that the next generation of models developed on the PERSUADE 2.0 corpus mitigate bias and support fairness. The inclusion of demographic and individual difference measures in PERSUADE 2.0 make this more feasible.

## Data availability

Data is available at

[https://github.com/scrosseye/persuade_corpus_2.0.](https://github.com/scrosseye/persuade_corpus_2.0)

## References

Baffour, P., Saxberg, T.,

Prize Competition Series. In Proceedings of the 2023 BEA 18th Workshop on Innovative Use of NLP for Building Educational Applications.

Common Core State Standards Initiative (2010). Common core state standards for English language arts & literacy in history/social studies, science, and technical subjects.

Retrieved from 〈http://www.corestandards.org〉. [URL 🔗](http://www.corestandards.org)

Guo, L., Crossley, S. A., & McNamara, D. S. (2013). Predicting human judgments of essay quality in both integrated and independent second language writing samples: A comparison study. Assessing Writing, 18(3), 218–238. [URL 🔗](http://refhub.elsevier.com/S1075-2935(24)00058-8/sbref1)

National Center for Education Statistics (ED). (2013). The Nation’s Report Card: Trends in Academic Progress 2012. NCES 2013-456. ERIC Clearinghouse. [URL 🔗](http://refhub.elsevier.com/S1075-2935(24)00058-8/sbref1)

[Newell, G. E., Beach, R., Smith, J., & VanDerHeide, J. (2011). Teaching and learning argumentative reading and writing: A review of research. Reading Research](http://refhub.elsevier.com/S1075-2935(24)00058-8/sbref2)

[Quarterly,](http://refhub.elsevier.com/S1075-2935(24)00058-8/sbref2)

Shermis, M. D. (2014). State-of-the-art automated essay scoring: Competition, results, and future directions from a United States demonstration. Assessing Writing, 20, 53–76. [URL 🔗](http://refhub.elsevier.com/S1075-2935(24)00058-8/sbref3)

Stab, C. & Gurevych, I. (2014), October. Identifying argumentative discourse structures in persuasive essays. In Proceedings of the 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP) (pp. 46–56).

[Stab, C., & Gurevych, I. (2017). Parsing argumentation structures in persuasive essays. Computational Linguistics, 43(3), 619–659.](http://refhub.elsevier.com/S1075-2935(24)00058-8/sbref4)

[Toulmin, S. (1958). The uses of argument. Cambridge: Cambridge University Press,.](http://refhub.elsevier.com/S1075-2935(24)00058-8/sbref5)

Tywoniw, R., & Crossley, S. A. (2019). The effect of cohesive features in integrated and independent L2 writing quality and text classification. Language Education & Assessment, 2(3), 90–103. [URL 🔗](http://refhub.elsevier.com/S1075-2935(24)00058-8/sbref6)

Scott Crossley is a professor of Special Education at Vanderbilt University. His primary research focus is on natural language processing and the application of computational tools and machine learning algorithms in language learning, writing, and text comprehensibility.His main interest area is the development and use of natural language processing tools in assessing writing quality and text difficulty.

&

Crossley, S. (in press). Analyzing Bias in Large Language Model Solutions for Assisted Writing Feedback Tools: Lessons from the Feedback

[46(3), 273–304.](http://refhub.elsevier.com/S1075-2935(24)00058-8/sbref2)
