# 10 CA ĐIỂN HÌNH BỊ DỰ ĐOÁN SAI (INEFFECTIVE FAILURE CASES)


## Case #1: Essay `5.55361E+12`
- **Prompt:** Phones and driving
- **Discourse Type:** `Counterclaim`
- **True Label:** `Ineffective` | **Predicted:** `Adequate` (P_Ineff=0.022, P_Adequate=0.962, P_Effective=0.015)
- **Target Segment:** "There are many reason on why texting while driving is very useful"
- **Lý do sai sót:** Mô hình gán nhãn đa số (Adequate) do độ dài bề mặt giống câu hoàn chỉnh, nhưng thiếu luận cứ bổ trợ hoặc tách rời khỏi luận đề chính.

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text
Phones & Driving

Should people use their phones while driving? Well 1 out of every 4 car accidents in the United States is caused by texting and driving. People are so distracted by their phones they forget about their own safety at risk while driving. While you're driving you should be more focused on the road and your surrounds more than a Facebook notification. It's not only teens that do this adults as well use their phones while driving. It is one of the leading reasons of car accidents today. Not only are you putting yourself at risk but you're putting others in risk as well. So should you use your phones while driving I think not.

Texting and driving is one of the most dangerous forms of distracted driving. In fact, the average text sent or read in a car takes a driver's eyes off the road for 5 seconds. This is more than enough time to get in a life-altering accident. Now in the matter of 5 seconds of looking at your phone you can cause yourself to getting in a really bad accident. Now if you get caught texting or using your phone while driving you can get in some trouble. Violation of the law is a misdemeanor, punishable by a fine of $25 for a first offense, $50 for a sec...
```
</details>

---

## Case #2: Essay `5181336`
- **Prompt:** Car-free cities
- **Discourse Type:** `Evidence`
- **True Label:** `Ineffective` | **Predicted:** `Effective` (P_Ineff=0.000, P_Adequate=0.038, P_Effective=0.961)
- **Target Segment:** "To provide reasonings to my strong point, brings me back to paragraph 36. It clearly states in bolded writing: ''With all these changes, people who stopped cars commuting as a result of the recession may find less reason to resume the habit....'' Furthermore, the demographic shifts in the driving population have strong trend that I can agree with. When you are fifteen, you can partake on the written and reading portion of driving and as you study your way to reach your goal, you get your permit. As you ascend your way into the online session and the real world test, you'll find yourself receiving a license as your ticket of permission to be behind the wheel by the law and by the state. Car ownership turnmoil is documented and caputred by the state due to it's nonfundamental implications that's truly not beneficial to those who rely on taking responsiblity for their actions. But if the decrease in measures that can be jotted down on paper proves that you have overestimated your duties and perogative that will not be catergorically denied before a state court or driving school. Once you lose your vehicle, it's not about banning the driving, this is about how to teach the driver on how can he or she be better the next time. Taking away driving privileges and sorts of public transportation will ease it's way to find itself in a world where nothing will be run by anyone."
- **Lý do sai sót:** Chứa từ vựng đao to búa lớn (rhetorical markers) khiến encoder chấm điểm cao, nhưng thực chất lạc đề hoặc ngụy biện so với đề bài.

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text
Cars are manufactured. They were designed to be put on this earth and be used by responsible drivers. Having no cars as a safeguarded transportable vehicle is like having your dices tossed on the dirt and you can't predict what you have. It's not define as smart decisions, this is considered by opinions. Individuals have dissimilar opinions on driving, whether it is dangerous to get behind the wheel or that it should be outlawed. Most can agree with the Mobile World Congress in the executive chairman, Bill Ford. His proper approach is to plan a business plan for a world that consider personal vehicle ownership is undesirable so they can put down emissions so it can improve safety. I don't buy it. Rejecting car culture is certainly the dumbest alternative decisions that anyone has to make. 

>>> [TARGET SEGMENT (Evidence)]: To provide reasonings to my strong point, brings me back to paragraph 36. It clearly states in bolded writing: ''With all these changes, people who stopped cars commuting as a result of the recession may find less reason to resume the habit....'' Furthermore, the demographic shifts in the driving population have strong trend that I can agree with. When you are fi...
```
</details>

---

## Case #3: Essay `AAAOPP13416000074421`
- **Prompt:** "A Cowboy Who Rode the Waves"
- **Discourse Type:** `Position`
- **True Label:** `Ineffective` | **Predicted:** `Adequate` (P_Ineff=0.022, P_Adequate=0.958, P_Effective=0.020)
- **Target Segment:** "I think you shouldn't join the Seagoing Cowboys"
- **Lý do sai sót:** Đoạn quá ngắn, thiếu lập luận triển khai; mô hình bị lừa bởi stop-words phổ biến.

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text
Lukes particapation to the Seagoing Cowboys progam allowed him to experience adventures. The one thing it didn't mention in the artical was his family where were they the whole time Luke was on board.

The artical never mentioned a mom or dad.

Was Luke alone with no communication skills.



>>> [TARGET SEGMENT (Position)]: I think you shouldn't join the Seagoing Cowboys <<<

 because you wouldn't get to see your family for as long as your with the Cowboys. Yes, it's an adventure but you could get sea sick or worse home sick. If you get home sick you may not know what to do.

You wouldn't want to go out in the sea, unboard animals then go back to main land. No one wants to do that. To many people would get sick and not want to go back on board and that would just put more pressure on you to do more work. You won't know if you have a certain amount of time to do certain things on the boat, who knows.

Luke may have loved all the adventures and great times, but that's only one person's point of view of the whole idea. You would need more oppinions in order to see if it is a good service to work for. Everybody may say joining the Cowboys is an amazing idea but others may say it's a te...
```
</details>

---

## Case #4: Essay `2021004433`
- **Prompt:** Cell phones at school
- **Discourse Type:** `Counterclaim`
- **True Label:** `Ineffective` | **Predicted:** `Adequate` (P_Ineff=0.038, P_Adequate=0.952, P_Effective=0.010)
- **Target Segment:** "Not allowing students to use there phones at all"
- **Lý do sai sót:** Đoạn quá ngắn, thiếu lập luận triển khai; mô hình bị lừa bởi stop-words phổ biến.

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text
Dear Principle

Most of the teenagers use there phones half of there life, Reconsidering the school's cell phone policy is a great idea, for many reason and some of the reasons are these. Even though you say not to bring cell phones to school students still do it , some of the students need to bring there phones to school to communicate with there parents telling them that they're at school. Other students need there phones incase of an emergency, and there parents need to contact there kids or the parents need to be contacted, the school can use there phones. It is a great idea letting the students use there phones during lunch or free periods that gives the students a feeling of trust from the school.



>>> [TARGET SEGMENT (Counterclaim)]: Not allowing students to use there phones at all <<<

 is not really going to help. The students will find a way to bring there phones to school and use them while the teachers are not looking. Most of the students are already doing it, why you think putting a new policy is going to help the school it really is not, but by letting the students bring there phones in school and giving them time to use them is going to let the students know that ...
```
</details>

---

## Case #5: Essay `AAAOPP13416000005720`
- **Prompt:** Driverless cars
- **Discourse Type:** `Position`
- **True Label:** `Ineffective` | **Predicted:** `Adequate` (P_Ineff=0.028, P_Adequate=0.952, P_Effective=0.021)
- **Target Segment:** "The Driverless people can cause problems."
- **Lý do sai sót:** Đoạn quá ngắn, thiếu lập luận triển khai; mô hình bị lừa bởi stop-words phổ biến.

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text


>>> [TARGET SEGMENT (Position)]: The Driverless people can cause problems. <<<

 Many People dies in car accident. People have to follow rules, so they can survive. If the cars is on over speed, then it can cause big accident and lot of people can died. The Driverless people can cause, accident like in traffic jam, death , like car is on over speed, and safety is important like drive in speed limit, and follow rules.

The First Thing is Accident. People don't wear the seat belts if they don't, then it can cause big problem , people have to wear seat belts. Another thing is Deaths, some people's dont the rules, sometime they drink and drive, if they sleep while driving it can hit somebody.

The Second Thing is Death. The Bridges, if the bridges are week, then it will break, so don;t drive on the week bridges. Another thing is that people like to drive fast and they just drive in the red light. One more thing is traffic jam, in traffic jam people like to hurry, so they hit on another cars.

The Third Thing is Safety. People can safe their life by drive slowly or drive in the speed limit. People neet to follow rules like wear seat belt and don't drink and drive, and it help him and ...
```
</details>

---

## Case #6: Essay `AAAXMP138200000777042125_OR`
- **Prompt:** Distance learning
- **Discourse Type:** `Counterclaim`
- **True Label:** `Ineffective` | **Predicted:** `Adequate` (P_Ineff=0.031, P_Adequate=0.944, P_Effective=0.025)
- **Target Segment:** "But Sometimes it could be a distraction from you doing all your work."
- **Lý do sai sót:** Mô hình gán nhãn đa số (Adequate) do độ dài bề mặt giống câu hoàn chỉnh, nhưng thiếu luận cứ bổ trợ hoặc tách rời khỏi luận đề chính.

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text
Home school is a benefit that anybody could have. Taking school at home would be better if you ask me, but it is not for everybody though.

Being home schooled is better then regular school because you got all day to do your work. Some people don't work as fast as others and need to work at a different pace. If you're home schooled you can watch TV and relax while doing your work at the same time, if you can multi-task. 

>>> [TARGET SEGMENT (Counterclaim)]: But Sometimes it could be a distraction from you doing all your work. <<<



For an example, If you do home school you dont have to worry bout waking up early in the morning. People like me are not a morning person. Also if you missed the bus to school and got no transportation you're gonna be stuck at home. School could be on the other side of town and walking would take too long.

Attending classes online would give you the benefit of getting through school faster. Doing home school will help you graduate 2x faster then usual if you doing all your work right. My brother was home schooled for 2 years and graduated at six-teen. Another thing is you can look up answers online to your work.

When you get home schooled you dont ha...
```
</details>

---

## Case #7: Essay `2311000707`
- **Prompt:** Cell phones at school
- **Discourse Type:** `Position`
- **True Label:** `Ineffective` | **Predicted:** `Adequate` (P_Ineff=0.035, P_Adequate=0.943, P_Effective=0.022)
- **Target Segment:** "I reconsider that are principal should let us eight graders bring are cell phones to school and allow us to use them at all time except during class."
- **Lý do sai sót:** Mô hình gán nhãn đa số (Adequate) do độ dài bề mặt giống câu hoàn chỉnh, nhưng thiếu luận cứ bổ trợ hoặc tách rời khỏi luận đề chính.

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text


>>> [TARGET SEGMENT (Position)]: I reconsider that are principal should let us eight graders bring are cell phones to school and allow us to use them at all time except during class. <<<

 I think if are principle allow us to use are phones all eight grader will probably appreciated what the principle will let us do . I think the reason why are principle wont let us use are phone is because there afraid that if someone phones get stolen or lost the school would have to be responsible for it or be in charge. Also a lot of teachers recommend us students not to use them during class or any were else, Because a lot of teachers have said that we shouldn't because if we were to use are cell phones a lot of people wouldn't be pay attention or follow direction or doing any class work like were suppose to be doing. Also i think because if we were to use our cell phones we would pay more attention to our phones then our work, and also it will be ringing and disturbing the class when most students wanna learn....
```
</details>

---

## Case #8: Essay `2021007793`
- **Prompt:** Cell phones at school
- **Discourse Type:** `Claim`
- **True Label:** `Ineffective` | **Predicted:** `Adequate` (P_Ineff=0.021, P_Adequate=0.939, P_Effective=0.040)
- **Target Segment:** "Some kids will ask there parents to transfer school"
- **Lý do sai sót:** Đoạn quá ngắn, thiếu lập luận triển khai; mô hình bị lừa bởi stop-words phổ biến.

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text
I thank policy one is better, because kids will bring cell phones to school no mater what. They will hide them from the teachers .Teachers can't go threw the students stuff any way . Just make the kids put them in there locker during class.

If you do a lot of the students will dich school any way, to be on there phones. You will just make all the kids mad.



>>> [TARGET SEGMENT (Claim)]: Some kids will ask there parents to transfer school <<<

. If you chose policy one you will make the student happy. The happier the students the happier you should be. It might help the kids, like make new friends. To do better at school not thanking about there phone, give them something to look forward to school.

Help the students have fun at school. They may have fun at school. Help them help you.

You can make school fun with policy one. We use them to pass time on the bus.

It can really help. To listen to muics on the bus, play games....
```
</details>

---

## Case #9: Essay `AAAOPP13416000005200`
- **Prompt:** Driverless cars
- **Discourse Type:** `Lead`
- **True Label:** `Ineffective` | **Predicted:** `Adequate` (P_Ineff=0.045, P_Adequate=0.939, P_Effective=0.016)
- **Target Segment:** "The future is near and the talk about driverless cars is upon us"
- **Lý do sai sót:** Mô hình gán nhãn đa số (Adequate) do độ dài bề mặt giống câu hoàn chỉnh, nhưng thiếu luận cứ bổ trợ hoặc tách rời khỏi luận đề chính.

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text


>>> [TARGET SEGMENT (Lead)]: The future is near and the talk about driverless cars is upon us <<<

. Driverless cars give us the oppertunity to save thousands of dollars in buying cars and paying for repairs. This also would be a lot more flexable than a bus because, the driverless cars could take us to our exact destination. Plus the driverless car idea would use half of the amount of fuel we use today.

The struggle we face on saving up to buy a car would not be a problem to us anymore. Multiple teens who already stress because of school have to also handle a job on top of that just to buy a car. Some even have to give up activities they love because of their jobs. Adults spend thousands of dollars just to buy cars and then have the risk of having to spend even more money when they break down to repair them. Cars are expensive items and the money we spend on them could go to other things like vacations, bills, and food.

Buses today have a certain route they follow on a daily basis. They are only capable of taking you to the closest bus stop to your desired location, this could still be a mile walk away from your destination. With driverless cars it would serve to you more as a...
```
</details>

---

## Case #10: Essay `5058061`
- **Prompt:** Car-free cities
- **Discourse Type:** `Claim`
- **True Label:** `Ineffective` | **Predicted:** `Adequate` (P_Ineff=0.039, P_Adequate=0.931, P_Effective=0.030)
- **Target Segment:** "Another cars is a bad idea is because of its gas."
- **Lý do sai sót:** Mô hình gán nhãn đa số (Adequate) do độ dài bề mặt giống câu hoàn chỉnh, nhưng thiếu luận cứ bổ trợ hoặc tách rời khỏi luận đề chính.

<details>
<summary>Xem ngữ cảnh toàn bài văn</summary>

```text
One of the advantages of getting rid of cars is traffic. Cars is a major isssue because mostly in the mornings people are tryin to get from one place to another at the same time. This action causes Death,car wrecks,etc. Bogota colombia- In aprogram  thtas set to spread to other countries millions of colombians hiked,biked,skated or took buses during a car free day to avoid traffic jams.



>>> [TARGET SEGMENT (Claim)]: Another cars is a bad idea is because of its gas. <<<

 When people drive or even crank their cars that gac or diesel is goin up into the air causing  our air to become filthy ans cloudy. Diesel or gas is dangerous because it harms the air, people, animals and other things. For example ''It's a good opportunity to take awat stress and lower air pollution'';said business man Carlos Arturo plaza as he rode a two seat bicycle with his wife.

But a good thin about this article is that it says that president obama's ambitious goals to curb the united states ' greenhouse gas emissions unveiled last week will get a fortuitous assist. So basically wat it is trying to say is that eventually a end to cars will come. Since 2005  the number of miles drive have dropped steadily a...
```
</details>

---
