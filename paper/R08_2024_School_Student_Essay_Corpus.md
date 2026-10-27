

Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics:
Human Language Technologies (Volume 1: Long Papers), pages 2661–2674
June 16-21, 2024 ©2024 Association for Computational Linguistics
A School Student Essay Corpus for
Analyzing Interactions of Argumentative Structure and Quality
## Maja Stahl
## 1
## , Nadine Michel
## 2
## , Sebastian Kilsbach
## 2
## ,
## Julian Schmidtke
## 1
## , Sara Rezat
## 2
, and Henning Wachsmuth
## 1
## 1
Leibniz University Hannover, Institute of Artificial Intelligence
## 2
Paderborn University, Institute for German Language and Comparative Literature
{m.stahl,h.wachsmuth}@ai.uni-hannover.de, julian.schmidtke@stud.uni-hannover.de
{nadine.michel, sebastian.kilsbach, sara.rezat}@uni-paderborn.de
## Abstract
Learning argumentative writing is challenging.
Besides writing fundamentals such as syntax
and grammar, learners must select and arrange
argument components meaningfully to create
high-quality essays. To support argumentative
writing computationally, one step is to mine the
argumentative structure. When combined with
automatic essay scoring, interactions of the ar-
gumentative structure and quality scores can be
exploited for comprehensive writing support.
Although studies have shown the usefulness
of using information about the argumentative
structure for essay scoring, no argument mining
corpus with ground-truth essay quality annota-
tions has been published yet. Moreover, none
of the existing corpora contain essays written
by school students specifically. To fill this re-
search  gap,  we  present  a  German  corpus  of
1,320 essays from school students of two age
groups.  Each essay has been manually anno-
tated for argumentative structure and quality
on multiple levels of granularity. We propose
baseline approaches to argument mining and
essay scoring, and we analyze interactions be-
tween both tasks, thereby laying the ground for
quality-oriented argumentative writing support.
## 1  Introduction
Writing argumentative texts, in particular argumen-
tative essays, constitutes an essential part of school
students’ writing education. However, learning to
write arguments of high quality can be challeng-
ing (Zhu, 2001; Ferretti et al., 2007; Peloghitis,
2017; Alexander et al., 2023). It requires various
skills, from writing fundamentals, such as syntax
and grammar, to argumentation-specific skills, such
as meaningfully organizing and structuring argu-
ments and counter-considerations (Rezat, 2011).
This takes time and effort to master (Ka-kan-dee
and Kaur, 2014; Dang et al., 2020). Given teachers’
limited time to give students feedback on their writ-
ing, automatic argumentative writing support could
## [12.10.2017]
## Dear Mrs. Grotje,
I would prefer to buy sports and play
equipment for the school
because we want to let off steam during the
break and free ourselves from the lessons.
We don’t want to sit on sofas and talk
We sports 2 to 3 times a week, that’s the only
time we can move around.
For the rest of the classes, we mostly sit and
listen to the teachers.
You can sit in class,
Best regards, OK51PL31
## CONCLUSION:
## Body
## Conclusion
## Argument
## Argument
## Thesis
## Claim
## Claim
## Premise
## Premise
## Premise
## Premise
## Positioning
## Reasoning
## Describing
## Describing
## Describing
## Describing
## Describing
## Instructing
because then we’d want to rush out and romp
around during class.
Sitting, contributing to the lesson, and listening
can all be done during school hours.
but during breaks, you need to move, have fun,
and clear your head from the lessons.
## Claim
## Claim
## Reasoning
RelevanceContentStructureStyleOverall
Figure 1: Exemplary annotated school student essay on
the use of school funding, taken from our corpus. The
text is from the FD-LEX corpus (Becker-Mrotzek and
Grabowski, 2018), translated from German for display.
benefit students as it offers guidance at their own
pace and convenience (Wambsganss et al., 2022a).
Argumentative writing support systems employ
argument mining to analyze input texts (Stab, 2017;
Wambsganss  and  Niklaus,  2022;  Weber  et  al.,
2023), that is, computational methods that iden-
tify argumentative components and their relations.
Common components aremajor claim(main stand-
point of the text, also known asthesis),claim(con-
troversial statement), andpremise(reason for justi-
fying or refuting the claim) along with their ar-
gumentative  relationssupportandattack.   This
knowledge enables the systems to give feedback on
the structure of a text, e.g., by highlighting unwar-
ranted claims (Stab and Gurevych, 2017a), or by an-
alyzing the number of argumentative components
quantitatively (Stab and Gurevych, 2017a; Wambs-
ganss and Niklaus, 2022; Weber et al., 2023).
Unlike argument mining, automated essay scor-
ing explicitly evaluates essay quality, either holis-
## 2661

tically (Uto et al., 2020; Yang et al., 2020; Wang
et al., 2023) or specific linguistic aspects, such as
coherence (Li et al., 2018; Farag et al., 2018), gram-
mar (Ajit Tambe and Kulkarni, 2022), and organi-
zation (Persing et al., 2010; Rahimi et al., 2015).
Combining argument mining with essay scoring
may enable support systems to give students com-
prehensive feedback on their writing. In addition,
it helps identify how different argumentative struc-
tures influence the overall essay quality and which
structures are common for different levels of qual-
ity (Wachsmuth et al., 2016).  However, student
essay corpora for argument mining are scarce and
do not include ground-truth essay quality annota-
tions (Stab and Gurevych, 2017a).  Moreover, no
corpus with structure annotations for essays written
by school students has been published yet.
To fill this research gap, we present a German
corpus of 1,320 school student essays with manual
annotations for argumentative structure and essay
quality.  The essays have been systematically se-
lected from an existing corpus (Becker-Mrotzek
and  Grabowski,  2018),  equally  distributed  over
two age groups (fifth-graders and ninth-graders)
and binary genders, three per student. We present
an extensive annotation scheme focused on school
student essays that covers argumentative structure
on four levels of granularity as well as five essay
quality aspects, as shown in Figure 1. To achieve
consistent annotations, we developed annotation
guidelines in close dialogue with our expert anno-
tators from the field of language education.  This
led to high agreement between the annotations.
Our analyses of the corpus provide various in-
sights into the correlation between the different
levels of argumentative structure and essay quality,
as well as the interaction between these two types
of annotation. We experiment with fine-tuned trans-
formers and adapters as baseline approaches to min-
ing argumentative structure and scoring essay qual-
ity. Moreover, we demonstrate that the information
on argumentative structure helps predicting the es-
say quality, which is in line with what previous
studies showed on other corpora (Wachsmuth et al.,
2016; Beigman Klebanov et al., 2016; Nguyen and
Litman, 2018).  This result underlines the useful-
ness of our corpus annotations for quality-oriented
argumentative writing support.
More explicitly,  this  work aims to  answer (i)
how the argumentative structure and essay qual-
ity of school student essays can be modeled, (ii)
how different levels of argumentative structure and
essay quality correlate for school student essays,
and (iii) how this correlation can be exploited to
automatically score the essay quality.
Altogether, this paper’s main contributions are:
## •
A corpus for studying argumentative structure
and essay quality on school student essays
•Empirical insights into the interactions of ar-
gumentative structure and essay quality
-  Baseline approaches to argument mining and
essay scoring
## 1
## 2  Related Work
Argumentative writing is a key capability that is
taught in school across age groups and disciplines
(Becker-Mrotzek  et  al.,  2010;  Rezat,  2011).   A
common educational form of argumentative text
is the essay, where school students should intro-
duce a thesis, to which they provide pro and con
arguments, and finally conclude (Townsend et al.,
1993; Schröter, 2021). The components of an argu-
mentative text take on different roles (e.g.,claim
orpremises), and they may operationalize differ-
ent actions (e.g.,concedingorreasoning) (Feilke,
2017). Learning to write argumentative text is com-
plex and requires continuous and detailed feedback
(Kellogg et al., 2010; Wambsganss et al., 2022b).
Analyzing the argumentative structure of texts
computationally,  also known as argument(ation)
mining, is a crucial and widely-studied step in pro-
viding automatic support for argumentative writing
(Stede and Schneider, 2019).  Student essays are
a prominent domain for argument mining.  A re-
spective annotated corpus of 402 English student
essays is available (Stab and Gurevych, 2017a), for
which also quality issues such as insufficient claim
support have been modeled (Stab and Gurevych,
2017b; Gurcke et al., 2021). Additionally, student
corpora are available for more specific domains,
such  as  argumentative  legal  texts  (Weber  et  al.,
2023), persuasive peer reviews on business mod-
els (Wambsganss et al., 2020), and business model
pitches (Wambsganss and Niklaus, 2022).
Some research has used argumentative structure
to assess essay quality. In consecutive works, Pers-
ing et al. (2010) and Persing and Ng (2013, 2014,
2015) graded different argumentation-related qual-
ity aspects for the well-known essay corpus ICLE
## 1
Our corpus and experiment code can be found under:
https://github.com/webis-de/NAACL-24.
## 2662

(Granger et al., 2009), namely organization, thesis
clarity, prompt adherence, and argument strength.
In contrast, Horbach et al. (2017) targeted different
quality aspects of argumentative writing at once.
Some  works  further  investigated  the  interaction
between argumentative structure and essay qual-
ity.  Wachsmuth et al. (2016) found that multiple
argumentation-related  essay  scoring  tasks  bene-
fit from argument mining, underlining the impact
of argumentative structure on essay quality.  The
analyses by Beigman Klebanov et al. (2016) and
Nguyen and Litman (2018) suggest that this find-
ing also holds for predicting holistic essay scores,
while Persing et al. (2010) observed similar for the
quality aspect organization. However, these stud-
ies relied on automatically assigned quality scores
only, due to the lack of ground-truth annotations.
In a related line of research, approaches have
been proposed to suggest revisions for argumenta-
tive essays (Afrin and Litman, 2018), to assess the
need for and the quality of revisions (Skitalinskaya
and Wachsmuth, 2023; Liu et al., 2023), as well
as to perform argument revisions computationally
(Skitalinskaya et al., 2023). Other works towards
writing support for argumentative essays presented
a prototypical system that gives simple feedback
in terms of missed criteria (Stab, 2017),  design
principles for an adaptive learning tool (Wambs-
ganss and Rietsche, 2019), visual feedback to the
learner to prompt them to repair broken argument
structures (Wambsganss et al., 2022a), or point to
enthymematic gaps in arguments and make sugges-
tions on how to fill these gaps (Stahl et al., 2023).
Most recently, Britner et al. (2023) proposed a tool
that not only analyzes issues with argument quality
but also generates an explanation for its prediction.
Our corpus supports these steps towards support
systems for argumentative writing by providing
detailed ground-truth annotations for both the argu-
mentative structure and the quality of essays.
However, all the works mentioned deal with texts
written by university students, while our work tar-
gets argumentative essays written by school stu-
dents, fifth-graders and ninth-graders specifically.
To the best of our knowledge, the only other pub-
lished corpora with school student essays is not
openly available (Correnti et al., 2013) and has
been analyzed for essay-level quality aspects only,
such as the integration of evidence (Rahimi et al.,
2014) and the essay’s organization (Rahimi et al.,
2015).  We recently came across another school
student essay corpus in English with annotations
for argumentative structure and quality, which has
yet to be published.
## 2
We go beyond in this work
by assessing the quality of school student essays in
terms of five aspects derived from language educa-
tion literature while incorporating their interaction
with annotated argumentative structures. This may
foster the development of effective methods for
helping school students improve their argumenta-
tive writing skills.
## 3  School Student Essay Corpus
This section presents the source data and annota-
tion of our corpus for analyzing the argumentative
structure and quality of school student essays.
## 3.1  Source Data
As the basis, we systematically selected 1,320 Ger-
man school student essays from the FD-LEX cor-
pus (Becker-Mrotzek and Grabowski, 2018).
## 3
## The
authors instructed students to each write three ar-
gumentative essays on topics pertinent to school
students: (a) a letter to school funding organization
on possible use of funding, (b) a statement on how
to deal with the misbehavior of a fellow student,
(c) a statement on who is guilty in a bike accident.
We seek to enable analyses of differences across
different groups of school student essays on the
corpus. Therefore, we pseudo-randomly chose 440
school students equally distributed across genders
(onlymaleandfemaleexist in the corpus) and age
groups (fifth-gradersandninth-graders).  Subse-
quently,  we included all three essays written by
each selected school student from the source data.
## 3.2  Annotation Scheme
Our annotation scheme goes beyond existing cor-
pora for argument mining, covering the macro and
micro structure of argumentative essays on four
levels in total. In addition, we evaluate the quality
of the essays overall and in terms of four quality
aspects. Figure 2 overviews our annotation scheme.
Argumentative StructureOn the broadest level
of granularity for argumentative structure, we an-
notatediscourse functions(Persing et al., 2010):
## 2
The  unpublished  pre-print  is  available  athttps://
zenodo.org/records/8221504.
## 3
Essays and metadata (grade, school form, age, gender,
language  background,  and  age  group)  are  available  here:
https://fd-lex.uni-koeln.de
## 2663

## Modied Thesis
## Antithesis
## Concluding
## Instructing
## Reasoning
## Comparing
ExemplifyingQualifying
## Conceding
DescribingReferencing
## Positioning
## Topic
## Claim
## Premise
## Conclusion
## Thesis
## Counter-argument
## Argument
Discourse ModesComponentsArgumentsDiscourse Functions
## Body
## Introduction
Argumentative StructureEssay Quality
## Content
## Rating
## Structure
## Relevance
Relations:support / attack
## Overall
## Style
MacroMicro
Figure 2: Proposed annotation scheme for argumentative school student essays: Four levels of argumentative macro
and micro structure (discourse functions, arguments, components, discourse modes) and five essay quality aspects.
•Introduction.Initiates an essay by presenting
the topic and possibly the context of an essay.
This section is usually non-argumentative and
placed at the beginning of an essay.
## •
Body.Core of the essay, containing the major-
ity of argumentative components.
## •
Conclusion.Summary of main points, often
with a final evaluation of the topic. This sec-
tion is typically found at the end of the essay.
Next, we annotateargumentsthat comprise one
point in an argumentative text, following Walton
et al. (2008).  We differentiate them by stance to-
wards the main standpoint (thesis) of an essay:
•Argument.Ideally a claim (conclusion) and
premises (reasons) supporting the claim.
•Counter-argument.An argument that attacks
the thesis of an essay.
For analyzing the micro structure, we annotate argu-
mentative and non-argumentativecomponents. As
Stab and Gurevych (2017a), we also mark support
and attack relations between them (see Figure 2):
•Topic.Non-argumentative component that de-
scribes the subject or purpose of the essay.
•Thesis.Main standpoint of the whole argu-
mentative text towards the topic. Repetitions
of the thesis are also annotated as such.
## •
Antithesis.Thesis contrary to the actual thesis.
•Modified Thesis.Modified version of the ac-
tual thesis (e.g., more detailed or resticted).
## •
Claim.Statement that conveys a stance to-
wards the topic.
## •
Premise.Reason that is given to support or
attack a claim or another premise.
## 4
## 4
The components in our annotation scheme are similar to
those of Stab and Gurevych (2017a). We addedantithesisand
modified thesisto reflect the changes in position in the essays.
On the finest level of granularity, we annotatedis-
course modes(Smith, 2003) specific to school stu-
dent essays. They are derived from language educa-
tion literature, where they are used for developing
and analyzing argumentative writing skills (Gätje
et al., 2012; Rezat, 2018; Feilke and Rezat, 2021):
•Comparing.Contrasting supporting and at-
tacking points to a statement.
•Conceding.Addressing a counter-considera-
tion and refuting it to support the own stance.
## •
Concluding.Drawing logical inferences using
consecutive or final clauses (so that,if... then).
•Describing.Providing additional information,
such as facts, statistics, and background data.
•Exemplifying.Providing examples or report-
ing on experiences.
•Instructing.Providing  explicit  instructions
that recommend a specific course of action.
•Positioning.Expressing the own standpoint.
•Reasoning.Providing causal links to support
a claim/thesis using markers (because,then).
•Referencing.Mentioning statements made by
others, for example, by authorities.
## •
Qualifying.Presenting a variation of the all-
or-nothing standpoints.
Essay QualityAs Persing et al. (2010), we score
essay quality on a 7-point scale from 1 (unsuccess-
ful), 2 (rather unsuccessful), 3 (rather successful)
to 4 (completely successful), with half points in
between. We adapted the quality aspects of Kruse
et al. (2012) for assessing school student essays in
general to argumentative essays as follows:
•Relevance.The essay fits the prompt.
## •
Content.The selection of content helps to
reach the essay’s goal.
## 2664

•Structure.The selected points are coherent
and well-connected.
•Style.The use of language is adequate.
•Overall.The overall impression of the rater.
## 3.3  Annotation Process
We underwent the following process for both argu-
mentative structure and essay quality:
To test and refine our annotation guidelines, we
conducted  pilot  studies  in  which  all  annotators
worked on the same 30 texts.  We then discussed
their understanding of the guidelines and annota-
tion differences. We integrated their feedback into
the guidelines to then test the reliability of the anno-
tations in an inter-annotator agreement (IAA) study,
where all annotators independently worked on the
same 120 texts. Finally, each annotator annotated
a set of 1,200 essays in the main annotation study.
As annotators, we employed experts in German
language education from our lab and started the
pilot and IAA studies on argumentative structure
with three annotators. For the main part, only the
two annotators with the most reliable annotations
proceeded. The same annotators then annotated the
essay quality, since they had already been trained
in argumentative texts and our general procedure.
However, we acknowledge that the annotators may
have been predisposed to view essays in a certain
way after the first annotation.
To assemble the final corpus, we combined the
1200 essays from the main study with the 120 es-
says from the IAA study after solving annotation
conflicts. For conflicts between the three structure
annotations per IAA essay, we kept the annotations
that had the highest agreement across all levels with
the other two. For conflicts between essay quality
scores, we used their mean as the final score.
## 5
3.4  Inter-Annotator Agreement
For the components, we follow Stab and Gurevych
(2017a) in that we evaluate the agreement per essay
at the token level, so the token labels are the unit
of analysis.  Thereby, overlaps of annotations are
taken into account.  For relations, we determined
the component-level spans that at least two annota-
tors agreed on with a relative overlap≥75%. For
all pairs of these, we then compared the relation
labels (no relation, support, or attack) between the
## 5
We rounded down to the next valid quality score for low
values (<2.5) and rounded up for high values (>2.5) to
prevent an upward distortion of the distribution.
## Argumentative Structureα
## Discourse Functions0.89
## Arguments0.86
## Components0.81
## Discourse Modes0.74
## Relations0.58
## Essay Qualityα
## Relevance0.77
## Content0.95
## Structure0.84
## Style0.92
## Overall0.95
Table 1: Krippendorff’sαagreement in the IAA study
between three annotators for argumentative structure
and two annotators for essay quality. The high values
stress the high reliability of our annotations.
annotators. The mean Krippendorff’sαscores over
the 120 IAA essays are reported in Table 1.  For
essay quality, we computed theα-value per quality
aspect with essays as the unit of analysis.
The agreement is high for argumentative struc-
ture spans with values between 0.74 and 0.89. The
agreement  for  relations  is  lower  but  reasonable,
given that disagreement from the components an-
notations is propagated to the relations. The agree-
ment for essay quality is also high, too, ranging
from 0.77 to 0.95.  Overall, we conclude that the
annotations can mostly be seen as very reliable.
Content and style quality annotations are very con-
sistent between annotators, while assessing the rele-
vance and structure seems slightly more subjective.
## 3.5  Corpus Statistics
Table 2 gives insights into the label distribution
for  argumentation  structure.Bodyoccurs  most
frequently among the discourse functions (1,335
times). With 56.75 tokens on average, bodies are
also  notably  longer  thanintroductionsandcon-
clusions.   On  the  argument  level,  we  note  that
counter-argumentsare rather sparse in student es-
says.   Among the components,claimsare most
frequent in total and per essay, followed bythe-
ses.  Furthermore, we notice thatmodified theses
are usually longer than theses, which matches our
expectation that students add more details or restric-
tions to the thesis there. The most used discourse
modes arepositioning,describing, andreasoning,
whilereferencing,comparing, andexemplifyingoc-
cur rarely. Notable are also the differences in span
length, e.g.positioningspans have on average only
about half as many tokens ascomparingspans.
Table 3 gives the frequency of annotated rela-
tions in our corpus. Most relations outgoing from
claimsare directed towardstheses(92.6%), while
most relations outgoing frompremisesare directed
towardsclaims(85.8%). Overall, 96.2% of the re-
## 2665

Label# Spans # Tokens Tokens/Span Spans/Essay
## Introduction1142 32920.430.09
## Body1 335   75 76656.751.01
## Conclusion1912 93815.380.14
## Argument2 692   51 56019.152.04
## Counter-arg.3451415.120.03
## Topic1011 65616.400.08
## Thesis1 68719 58111.611.28
## Modified T.2674 49016.820.20
## Antithesis1417412.430.01
## Claim3 137   39 09612.462.38
## Premise1 02012 53312.290.77
## Comparing2043121.550.02
## Conceding1422 87420.240.11
## Concluding86811 65413.430.66
## Describing1 69222 25813.151.28
## Exemplifying6392614.700.05
## Instructing1762 17412.350.13
## Positioning1 75819 17810.911.33
## Reasoning1 55317 20411.081.18
## Referencing1619712.310.01
## Qualifying1472 34415.950.11
Table  2:  Argumentative  structure  annotations  in  the
corpus:  Total number of spans and tokens per label,
average span length in number of tokens (Tokens/Span)
and average number of spans per essay (Spans/Essay).
The highest value per column and level is marked bold.
FromClaimto#  %
## Thesis2844 92.6
## Modified Thesis    218    7.1
## Antithesis9    0.3
FromPremiseto   #  %
## Thesis6    0.6
## Claim872 85.8
## Premise138  13.6
Table 3: Absolute and relative frequency of annotated
relations outgoing fromclaim(left) orpremise(right).
lations were labeled assupportand 3.8% asattack.
The distribution of quality scores is shown in
Table 4. We can see thatrelevance,structure, and
stylehave a similar score distribution, while the
distribution ofcontentscores is shifted towards
the higher scores,  with the highest mean (2.80).
Overall quality has the lowest mean score (2.20)
and was most often scored with the lowest score
of 1.0. These results suggest that overall quality is
not just the average of the other annotated quality
aspects but that it emerges from the annotators’
perception and possibly other aspects.
## 4  Analysis
This section reports on our corpus analysis of the
interaction between the argumentative structure on
micro vs. macro level and component vs. discourse
mode level, and the different essay quality aspects.
## Quality Aspect 1.0  1.5  2.0  2.5  3.0  3.5  4.0 Mean
## Relevance64  131548358  1902362.22
## Content6233  123  312510 173 107   2.80
## Structure5991  423  414  29224172.35
## Style751593964362331292.25
## Overall90142  478  390  1952322.20
Table 4:  Distribution and mean of scores per quality
aspect. The highest value per column is marked bold.
## (a)
## (b)
Figure 3: Cooccurrence matrices: Relative token-level
overlap of (a) macro and micro structure and (b) compo-
nent and discourse mode labels in percent. For example,
68% of all tokens labeled asIntroductionon the macro
level are also labeled asTopicon the micro level.
4.1  Macro vs. Micro structure
Figure 3(a) shows the overlap between macro struc-
ture (discourse functions and arguments) and mi-
cro structure (components and discourse mode) la-
bels.  Theintroductionmainly includes thetopic
(68%),  while every second token in thebodyis
aclaimon average.  Thethesiscooccurs with all
three discourse functions. We see that the propor-
tion ofclaimsandpremisesdiffers forarguments
andcounter-arguments.  Counter-arguments con-
tain more claim tokens than arguments, while fewer
counter-argument tokens are part of a premise.
The usage of discourse modes differs between
the macro-structure levels, too. In the introduction,
students mostlydescribe(68%) andposition(24%).
The discourse modes are more diverse for the body,
also including a notable portion ofreasoning. As
expected, in theconclusion, students focus more
onconcluding.  While describing and reasoning
are prevalent in arguments and counter-arguments,
a notable portion of argument tokens is used for
concluding. At the same time, moreconcedingand
## 2666

## Relevance Content Structure Style Overall
## Relevance.53.61.47.75
## Content.53.48.41.60
## Structure.61.48.51.71
## Style.47.41.51.61
## Overall.75.60.71.61
Table 5:  Kendall’sτcorrelation between the quality
aspects. The highest value per column is marked bold.
qualifyingtokens occur in counter-arguments. This
is expected, since especially in counter-arguments
other points of view should be varied or refuted.
4.2  Components vs. Discourse modes
The cooccurrences between components and ac-
tions can be seen in Figure 3(b).  While thetopic
is mostlydescribed(90%) and thethesisconsists
primarily ofpositioning(85%), the remaining com-
ponents include more diverse discourse modes. In
contrast totheses,modified thesesalso featurede-
scribingandqualifyingtokens, whileantithesesad-
ditionally coverconcedingandconcluding.Claims
andpremisesmainly cooccur withdescribing,rea-
soning, andconcluding. However, the proportions
differ slightly. The cooccurrence matrix between
all structure labels can be found in Appendix A.
## 4.3  Essay Quality
To further assess the interaction between the quality
aspects, Table 5 shows all pairwise Kendall’sτcor-
relations.  All aspects correlate most withoverall
quality, most stronglyrelevance(.75).  The cor-
relation betweencontentandstyleis lowest (.41),
which underlines their distinctive nature.
## 5  Experiments
This section presents baseline approaches to the
two main tasks our corpus enables: Predicting the
argumentative structure (argument mining) and the
essay quality (essay scoring). Additionally, we in-
vestigate whether information about the argumen-
tative structure helps to predict the essay quality.
## 5.1  Argument Mining
We treat argument mining as a token classification
task: Given a school student essay and a structure
level, predict the label of each token on that struc-
ture level. The IOB2 format is used for the labels
to separate adjacent spans of the same type.  We
performed 5-fold cross-validation for each struc-
ture level.  For each folding, we used four folds
## D. Func.  Argum.  Compon.  D. Mode
ApproachAcc. F
## 1
## Acc. F
## 1
## Acc.  F
## 1
## Acc. F
## 1
## Random.14  .00.20  .00.08   .00.05  .00
## Majority.86  .52.56  .00.41   .00.24  .00
mDeBERTaV3.92  .46.86  .29.66   .21.63  .21
## -adapter.95 .68   .92 .52   .76  .49   .73 .46
## Human.98  .94.96  .85.93   .89.89  .84
Table 6: Argument mining results: Macro F
## 1
-score and
accuracy of each approach in 5-fold cross-validation on
all four argumentative structure dimensions. The best
value per column is marked bold.
(80%) for training and divided the fifth fold in half:
one half (10%) for selecting the best-performing
checkpoint in terms of macro-averaged F
## 1
## -score,
and the remaining half (10%) for testing.
ModelsWe used the multilingual modelmDe-
BERTaV3(He et al., 2023) (microsoft/mdeberta-
v3-base) from Huggingface (Wolf et al., 2020).
## 6
Besides, we tested the effect of trainingadapters
(Houlsby et al., 2019), a set of task-specific param-
eters that are added to every transformer layer of
mDeBERTaV3 and fine-tuned on the task while the
model weights are fixed.  To quantify the impact
of learning, we compare against a random baseline
that chooses a token label pseudo-randomly and a
majority baseline that always predicts the majority
token label from the training set. As upper bound,
we report the human performance in terms of the
average of each annotator in isolation on the 120
IAA texts annotated by all annotators.
## 7
Experimental SetupWe train mDeBERTaV3 for
30 epochs (1,980 steps) using the suggested hyper-
parameter values: a learning rate of3e−5, batch
size 16, and 500 warmup steps. For mDeBERTaV3-
adapter, we follow Pfeiffer et al. (2020) who rec-
ommend to use a higher learning rate of1e−4and
train longer, here 50 epochs (3,300 steps).
ResultsTable 6 presents the token classification
results for all levels of argumentative structure, av-
eraged over all folds. Noteworthily,mDeBERTaV3-
adapteroutperforms  training  the  whole  model
(mDeBERTaV3)  in  all  cases.Given  that  the
## F
## 1
-scores  improve  more  than  the  accuracy,  the
## 6
Explorative experiments using instruction fine-tuned mod-
els such as Alpaca (Taori et al., 2023) did not lead to promising
results for our token classification task.
## 7
Note that the test set used for the model performance is a
different subset of the dataset.
## 2667

ApproachRelevanceContentStructureStyleOverall
## Random−0.013±0.084−0.011±0.071−0.014±0.0730.017±0.084−0.004±0.083
## Majority0.000±0.0000.000±0.0000.000±0.0000.000±0.0000.000±0.000
mDeBERTaV30.530±0.0690.295±0.1090.513±0.0440.492±0.0590.616±0.040
## -adapter0.564±0.0180.431±0.0980.575±0.0380.579±0.0770.648±0.054
-fusion-w/-discourse-functions0.599±0.0430.381±0.1340.559±0.0360.569±0.0690.668±0.049
## -fusion-w/-arguments0.593±0.0300.448±0.1050.575±0.0190.581±0.0540.668±0.036
## -fusion-w/-components
## †
## 0.600±0.025
## 0.437±0.1370.543±0.0440.585±0.0530.663±0.046
-fusion-w/-discourse-modes0.544±0.0280.420±0.1180.535±0.0410.583±0.0640.645±0.023
## -fusion-w/-all0.574±0.0390.454±0.1420.546±0.0130.617±0.057
## †
## 0.686±0.031
## Human0.636±0.0550.632±0.0030.734±0.0070.766±0.0050.746±0.003
Table 7: Essay scoring results: QWK of each approach in 5-fold cross-validation on all five quality dimensions. The
best value per column is marked bold. We mark significant gains overmDeBERTaV3-adapteratp < .05with†.
adapters seem less prone to overfitting to the major-
ity label. This learning success suggests the possi-
bility of predicting all argumentative structure lev-
els on our corpus. However, further improvements
using more advanced approaches are expected.
## 5.2  Essay Scoring
We treat predicting the essay quality as a text clas-
sification task:  Given a school student essay and
a quality aspect, predict the corresponding qual-
ity score.  As before, we performed 5-fold cross-
validation for each quality aspect using the same
folds.    We  selected  the  best-performing  check-
point on the validation set using quadratic weighted
kappa (QWK), the most widely adopted metric for
automatic essay scoring (Ke and Ng, 2019).
ModelsWe adopted the previous approaches by
changing  the  head  to  a  text  classification  head.
To analyze the interaction between argumentative
structure and essay quality, we employedAdapter-
Fusion(Pfeiffer et al., 2021), a multi-task learning
framework that can be used to investigate relations
between different dimensions by learning how to
combine model weights with one or more adapters.
We used the mDeBERTaV3-adapters trained on
argumentative structure from the previous experi-
ment. As the final adapter, we chose the one trained
on the folding that performed most representative
for all folds (F
## 1
-score closest to the reported aver-
aged F
## 1
-score across folds). To measure the impact
of each level of argumentative structure on the scor-
ing performance, we used each adapter individually
and a combination of all of them.
Experimental SetupThe experimental setup for
mDeBERTaV3  and  mDeBERTaV3-adapter  was
adopted  from  before.   For  training  the  Adapter-
Fusion, we followed Pfeiffer et al. (2021) to use a
learning rate of5e−5and trained shorter than the
adapters, in our case for 20 epochs (1,320 steps).
ResultsTable 7 shows the scoring results.  All
models outperform the lower-bound baselines (ran-
domandmajority),  suggesting  that  the  quality
scoring can be learned from our corpus.  Further-
more, fusing all adapters trained on argumentative
structure (mDeBERTaV3-fusion-w/-all) performs
best for three out of five quality aspects, signifi-
cantly beating mDeBERTaV3-adapter in predict-
ing overall quality.
## 8
This underlines the need for
all four levels of argumentative structure together
in order to improve scoring overall quality (0.686
vs.  0.648).   In  addition,  using  only  the  adapter
trained  on  the  component  level  (mDeBERTaV3-
fusion-w/-components) helps to significantly im-
prove over mDeBERTaV3-adapter in predicting
relevance (0.600 vs. 0.564), indicating an interac-
tion between the structure on component level and
this quality aspect. QWK scores greater or equal to
0.6 suggest substantial agreement between the pre-
dicted and ground-truth quality scoring of essays.
AdapterFusion ActivationsAdapterFusion ex-
tracts information from adapters only if they benefit
the target task. Similar to Falk and Lapesa (2023),
we visualize the average activations of our model
mDeBERTaV3-fusion-w/-allover the layers in Fig-
ure 4 to investigate the influence of each level of
argumentative structure on the quality scoring. All
adapters are activated fairly evenly for all quality
aspects, with slight deviations. This aligns with our
previous results and underlines that all annotated
## 8
We use Wilcoxon signed-rank tests atp < .05for testing
the significance.
## 2668

D.Func.
## Argum.
## Compon.
D.Mode
## Avg.23.26.21.30
## Relevance
D.Func.
## Argum.
## Compon.
D.Mode
## .14.31.21.35
## Content
D.Func.
## Argum.
## Compon.
D.Mode
## .26.21.20.32
## Structure
D.Func.
## Argum.
## Compon.
D.Mode
## .27.19.25.29
## Style
D.Func.
## Argum.
## Compon.
D.Mode
## .28.23.21.28
## Overall
## 0
## 1
Figure 4:  AdapterFusion activation on average over the layers for eachmDeBERTaV3-fusion-w/-allmodel per
quality aspect.  We average the activation for each fused adapter (discourse functions, arguments, components,
discourse modes) over all instances in the most representative test set folding.
structure levels are helpful for quality scoring. The
activations per layer can be found in Appendix B.
## 6  Conclusion
Argumentative writing support of school students
presupposes that the quality of their arguments can
be assessed. Until now, no argument mining corpus
with school student essays has been published, let
alone any essay corpus with both argument and
quality annotations.  With this work, we fill both
research gaps with a new corpus of 1,320 German
school student essays, annotated by experts for ar-
gumentative structure and essay quality.
Our  corpus  analysis  has  provided  various  in-
sights into the correlation between the different
levels of argumentative structure and essay quality.
In our experiments with fine-tuned transformers
and adapters for mining argumentative structure
and scoring essay quality we have demonstrated
that combining information on all four argumenta-
tive structure levels helps the prediction of essay
quality. This shows the usefulness of our corpus for
research on quality-oriented argumentative writing
support, which we seek to enable with this paper.
We point out that our corpus contains various
information yet to be explored, such as argumenta-
tive relations and school student metadata. It thus
lays the ground for further analyses—like identify-
ing unwarranted claims and studying differences
across age groups and genders.
## 7  Limitations
Aside from the still-improvable performance of the
presented baseline models for argument mining
and essay scoring, we see two notable limitations
of our work: the restriction to German texts, and
the pending utilization of the corpus for quality-
oriented argumentative writing support.
First, we point out the specific language back-
ground of our work.  The essays were written by
German school students, and the annotations were
developed in close communication with German
experts from the field of language education, while
the discourse modes and essay quality aspects are,
to a considerable extent, derived from work on Ger-
man texts.  This means that our findings may not
perfectly align with argumentative writing in other
countries or languages with different expectations
for argumentative essays.
Second, while our analyses suggest that our cor-
pus helps to enable quality-oriented argumentative
writing support, the perceived usefulness of such a
tool is still to be evaluated. We expect and encour-
age future work to utilize our corpus for such writ-
ing support tools, for example, by further analyzing
which exact argumentative structures influence the
essay quality and to what extent. Interpretable es-
say quality scoring based on the structure might
generate helpful insights that can be used as writing
feedback by school students.
## 8  Ethical Considerations
We see no apparent risk of the corpus or the meth-
ods  presented  in  this  paper  being  misused  for
ethically doubtful purposes.   The authors of the
FD-LEX corpus (Becker-Mrotzek and Grabowski,
2018) have already pseudonymized the author of
each essay. Therefore, it is not possible to identify
the individual school student from the provided
data. However, we want to point out that one might
find differences in the essays across gender or age
groups that do not reflect reality but are rather due
to an unintentional bias in the data selection.
## Acknowledgments
We would like to thank the participants of our study
and the anonymous reviewers for the valuable feed-
back and their time. This work was partially funded
by the Deutsche Forschungsgemeinschaft (DFG,
German Research Foundation) within the project
ArgSchool, project number 453073654.
## 2669

## References
Tazin Afrin and Diane Litman. 2018.  Annotation and
classification of sentence-level revision improvement.
InProceedings of the Thirteenth Workshop on In-
novative Use of NLP for Building Educational Ap-
plications, pages 240–246, New Orleans, Louisiana.
Association for Computational Linguistics.
Aniket Ajit Tambe and Manasi Kulkarni. 2022.   Au-
tomated essay scoring system with grammar score
analysis. In2022 Smart Technologies, Communica-
tion and Robotics (STCR), pages 1–7.
## Patricia A. Alexander, Jannah Fusenig, Eric C. Schoute,
Anisha  Singh,  Yuting  Sun,  and  Julianne  E.  van
Meerten. 2023. Confronting the challenges of under-
graduates’ argumentation writing in a “learning how
to learn” course.Written Communication, 40(2):482–
## 517.
Michael  Becker-Mrotzek  and  Joachim  Grabowski.
## 2018.   Textkorpus Scriptoria.   In Michael Becker-
Mrotzek  and  Joachim  Grabowski,   editors,FD-
LEX (Forschungsdatenbank Lernertexte). Mercator-
Institut für Sprachförderung und Deutsch als Zweit-
sprache,  Köln.Available  at:https://fd-lex.
uni-koeln.de.
Michael Becker-Mrotzek, Frank Schneider, and Klaus
Tetling. 2010. Argumentierendes Schreiben - lehren
und  lernen.  Vorschläge  für  einen  systematischen
Kompetenzaufbau in den Stufen 5 bis 8.
## Beata Beigman Klebanov, Christian Stab, Jill Burstein,
Yi Song, Binod Gyawali, and Iryna Gurevych. 2016.
Argumentation: Content, structure, and relationship
with essay quality. InProceedings of the Third Work-
shop on Argument Mining (ArgMining2016), pages
70–75, Berlin, Germany. Association for Computa-
tional Linguistics.
Sebastian Britner, Lorik Dumani, and Ralf Schenkel.
-  Aquaplane:  The argument quality explainer
app. InProceedings of the 32nd ACM International
Conference on Information and Knowledge Manage-
ment, CIKM ’23, page 5015–5020, New York, NY,
USA. Association for Computing Machinery.
## Richard  Correnti,  Lindsay  Clare  Matsumura,  Laura
Hamilton, and Elaine Wang. 2013.  Assessing stu-
dents’ skills at writing analytically in response to
texts.The Elementary School Journal, 114(2):142–
## 177.
## Scott  Crossley,   Perpetual  Baffour,   Tian  Yu,   Alex
Franklin, Meg Benner, and Ulrich Boser. 2023a.  A
large-scale corpus for assessing written argumenta-
tion: PERSUADE 2.0.
## Scott  Crossley,   Yu  Tian,   Perpetual  Baffour,   Alex
## Franklin, Youngmeen Kim, Wesley Morris, Meg Ben-
ner, Aigner Picou, and Ulrich Boser. 2023b. The en-
glish language learner insight, proficiency and skills
evaluation (ellipse) corpus.International Journal of
## Learner Corpus Research, 9(2):248–269.
Thi Hanh Dang, Thanh Hai Chau, and To Quyen Tra.
- A study on the difficulties in writing argumen-
tative essays of english-majored sophomores at tay
do university, vietnam.European Journal of English
## Language Teaching, 6(1).
Neele Falk and Gabriella Lapesa. 2023. Bridging argu-
ment quality and deliberative quality annotations with
adapters. InFindings of the Association for Compu-
tational Linguistics: EACL 2023, pages 2469–2488,
Dubrovnik, Croatia. Association for Computational
## Linguistics.
Youmna Farag, Helen Yannakoudakis, and Ted Briscoe.
-   Neural automated essay scoring and coher-
ence modeling for adversarially crafted input.   In
Proceedings of the 2018 Conference of the North
American Chapter of the Association for Computa-
tional Linguistics: Human Language Technologies,
Volume 1 (Long Papers), pages 263–271, New Or-
leans, Louisiana. Association for Computational Lin-
guistics.
Helmuth Feilke. 2017.  Schreib- und Textprozeduren.
In Jürgen Baurmann, Clemens Kammler, and Astrid
Müller, editors,Handbuch Deutschunterricht. Theo-
rie und Praxis des Lehrens und Lernens, 1 edition,
pages 51–57. Reihe Praxis Deutsch.
Helmuth  Feilke  and  Sara  Rezat.  2021.Textproze-
duren  und  der  Erwerb  literaler  Kompetenz.In
Nikolas  Koch  and  Barbara  Kozikowski,  editors,
Sprach(en)erwerb, pages 69–79. Der Deutschunter-
richt.
Ralph   P.   Ferretti,   Scott   Andrews-Weckerly,   and
William E. Lewis. 2007.   Improving the argumen-
tative writing of students with learning disabilities:
Descriptive and normative considerations.Reading
## & Writing Quarterly, 23(3):267–285.
## Sylviane Granger, Estelle Dagneaux, Fanny Meunier,
and Magali Paquot. 2009.The International Cor-
pus of Learner English.   Presses universitaires de
Louvain, Louvain-la-Neuve.
Timon   Gurcke,   Milad   Alshomary,   and   Henning
Wachsmuth. 2021.  Assessing the sufficiency of ar-
guments through conclusion generation. InProceed-
ings of the 8th Workshop on Argument Mining, pages
## 67–77, Punta Cana, Dominican Republic. Associa-
tion for Computational Linguistics.
Olaf Gätje, Sara Rezat, and Torsten Steinhoff. 2012. Po-
sitionierung. Zur Entwicklung des Gebrauchs modal-
isierender Prozeduren in argumentativen Texten von
Schülern  und  Studenten.   In  Helmuth  Feilke  and
Katrin Lehnen,  editors,Textroutinen. Theorie,  Er-
werb und didaktisch-mediale Modellierung, pages
125–153. Lang, Frankfurt/Main.
Pengcheng He, Jianfeng Gao, and Weizhu Chen. 2023.
DeBERTav3: Improving deBERTa using ELECTRA-
style pre-training with gradient-disentangled embed-
ding sharing. InThe Eleventh International Confer-
ence on Learning Representations.
## 2670

Andrea Horbach, Dirk Scholten-Akoun, Yuning Ding,
and Torsten Zesch. 2017. Fine-grained essay scoring
of a complex writing task for native speakers.   In
Proceedings of the 12th Workshop on Innovative Use
of NLP for Building Educational Applications, pages
357–366,  Copenhagen,  Denmark. Association  for
## Computational Linguistics.
## Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski,
## Bruna  Morrone,  Quentin  De  Laroussilhe,  Andrea
Gesmundo, Mona Attariyan, and Sylvain Gelly. 2019.
Parameter-efficient  transfer  learning  for  NLP.   In
Proceedings of the 36th International Conference
on Machine Learning,  volume 97 ofProceedings
of Machine Learning Research, pages 2790–2799.
## PMLR.
Maleerat Ka-kan-dee and Sarjit Kaur. 2014.  Argumenta-
tive writing difficulties of thai english major students.
InThe 2014 WEI International Academic Conference
Proceedings, pages 193–207.
Zixuan Ke and Vincent Ng. 2019.   Automated essay
scoring: A survey of the state of the art. InProceed-
ings of the Twenty-Eighth International Joint Con-
ference on Artificial Intelligence, IJCAI-19, pages
6300–6308. International Joint Conferences on Arti-
ficial Intelligence Organization.
Ronald T. Kellogg, Alison P. Whiteford, and Thomas
Quinlan. 2010.  Does automated feedback help stu-
dents learn to write?Journal of Educational Com-
puting Research, 42(2):173–196.
## Norbert  Kruse,   Anke  Reichardt,   Maik  Herrmann,
Friederike Heinzel, and Frank Lipowsky. 2012. Zur
qualität  von  kindertexten.  entwicklung  eines  bew-
ertungsinstruments  in  der  grundschule.Didaktik
Deutsch  :   Halbjahresschrift  für  die  Didaktik  der
deutschen Sprache und Literatur, 17(32):87–110.
## Xia Li, Minping Chen, Jianyun Nie, Zhenxing Liu, Zi-
heng Feng, and Yingdan Cai. 2018.  Coherence-based
automated essay scoring using self-attention. InChi-
nese  Computational  Linguistics  and  Natural  Lan-
guage Processing Based on Naturally Annotated Big
Data, pages 386–397, Cham. Springer International
## Publishing.
## Zhexiong Liu,  Diane Litman,  Elaine Wang,  Lindsay
Matsumura, and Richard Correnti. 2023. Predicting
the quality of revisions in argumentative writing. In
Proceedings of the 18th Workshop on Innovative Use
of NLP for Building Educational Applications (BEA
2023), pages 275–287, Toronto, Canada. Association
for Computational Linguistics.
Huy Nguyen and Diane Litman. 2018. Argument min-
ing for improving the automated scoring of persua-
sive essays.Proceedings of the AAAI Conference on
## Artificial Intelligence, 32(1).
John Peloghitis. 2017.   Difficulties and strategies in
argumentative writing: A qualitative analysis.Trans-
formation in language education. JALT.
Isaac Persing, Alan Davis, and Vincent Ng. 2010. Mod-
eling organization in student essays. InProceedings
of the 2010 Conference on Empirical Methods in
Natural Language Processing, pages 229–239, Cam-
bridge, MA. Association for Computational Linguis-
tics.
Isaac Persing and Vincent Ng. 2013.  Modeling thesis
clarity in student essays. InProceedings of the 51st
Annual Meeting of the Association for Computational
Linguistics (Volume 1:  Long Papers),  pages 260–
269, Sofia, Bulgaria. Association for Computational
## Linguistics.
Isaac Persing and Vincent Ng. 2014. Modeling prompt
adherence in student essays.  InProceedings of the
52nd Annual Meeting of the Association for Compu-
tational Linguistics (Volume 1: Long Papers), pages
1534–1543,  Baltimore,  Maryland. Association for
## Computational Linguistics.
Isaac Persing and Vincent Ng. 2015.  Modeling argu-
ment strength in student essays.  InProceedings of
the 53rd Annual Meeting of the Association for Com-
putational Linguistics and the 7th International Joint
Conference on Natural Language Processing (Vol-
ume 1: Long Papers), pages 543–552, Beijing, China.
Association for Computational Linguistics.
## Jonas  Pfeiffer,  Aishwarya  Kamath,  Andreas  Rücklé,
Kyunghyun   Cho,    and   Iryna   Gurevych.   2021.
AdapterFusion:  Non-destructive task composition
for transfer learning. InProceedings of the 16th Con-
ference of the European Chapter of the Association
for Computational Linguistics: Main Volume, pages
487–503, Online. Association for Computational Lin-
guistics.
## Jonas Pfeiffer, Andreas Rücklé, Clifton Poth, Aishwarya
## Kamath, Ivan Vuli
## ́
c, Sebastian Ruder, Kyunghyun
Cho, and Iryna Gurevych. 2020.   AdapterHub:  A
framework for adapting transformers.  InProceedings
of the 2020 Conference on Empirical Methods in Nat-
ural Language Processing: System Demonstrations,
pages 46–54, Online. Association for Computational
## Linguistics.
Zahra Rahimi, Diane Litman, Elaine Wang, and Richard
Correnti. 2015.  Incorporating coherence of topics
as a criterion in automatic response-to-text assess-
ment of the organization of writing. InProceedings
of the Tenth Workshop on Innovative Use of NLP
for Building Educational Applications, pages 20–30,
Denver,  Colorado. Association for Computational
## Linguistics.
## Zahra Rahimi, Diane J. Litman, Richard Correnti, Lind-
say Clare Matsumura, Elaine Wang, and Zahid Kisa.
-  Automatic scoring of an analytical response-
to-text assessment.  InIntelligent Tutoring Systems,
pages 601–610, Cham. Springer International Pub-
lishing.
## Sara Rezat. 2011.   Schriftliches Argumentieren. Zur
Ontogenese konzessiver Argumentationskompetenz.
## 2671

Didaktik Deutsch: Halbjahresschrift für die Didaktik
der deutschen Sprache und Literatur, 16(31):50–67.
Sara Rezat. 2018.  Argumentative Textprozeduren als
Instrumente zur Anbahnung wissenschaftlicher Tex-
tkompetenz.   In Sabine Schmölzer-Eibinger,  Bora
Bushati, Christopher Ebner, and Lisa Niederdorfer,
editors,Wissenschaftliches Schreiben lehren und ler-
nen. Diagnose und Förderung wissenschaftlicher Tex-
tkompetenz in Schule und Universität, pages 125–146.
## Waxmann, Münster.
Juliane Schröter. 2021.Linguistische Argumentations-
analyse. Kurze Einführungen in die germanistische
## Linguistik. Universitätsverlag Winter, Heidelberg.
Gabriella Skitalinskaya, Maximilian Spliethöver, and
Henning Wachsmuth. 2023.  Claim optimization in
computational  argumentation.    InProceedings  of
the  16th  International  Natural  Language  Genera-
tion Conference, pages 134–152, Prague, Czechia.
Association for Computational Linguistics.
Gabriella Skitalinskaya and Henning Wachsmuth. 2023.
To revise or not to revise: Learning to detect improv-
able claims for argumentative writing support.   In
Proceedings of the 61st Annual Meeting of the As-
sociation for Computational Linguistics (Volume 1:
Long Papers), pages 15799–15816, Toronto, Canada.
Association for Computational Linguistics.
Carlota S. Smith. 2003.Modes of Discourse: The Local
Structure of Texts. Cambridge Studies in Linguistics.
## Cambridge University Press.
Christian Stab. 2017.Argumentative Writing Support
by means of Natural Language Processing.   Ph.D.
thesis, Technische Universität Darmstadt, Darmstadt.
Christian Stab and Iryna Gurevych. 2017a.   Parsing
argumentation structures in persuasive essays.Com-
putational Linguistics, 43(3):619–659.
Christian Stab and Iryna Gurevych. 2017b.  Recognizing
insufficiently supported arguments in argumentative
essays.   InProceedings of the 15th Conference of
the European Chapter of the Association for Compu-
tational Linguistics: Volume 1, Long Papers, pages
980–990, Valencia, Spain. Association for Computa-
tional Linguistics.
Maja Stahl, Nick Düsterhus, Mei-Hua Chen, and Hen-
ning Wachsmuth. 2023.  Mind the gap: Automated
corpus creation for enthymeme detection and recon-
struction in learner arguments.   InFindings of the
Association for Computational Linguistics: EMNLP
2023, pages 4703–4717, Singapore. Association for
## Computational Linguistics.
Manfred Stede and Jodi Schneider. 2019.Argumenta-
tion Mining. Springer International Publishing.
## Rohan  Taori,  Ishaan  Gulrajani,  Tianyi  Zhang,  Yann
## Dubois, Xuechen Li, Carlos Guestrin, Percy Liang,
and Tatsunori B. Hashimoto. 2023. Stanford alpaca:
An  instruction-following  llama  model.https://
github.com/tatsu-lab/stanford_alpaca.
## Michael A. R. Townsend, Lynley Hicks, Jacquilyn D. M.
Thompson, Keri M. Wilton, Bryan F. Tuck, and Den-
nis W. Moore. 1993.   Effects of introductions and
conclusions in assessment of student essays.Journal
of Educational Psychology, 85(4):670–678.
Masaki  Uto,  Yikuan  Xie,  and  Maomi  Ueno.  2020.
Neural automated essay scoring incorporating hand-
crafted features.  InProceedings of the 28th Inter-
national Conference on Computational Linguistics,
pages 6077–6088, Barcelona, Spain (Online). Inter-
national Committee on Computational Linguistics.
Henning  Wachsmuth,  Khalid  Al-Khatib,  and  Benno
Stein. 2016.  Using argument mining to assess the
argumentation quality of essays.  InProceedings of
COLING 2016, the 26th International Conference on
Computational Linguistics: Technical Papers, pages
1680–1691, Osaka, Japan. The COLING 2016 Orga-
nizing Committee.
Douglas  Walton,   Christopher  Reed,   and  Fabrizio
Macagno.  2008.Argumentation  Schemes.   Cam-
bridge University Press.
Thiemo Wambsganss, Andrew Caines, and Paula But-
tery. 2022a. ALEN app: Argumentative writing sup-
port to foster English language learning. InProceed-
ings of the 17th Workshop on Innovative Use of NLP
for Building Educational Applications (BEA 2022),
pages 134–140, Seattle, Washington. Association for
## Computational Linguistics.
Thiemo Wambsganss, Andreas Janson, and Jan Marco
Leimeister. 2022b.  Enhancing argumentative writ-
ing with automated feedback and social comparison
nudging.Computers and Education, 191:104644.
Thiemo  Wambsganss  and  Christina  Niklaus.  2022.
Modeling  persuasive  discourse  to  adaptively  sup-
port students’ argumentative writing. InProceedings
of the 60th Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers),
pages 8748–8760, Dublin, Ireland. Association for
## Computational Linguistics.
## Thiemo Wambsganss, Christina Niklaus, Matthias Söll-
ner, Siegfried Handschuh, and Jan Marco Leimeister.
-  A corpus for argumentative writing support
in German. InProceedings of the 28th International
Conference on Computational Linguistics, pages 856–
869, Barcelona, Spain (Online). International Com-
mittee on Computational Linguistics.
Thiemo Wambsganss and Roman Rietsche. 2019.  To-
wards designing an adaptive argumentation learning
tool. InInternational Conference on Interaction Sci-
ences.
## Cong Wang, Zhiwei Jiang, Yafeng Yin, Zifeng Cheng,
Shiping Ge, and Qing Gu. 2023. Aggregating multi-
ple heuristic signals as supervision for unsupervised
automated essay scoring. InProceedings of the 61st
Annual Meeting of the Association for Computational
## 2672

Linguistics (Volume 1: Long Papers), pages 13999–
14013, Toronto, Canada. Association for Computa-
tional Linguistics.
## Florian Weber, Thiemo Wambsganss, Seyed Parsa Ne-
shaei, and Matthias Soellner. 2023.  Structured per-
suasive writing support in legal education: A model
and tool for German legal case solutions.  InFind-
ings of the Association for Computational Linguis-
tics: ACL 2023, pages 2296–2313, Toronto, Canada.
Association for Computational Linguistics.
## Thomas  Wolf,  Lysandre  Debut,  Victor  Sanh,  Julien
## Chaumond, Clement Delangue, Anthony Moi, Pier-
ric Cistac, Tim Rault, Remi Louf, Morgan Funtow-
icz, Joe Davison, Sam Shleifer, Patrick von Platen,
## Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu,
## Teven Le Scao, Sylvain Gugger, Mariama Drame,
Quentin Lhoest, and Alexander Rush. 2020.  Trans-
formers: State-of-the-art natural language processing.
InProceedings of the 2020 Conference on Empirical
Methods in Natural Language Processing:  System
Demonstrations, pages 38–45, Online. Association
for Computational Linguistics.
## Ruosong Yang, Jiannong Cao, Zhiyuan Wen, Youzheng
Wu, and Xiaodong He. 2020. Enhancing automated
essay scoring performance via fine-tuning pre-trained
language models with combination of regression and
ranking. InFindings of the Association for Computa-
tional Linguistics: EMNLP 2020, pages 1560–1569,
Online. Association for Computational Linguistics.
Wei Zhu. 2001.  Performing argumentative writing in
english: Difficulties, processes, and strategies.TESL
## Canada Journal, 19(1):34–50.
## A  Cooccurrence Matrix
The  cooccurrence  matrix  between  all  argumen-
tative structure levels (discourse functions, argu-
ments, components, and discourse modes) is shown
in Figure 5.
B  AdapterFusion Activations
Similar to Pfeiffer et al. (2021), we visualize the
activations of our modelmDeBERTaV3-fusion-w/-
allper layer in Figure 6 to further investigate the
influence of each level of argumentative structure
on the quality scoring.  The first activation layers
show for all five quality aspects that all structure
adapters are activated quite diversely. In contrast,
the later layers have a clear tendency towards ac-
tivating only one or two adapters.  Notable is the
similar activation pattern between relevance and
overall quality, which could come from their value
correlation.
## 2673

## Introduction
## Body
## Conclusion
## No Discourse Function
## Argument
## Counter-argument
## No Argument
## Topic
## Thesis
## Modified T.
## Antithesis
## Claim
## Premise
## No Component
## Comparing
## Conceding
## Concluding
## Describing
## Exemplifying
## Instructing
## Positioning
## Reasoning
## Referencing
## Qualifying
## No Discourse Mode
## Introduction
## Body
## Conclusion
## Argument
## Counter-argument
## Topic
## Thesis
## Modified T.
## Antithesis
## Claim
## Premise
## Comparing
## Conceding
## Concluding
## Describing
## Exemplifying
## Instructing
## Positioning
## Reasoning
## Referencing
## Qualifying
## .00.00.00.00.00.00.00.68.24.01.00.00.00.07.00.00.00.68.00.01.24.04.00.01.02
## .00.00.00.00.67.01.33.00.23.06.00.50.17.04.01.04.14.27.01.03.24.22.00.03.03
## .00.00.00.00.30.00.70.00.59.05.02.30.01.03.00.01.43.14.00.04.22.14.01.02.00
## .00.98.02.00.00.00.00.00.00.00.00.75.24.01.01.05.19.35.02.03.02.33.00.00.01
## .00.00.00.00.00.00.00.00.00.00.00.82.17.01.08.31.05.21.00.01.01.14.00.16.03
## .96.04.00.00.00.00.00.00.00.00.00.00.00.00.00.00.00.90.00.01.01.07.00.00.01
## .03.88.09.00.00.00.00.00.00.00.00.00.00.00.00.01.07.03.00.02.85.01.00.01.00
## .01.96.03.00.00.00.00.00.00.00.00.00.00.00.00.02.03.17.00.03.31.00.00.41.02
## .00.72.28.00.00.00.00.00.00.00.00.00.00.00.00.22.22.06.00.00.25.00.00.24.00
## .00.98.02.00.99.01.00.00.00.00.00.00.00.00.01.06.17.34.00.03.02.37.00.00.00
## .00.00.00.00.99.01.00.00.00.00.00.00.00.00.00.03.27.39.07.03.01.20.01.01.00
## .00.91.00.09.83.09.08.00.04.04.00.84.03.05.00.00.00.00.00.00.00.00.00.00.00
## .00.99.01.00.84.05.10.00.05.03.01.79.12.01.00.00.00.00.00.00.00.00.00.00.00
## .00.89.11.00.86.00.14.00.12.01.00.57.29.01.00.00.00.00.00.00.00.00.00.00.00
## .07.90.02.01.80.00.19.07.03.03.00.59.22.06.00.00.00.00.00.00.00.00.00.00.00
## .00.00.00.00.99.00.01.00.01.00.00.09.90.00.00.00.00.00.00.00.00.00.00.00.00
## .01.93.05.01.67.00.32.01.20.07.00.53.15.04.00.00.00.00.00.00.00.00.00.00.00
## .03.94.03.00.05.00.95.00.87.07.00.04.00.01.00.00.00.00.00.00.00.00.00.00.00
## .01.97.02.00.98.00.02.01.01.00.00.84.14.00.00.00.00.00.00.00.00.00.00.00.00
## .00.90.10.00.88.00.12.00.07.00.00.36.52.05.00.00.00.00.00.00.00.00.00.00.00
## .01.97.02.00.07.04.90.00.07.79.02.07.03.02.00.00.00.00.00.00.00.00.00.00.00
## 0.0
## 0.2
## 0.4
## 0.6
## 0.8
## 1.0
Figure 5:  Relative token-level overlap of all argumentative structure labels,  seperated into the four levels of
granularity. For example, 68% of all tokens labeled asIntroductionare also labeledTopic.
## 1
## 2
## 3
## 4
## 5
## 6
## 7
## 8
## 9
## 10
## 11
## 12
## Layers
## .28.17.30.25
## .12.61.12.15
## .08.69.14.10
## .24.39.23.14
## .35.13.15.37
## .52.03.12.33
## .16.04.05.74
## .16.10.16.58
## .02.08.10.80
## .76.03.20.02
## .04.80.00.16
## .01.01.97.02
## Relevance
## .16.28.42.14
## .13.10.09.67
## .10.16.22.52
## .06.64.12.18
## .22.04.48.25
## .17.17.42.24
## .16.09.41.34
## .27.07.21.45
## .06.06.01.86
## .08.40.06.46
## .00.00.00.00
## .28.66.05.01
## Content
## .32.24.15.29
## .40.25.14.21
## .81.07.06.06
## .24.36.24.16
## .43.26.14.17
## .24.05.27.44
## .15.05.17.63
## .11.05.10.74
## .05.10.03.81
## .40.26.15.19
## .00.80.00.20
## .01.00.98.01
## Structure
## .38.21.19.22
## .33.13.35.18
## .12.48.18.21
## .11.34.39.16
## .35.34.23.08
## .21.15.26.38
## .19.10.15.56
## .08.09.07.76
## .07.02.10.81
## .41.46.06.07
## .98.00.02.00
## .02.00.98.00
## Style
## .28.24.32.16
## .13.53.15.20
## .15.70.08.07
## .47.22.11.20
## .41.06.42.12
## .43.04.17.36
## .22.03.07.68
## .49.05.06.40
## .03.04.11.81
## .70.11.15.03
## .03.70.00.27
## .06.00.92.01
## Overall
## 0.0
## 0.2
## 0.4
## 0.6
## 0.8
## 1.0
D.Func.
## Argum.
## Compon.
D.Mode
## Avg.23.26.21.30
D.Func.
## Argum.
## Compon.
D.Mode
## .14.31.21.35
D.Func.
## Argum.
## Compon.
D.Mode
## .26.21.20.32
D.Func.
## Argum.
## Compon.
D.Mode
## .27.19.25.29
D.Func.
## Argum.
## Compon.
D.Mode
## .28.23.21.28
Figure 6: AdapterFusion activation per layer (1–12) and on average over the layers (Avg) for eachmDeBERTaV3-
fusion-w/-allmodel per quality aspect. We average the activation for each fused adapter (for discourse functions,
arguments, components, or discourse modes) over all instances in the test set of the most representative folding.
## 2674