

## Midterm — Final Project Idea Presentation
61FIT4MLA Machine Learning Applications | Week 6 | 30% of the course grade
What this is
Your midterm is agroup presentation of your final-project idea. There is no written midterm
examination this semester.
You present the problem you intend to solve, the data you intend to use, the machine-learning task
you have formulated, and how you will evaluate it. You are graded on thequality of the plan and your
reasoning, not on results — you are not expected to have trained anything yet.
The theme of the course iseducational support: machine learning that helps a teacher or a learner.
Your project sits inside that theme. How you enter it is up to your group:
•Learner-response data— predicting whether a student answers a question correctly, which topics
a learner is weak in, which questions discriminate well. This is the closest match to the labs you
have been doing all semester, and the easiest route to a solid project.
•Translation and language-learning support— error typing, feedback prioritisation, diﬀiculty es-
timation on language data. A natural fit at HANU, and the instructor’s own research direction.
•Another educational-support problemyou can find real data for. Bring it to the instructor before
## Week 4.
None of these is worth more marks than another. Choose the one whose data you can actually
obtain.
The framing rule that applies to every project
Whatever you build is asupport tool for a human teacher or learner. It is not an automatic
grader, not an AI teacher, and not a replacement for human judgement. The human remains the
final decision-maker, and every model output is a suggestion to be checked.
A presentation that proposes to replace the teacher will lose marks under criterion 5, however good
the machine learning is.
## Format
Group size   as registered for the final project
Presentation7 minutes, strictly timed
Questions3 minutesfrom the panel and the class
Slides6–8 slides, PDF only
Speakeronemember presents for the group
Submissionone representativeuploads the PDF,before 20:00 the day before
Slides are collected the night before and projected from one machine. This keeps the session to
time and removes laptop-swapping. A group that has not uploaded by the deadline presents last
and loses the delivery marks.
What your slides must cover
Six things. One slide each is a reasonable plan.
1.Problem and user.What educational-support problem are you addressing?Whois the hu-
man being supported — a teacher deciding who needs help, a learner practising, a curriculum
designer? What decision does your tool inform?
## 1

2.Data.Which data route (public benchmark, student-curated mini-dataset, instructor-provided, or
faculty collaboration)? Name the specific dataset. State its size, its fields, and itslicence. If you
do not yet have the data in hand, say exactly what you will do to get it and by when. Learner-
response tables of the kind used in the weekly labs are a legitimate and well-supported choice.
3.ML task alignment.Turn the problem into a machine-learning task. State the input, the output,
and what one training example looks like. If your labels are subjective or imbalanced, say so now.
4.Model plan.Name at leasttwo model families from this courseyou intend to apply, and say
why those twofor this task. “We will try everything” is not a plan.
5.Evaluation plan.How will you split the data? Which metrics, and why is accuracy alone in-
suﬀicient here? What is yourbaseline— the simple thing your model must beat to be worth
anything?
6.Risks and responsible use.What is most likely to go wrong? Where could the tool mislead a
teacher or a learner? What stays under human control?
How you are graded
The midterm mark is out of 100 and is split evenly:
ComponentShare of the midterm mark
Presentation of your final-project idea (group mark)50%
Completion of Lab 1 to Lab 5 (individual mark)50%
Presentation mark.Graded out of 100 against the criteria below.
#  CriterionMarks
1  Problem formulation, and a clearly identified human user20
2  Data: route, specific dataset, licence, feasibility20
3  ML task alignment and justified choice of two model families25
4  Evaluation plan, split discipline, metrics, and a named baseline15
5  Risks, limitations, and responsible human-in-the-loop framing10
6  Delivery: timing, clarity, and answers to questions10
## Total100
Only one member speaks, and the whole group receives the same presentation mark. Every member
should still contribute to the plan; the panel may ask any question about the project.
Lab completion: half of the midterm mark
Lab mark.Each of Lab 1 to Lab 5 is worth 20 out of 100. You earn the 20 marks for a lab when you
submit it by its posted deadline. Completing all five labs gives the full 100 for this component.
This is a completion check, not a quality check: a submitted, genuine attempt counts. The lab mark
isindividual. It depends only on your own submissions, not on those of your teammates.
Your midterm markis
midterm= 0.5×presentation mark+ 0.5×lab mark.
Example.Your group scores 80 on the presentation. If you completed all five labs, your midterm
mark is0.5×80 + 0.5×100 = 90. A teammate who completed three labs (lab mark 60) receives
## 0.5×80 + 0.5×60 = 70.
## 2

The midterm mark out of 100 is scaled to the 30% midterm component of the course grade. There
is no bonus and no cap: the two halves add up to the 100 marks.
## Deadlines
Group registration and provisional titleend of Week 4
Lab 1–5 submissions (half of the midterm mark)their own posted deadlines
Slides uploaded as PDF20:00, the day before Week 6
PresentationsWeek 6, in class
What you do not need yet
No trained model. No results table. No final dataset if you have documented how you will obtain it.
No language-model component — that belongs to the optional research track and is not required.
What youdoneed is a problem a human actually has, data you can really get, a task you can really
formulate, and an honest account of what might fail.
Advice from previous cohorts
The three ways groups lose most marks:
•A dataset with no task.“We found an interesting corpus” is not a machine-learning project.
Criterion 3 is the largest single block of marks.
•No baseline.If you cannot say what simple method your model must beat, you cannot later claim
it worked.
•Running over time.Seven minutes is short. Rehearse it. The panel stops you at seven.
61FIT4MLA Week 6 midterm brief.
## 3