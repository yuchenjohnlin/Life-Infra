---
source_url: https://www.youtube.com/watch?v=cMiu3A7YBks
source_type: youtube
title: "Adv. LLM Agents MOOC | UC Berkeley Sp25 | Open Training Recipes: LLM Reasoning by Hanna Hajishirzi"
author: Berkeley RDI
channel_slug: berkeley-rdi
video_id: cMiu3A7YBks
captured_at: 2026-04-28
duration_seconds: 4853
language: en
is_auto_caption: false
is_translation: false
has_chapters: false
chapter_count: 0
status: raw
---


# Transcript

[00:00:00] HANNA HAJISHIRZI: I am very
excited to be here today to talk about some
of our efforts in developing training recipes
for building language models, and particularly for
reasoning in language models. OK, so let me start. I want to argue that
AI is here today or we've seen all this
progress in AI because of open scientific research
and development that is happening in this area
and because we had access
[00:00:31] to fully open model. However, over time, we've seen a
lot of research and development in this area is
getting closed off. But what does that mean now? Does it mean that
now we are done with scientific language
modeling, research, and innovation? I would argue no. We need still to do
a lot of research to understand the science
of language models, to improve them, and also
build their next generation. Also, we need to make
a lot of advances
[00:01:03] to push a language
models beyond language, like in science domains
language models for health and move it beyond text. Also, we need to mitigate
their biases and risk. Use these language
models in real-world. Obviously, work on LLM agents,
improve their planning, reasoning, test-time
scaling, and also make them suitable
for deployment and build efficient model.
[00:01:30] So with that I want to argue to
facilitate innovation and also accelerate the science
of language models, we need these models
to be fully open. We want them to be transparent,
we have access to their data. We want them to be
accessible and reproducible by researchers and developers. So at UW and Ai2,
this is our focus. We like to build an
open ecosystem such that we can build language
models from at different stages,
[00:02:02] from pretraining to
post-training to mid-training and also building agents. In particular, my team
is leading two efforts called open language model,
OLMo and Tulu, which is our open post-training recipes. I also want to highlight that
this fully open ecosystem is only one piece of puzzle in
this landscape of AI these days. So with this project
OLMo, we would
[00:02:32] like to develop, study, and
advance language models. We want all our efforts to
be fully open, documented, and reproducible. And with this, we would like
to empower the AI community and also inform the public
about how AI works and so on. OK, so in this talk, I'm going
to talk about three efforts that we've done to improve
mostly reasoning and language
[00:03:01] models. And these three directions
are mostly orthogonal. And I'm going to talk about
pretraining, post-training, and inference test-time inference. And many of my slides are
from my amazing students and team members who have
worked on these projects. OK, so in the past
year or so, we have released and launched a
bunch of models and toolkits that we encourage all of you
to work and improve even.
[00:03:33] In pretraining, we have
released OLMo 1 and 2, our mixture of expert
version, and also our full pretraining data. During for
post-training, we have developed our training recipe on
top of many open weight models, such as Llama, Qwen, and so on. And also we've applied that to
our fully open language model OLMo. And also we have
all the toolkit data
[00:04:01] and so on publicly available. And most recently,
we've continued working on test-time
scaling, which we have released a S1,
Open Scholar, and self-RAG, which I'm going to very briefly
talk about those three as well. OK, so just a quick snapshot
of where results are standing is in our latest
release of OLMo2, which we have released OLMo
at 7 billion parameter and 13 billion parameter scale.
[00:04:30] The base model at the
end of pretraining, it is on par and some
data sets better, a little bit worse
on some data set, but on average on par with
Llama3 and Owen2.5, same as 13B. Importantly, we have used less
number of training tokens and we argue that OLMo-2 is on this
Pareto optimal curve compared to many other open weight
models like Qwen-2.5, Llama-3.1,
[00:05:02] and so on. So this curve shows
the average performance versus the approximate
pretraining flops. And as you see those are dual,
two stars show where to start. A snapshot of our
post-training efforts. So most recently, we have
developed our post-training recipe on top of the
largest open weight model,
[00:05:30] which was Llama 405B. And I'm going to talk
about how this process is being done in this talk. And I can show you that Tulu
3, 405B now is on par or better than DeepSeek V3 and
almost on par with GPT 4o, which is very impressive showing
that now we are getting a really good result compared to
even proprietary models. OK, so with that, I first want
to start with post-training
[00:06:01] because a lot of
our efforts on how to make these models able to
reason starts from post-training or happens during
the post-training. And I talk-- we'll talk
about how we develop Tulu along this process. So how do we build a modern
large language model. So it is roughly going
these two stages, pretraining and post-training. In pretraining, the
models are trained
[00:06:32] with predicting the next
token where data usually comes from long and large scale
data, mostly from the web. But the model that
comes out of this stage is not ready to be used
for a lot of applications. It is not safe. It's probably not able to
follow human instructions. And it's not that
good at reasoning
[00:07:00] When post-training happens, now
models can do a lot of things. It can chat. It follows instructions. You can integrate
it with tool use. It's able to reason. It's able to tell you when it is
harmful when it doesn't follow the instruction, and so on. So we do post-training to
align with human preferences. You've seen it when,
for example, you use ChatGPT, which of these
two responses you prefer. And we collect these
type of data to say,
[00:07:31] which of these outcomes are
more aligned with humans? And we do post-training
to be able to follow, to do-- to use a searching
code execution and so on. And also we do a lot in
post-training for models to be able to reason. For example, in
this case, we want to teach the model how to solve
this arithmetic word problem. OK, so how does it work? Following many standard language
modeling or machine learning
[00:08:04] pipelines, it
requires these pieces, the data that we
need to train on, a training
architecture and neural network, which in
almost all cases it's a transformer-based
architecture, and a very thorough
evaluation loop to tell us where
we are improving and where things are
not going so well. And I'm going to
talk about these are the 3 integral
parts in building
[00:08:31] a very modern successful
language model data, models, and algorithms. And during this talk, I'm going
to talk about, what type of data is important and what
type of algorithms are useful for
which type of data? So data plays a
really important role in building these post-train
models and pre-trained model. It comes from different sources
in many different forms. And they are targeting
diverse capabilities.
[00:09:03] So for example we need data
to be able to solve math word problems. We need data to build agents. We need data to tell
the model when it is not safe to respond to a query. But we need to design and
use different algorithms on deciding when to use
the right data and how-- which of these algorithms
are useful when. So this was our effort
throughout this Tulu project,
[00:09:32] which started from 2023. And now we have an open,
reproducible, and state of the art post-training recipe. And we can apply it on many
different open rate models. In the first version, which
we worked on June 2023, we pretty much only
showed, what is the best recipe to develop supervised
finetuning data or instruction data? I'm going to dig into all
these a little bit deeper
[00:10:02] in the next slides. In the second version, we showed
that how we bring and digest a preference data. And then finally, we started
doing very systematic study on, what are the best algorithms
to use these type of preference tuning data? And at the end of
these stages, we managed to show that with
only open source models, we can be as good as ChatGPT,
even upsetting GPT-4.
[00:10:32] Finally, at the end of
last year in November, we released a Tulu 3, which
pretty much put all our efforts together such that
we develop Tulu 3. And then we applied
the same recipe on OLMo showing that the fully open
training recipe also works. So what is this training recipe? So it starts from
a base model and we are following three important
steps, instruction tuning,
[00:11:00] preference tuning, and
our new novel method, we call it reinforcement
learning with verifiable reward. And sometimes we have to do
a bunch of back and forth between these
stages and I'm going to talk about how this works. OK, so let's first start getting
the ingredients to start with, which is data. So in order to do a
successful post-training, we first need to establish
meaningful evaluations for targeted skills.
[00:11:31] For example, for Tulu
3 these were our goal. We want to have a general
chat capabilities. We want our model
to be able to do to be good at knowledge, recall,
math, and reasoning, coding, and safety and non-compliance,
multilingual, and also very precisely follow
instructions even when it shows some constraints. So we developed all these
evaluation benchmarks,
[00:12:00] we decided, what type
of evaluation data set? Sometimes we also had to
create the data sets ourselves on how to evaluate if
our model has acquired good capabilities in
all of these categories that I just talked about. And we also followed really good
old machine learning techniques, which we set some of these
data sets for development and then kept some as hidden. And we just evaluated
at the end of-- when all our training was done.
[00:12:30] So given our emphasis
on these capabilities, we started collecting prompts
like queries and instructions that we think our model
should be able to answer. We checked for licenses. Are they collected
with a user consent? How the licensing work. And then make sure that
we decontaminate them with the evaluation sets
that we are evaluating on. This is very important
because we've
[00:13:00] noticed in the literature people
show some really good data sets getting really good results
on certain benchmarks. But the decontamination
wasn't done carefully because we are talking
about very complex instances and it's very easy
for some of the test sets to be different--
to be contaminated. So in our open
instruct toolkit, we have a code available
for all these cases. And it's really
useful to follow this. OK, so now that we
have the ingredients,
[00:13:32] we want to go through
the first step, which is instruction tuning
or sometimes called supervised finetuning. What does that mean? It basically is a
very simple step. It takes a lot of these
prompts and completions and then fine tune a
pre-trained language model to be able to
follow these instructions. So for example, we can
have a queries like answer these questions one by one. Summarize this talk like many
of these type of questions
[00:14:03] and then the final answers. But how do we curate this data? How do we source this data? We can have and source this data
through human annotation, which obviously it is costly,
it is time-consuming, and also it has high
variance right now. Sometimes, particularly
in tasks like reasoning, we are dealing with
complex annotations. And it might not be well
suited for general annotators.
[00:14:31] Another approach, which we
introduced in our 2023 self and strike paper was to
synthetically generate these data with self-loop
or self-instruction loop with another language model. So synthetic data generation. And obviously, it is good. It's really good
in a lot of cases, but it's going to
be noisy as well OK, and it is biased to
the language model that we are generating
this data from.
[00:15:01] And most recently, we've
discovered the optimal solution is combining both of
them, which we build a hybrid collection of data
coming from human annotation and also from synthetically
generated by other language models. So data curation has
been received well within the open
source community. We had some earlier
work in 2022 on,
[00:15:31] we called it natural
instructions and supernatural instructions where we only
focused on NLP relevant tasks where we were looking
at tasks-like question answering, summarization,
translation, and so on. Then we developed the
self-instruct, a framework where we generate data synthetically. This has picked up really
well within the community. Many next efforts have been
introduced within the community to generate more and more
synthetic data sets like Alpaca,
[00:16:01] Vicuna, and so on and so forth. We also have a very
good collection of data sets that are mostly
focused on short form question answering type tasks,
like for MV1 and so on. So I'm just listing a few
of these data sets here. For the full set, please
check out Tulu 3 paper. We listed a lot of
publicly available data sets, either manually
curated, expert
[00:16:32] curated, or synthetically
generated wider community. And we combine a lot of them. Use the ones that we saw
most signal out of them in to build our final SFT mix. OK, so now we have looked at all
these data that are available. And now, we are doing these two
repeated parallelizable tracks where we collect this data. And now we want to
mix them such that we
[00:17:01] get high accuracy in the
capabilities that we care about. This requires
substantial effort. Why? Because, for example,
if I add a lot of data about form generation,
probably my math reasoning capabilities drop. If I add a lot of data
on math reasoning, probably I would lose
this creative task like poem generation. So it's a pretty
challenging task to keep a good balance
of all these data
[00:17:31] such that we are getting high
accuracy across the board. So we are exploring and
also in the community people are exploring
many different ways of this data mixing including
manual empirical analysis, automated mixing. And I think the
literature is evolving and there are a lot of active
research going on in this area. OK, so let me show you
some of our efforts
[00:18:03] and how we did this data
mixing in our Tulu 1, which was very simple. There were not much
data available in 2023 such that we start doing
all these combinations. So first, we combined all
available open data sets that were available back then. And I'm listing
them on the left. And some of them are created
by humans, general public,
[00:18:31] or experts. And then some are synthesized
with some of the most successful language models back then. Then, similar to what
I just described, we started looking at
evaluation sets or data sets targeted to evaluate
certain capabilities. For example, this is the
outcome of our finetuning when we were evaluating on
chat type evaluation sets.
[00:19:01] And here are how
the results compare. The red ones mean the
results are not that good. And then the blue ones show,
OK, successful results. As you see here,
that GPT4-Alpaca shows good high results
on chat type evaluations. ShareGPT also showing good
results on chat evaluation. So we did that across
many different verticals knowledge, reasoning, coding,
multilinguality, and safety. And some of these results
are quite exciting.
[00:19:30] For example, when we train
with chain-of-thought data, we see higher numbers on
reasoning type evaluation sets. OK, so now the question
is, how do we combine them? How do we take the best
of all of these worlds? Because as you saw,
this data-- actually let me go back here--
this data like shared GPT, or self-instruct,
or like I would say, open the system one
that is good in chat,
[00:20:01] they are not that good in
knowledge or reasoning type test. So it is important to get
the best of all these worlds. So we try to look
at the data sets that show high numbers
across one of these verticals and I started combining them. And as a result, we have a
human plus synthetic type data. I want to highlight that we saw
really good results with shared GPT early on, but we
later dropped this data because license and the
way the data was collected
[00:20:32] was not that good. So we dropped this data
in our next versions. OK, now with the
emphasis on reasoning, I want to dig a little bit
deeper on, what type of data, particularly is
useful for reasoning? Why is this challenging? Let me give you a math example. We want to solve this problem. The question is you
can read this here. A store has buy 2 get
1 free deal on shirts. Each shirt costs $25.
[00:21:01] If Sarah wants to buy 7 shirts,
how much will she spend? So one quick thing could
be, OK, I have this problem. The final answer is $125. It's pretty easy to come
up with that number. However, if I just
fine tune a model with this input-output
setting, probably I won't get that much out
of this training instance. So we all observe
in the community that it's really better if we
start integrating and using
[00:21:33] this type think
chain-of-thought output where we say we're going to
break this down into, OK, step one, do this, step two, do
this, and then break this down as if you are
explaining it to a child how to follow these steps to
come up with that final number $125. So why do to summarize,
why do we think chain-of-thought data is
helpful for reasoning. It's helping the model to handle
complex multi-step problems much
[00:22:03] easier. It also starts revealing the
model's reasoning process. Also, one thought is
a lot of these models during pretraining have
seen a lot of this type think chain-of-thought data. And then this starts
to boost them up, to boost this capability
up of saying, OK, remember, you knew how to
think step by step. Bring them up when you are
looking at these more complex
[00:22:32] math reasoning problems. Also, when we look at
these type of annotations. These type think
chain-of-thought data makes it much easier to spot
errors in the logic and also it resembles how we
are explaining things to humans or how humans
thought process work. OK, these are all
very good points about why this type think
chain-of-thought data is important. However, it's becoming more
and more challenging to observe
[00:23:05] and obtain manual annotation
for this type think chain-of-thought data. It is time consuming. It is very expensive. and it often requires
expert annotation. The example that I showed in
the last slide was quite easy, but think of more
challenging math problems. We need experts
to annotate those. And obviously, it is
difficult to scale.
[00:23:31] And also it is not
diverse enough. It is very hard
to boost diversity with all these
limitations that we have when we want to
collect this type think chain-of-thought data. So again, our approach
to address this solution was hybrid data
curation where we look at data mixing
and also selecting from existing resources. We also did some very-- observed a very interesting
paper from the literature
[00:24:03] where they proposed to
use different personas to generate diverse data. So I'm referring
to this paper here, but the idea is we're going
to look at different skills, for example, math coding,
precisely follow instruction. But then we devise
different personas, and then we ask the
model to generate data
[00:24:31] for those skills, given the
persona that it is looking at. This would ensure high diversity
and enables us to scale further. What does that mean? So we develop this prompt. We say we want to create this
data with this specific persona in mind. For example, we want to
create a math problem given that we are creating
it for a chemical kinetics researcher.
[00:25:01] And now the problem
looks like this. Dr. Smith, a chemist, is
studying this and so on. Or we say we want to solve
this logical reasoning problem, again,
for that persona, for that chemical
kinetics researcher. We tried many
different personas. We designed this
type of math problems for experts, for children,
six-year-old children, or a computer
scientist, and musician.
[00:25:32] So you give many different
personas to the model, and then we ask the model
to generate it specifically designed for that persona. With that, we created more than
150k hard math problems and 50k grade school math problem. We created 35k Python coding and
precise instruction following. Then these were mostly
for generating prompts
[00:26:01] because this was the point
of boosting diversity for the types of problems
that we are getting. Then we used a combination
of GPT-4o and Claude Sonnet to generate a step
by step solutions, for example, for a given
math problem, a coding or precise
instruction following. OK, so now let's
look at the result. How successful and
useful these data are? OK, so let me walk through
how we read these figures.
[00:26:34] So in the figures below, you
are seeing results on two data sets math and GSMK8, which are
due to popular math data sets. Then each of these
bars show a combination of using our public data
sets, like the data sets that are available, for example,
for math or general purpose,
[00:27:00] combined with this
persona-driven synthetic math problems. And we varied the amount of
these persona-driven math data in our experiments. So the first bar,
the yellow bar just uses the general public data. And the last bar does have a
50-50 between persona-driven data and then general data. And as you see, over
time, we see improvement
[00:27:32] mostly on the math. On GSM8K, we saw
less improvement and we think the
reason is because GSM8K are simpler math word problems
like grade school math word problems. And we think the available
public data set were already good enough. So that's why we
didn't gain much. So to summarize, adding more
persona-driven data consistently
[00:28:00] improves math performance. GSM8K improves,
but it's much less and I kept a balance on how
to use this type of persona. OK, so we did another
step to filter the data. How do we do that? For every word problem
or every instance that was generated
synthetically, we actually went ahead and
asked GPT-4 to generate
[00:28:33] multiple reasoning paths. And then we basically
did self-consistency. So in one of the
classes earlier, I think this semester
or last semester, you learned about
self-consistency. And here is what we used. And then we basically saw,
which one has majority vote and kept those reasoning paths
that gave us that better answer? So through this, we managed to
filter a lot of data, almost 40%
[00:29:05] of the data. And now, we are seeing that
using only 60% of the data, we are getting similar
performance on math. This new pink is the
filtered process data, which is almost on par. I would say this is just
error bar on how different they are from the original mix. And we saw more significant
boost on the GSM8K,
[00:29:31] highlighting that with
this better filtered data, we are getting higher
accuracy on GSM8K. So at the end of
the day, now we are able to use this 60%
of the data and we are getting good performance
from this synthetically generated data. OK, so there are
many other approaches in the research community to
generate chain-of-thought data. One is obviously manual
human annotation.
[00:30:01] As I mentioned this is great. This is very accurate,
but we can pretty much have a limited scale. And sometimes it is hard
to increase diversity in the reasoning style. And there are methods that
they convert math problems into Python code and then
generate solutions that way. This is great because it
guarantees correctness through execution. The only issue, it's a little
bit less natural language
[00:30:32] reasoning, the same way that you
are explaining it to a child. So somewhat less intuitive,
but it's still very interesting and it works really well. And also this type of
self-generated chain-of-thought, which is scalable
to many problems, the quality of the model really
depends on the base model. And we did a combination
of all of these methods. OK, so putting
all this together,
[00:31:02] so I talked a lot
about how we created and curated these synthetic
data for math and reasoning. Then we put all of these
together and built our data mix for supervised
finetuning and this is the outcome, which
is the combination of human and synthetic data
and we finally built Tulu SFT. So let's discuss a
little bit of results. So this table has
a lot of numbers,
[00:31:31] but I want to show some of
the ablations we've done. The columns show
many different data sets that we evaluated
on like MMLU, TQA, PopQA, and they are all evaluating
some of those core skills that we cared about. And this is our final
results on the final SFT mix that we discovered. And these are some
of the ablations. For example, if we
remove wild Chad, which
[00:32:00] is our data mix to approach
general chat capabilities, our average will get into
58.9, with probably the biggest drop on, as you see here
AlpacaEval on chat evaluations. Or without the
persona data, we get to 58.6 where we saw drops on,
for example, math, and so on. Or math data, if
we remove that, we see a really significant drop
on this type of math evaluation.
[00:32:34] Another thing that
we were very careful was we want to make
sure our model is safe. So we added safety data. But at the same time,
we want to make sure that it doesn't drop
the capabilities, the general capabilities
of the model. And this is what we've observed,
that adding safety data doesn't hurt general
capabilities of the model. This is also comparing
the Tulu SFT data
[00:33:01] with the other data sets that
were available in the community like mammoth data or RLHF. These were some of the
most popular data sets that existed in the community. And this is the gains that
we are having for the 656. And these were our earlier Tulu
2 SFT is like our earliest data mix in our earlier versions. So in overall, we argue that
this is a really good SFT mix. A lot more can be done here.
[00:33:32] And it's really good if people
in the open source community also start improving
this data mix. OK, so step one is done. We took our base model and
then did supervised fine tuning with a very carefully
curated data mix. Next step is
preference tuning where it works with a reward model. OK, let's see what happens here.
[00:34:02] So at the preference
finetuning stage-- I think Jason also
talked about this-- the goal is we want to
align to human preferences. For example, we have this query. We say, write a haiku about AI. It talks about the model
comes and outputs something. We want to give thumbs up,
thumbs down if the output seems good or bad. But in practice,
what we've observed,
[00:34:32] the role of
preference finetuning is to show a very strong
training signal to make style, to have a better style of chats. And it shows really
higher improvements on chat type evaluation. It also keeps improving
the basic capabilities that we were targeting. But in general, we saw
lower absolute magnitude of improvement,
for, for example,
[00:35:02] math type capabilities So let's
dig a little bit deeper how the preference data looks like. So we have this prompt. Let's say explain
the moon landing to a six-year-old
in a few sentences. We want our model to
generate two responses And then the preference
instance tells us one response is better than the other one.
[00:35:30] And it can be
annotated by humans saying that this response
to me seems much more suitable for a six-year-old. Most recently, people look at
this called RLAIF where instead of humans, we can
have another AI model, let's say GPT-4 or
Claude Sonnet or so-- to evaluate which of
these responses are better for a 6-year-old. And then the algorithm to update
that at some level sometimes
[00:36:02] it's called RLAIF. So this is the nature of data. Why does this data play an
important role in building and post-training stages
is in a lot of cases, we are dealing with
open-ended generations and have coming up with
some absolute numbers to say oh, OK, this
response is good, is hard. However, it's much easier
to deal with comparison
[00:36:31] to say this response
is generally better than the other one. So the task of annotation
has become much easier. But then we cannot use the same
supervised finetuning algorithm to deal with this type
of preference data. Now, let me unpack RLHF
or reinforcement learning with human feedback. How do we integrate and use
this type of preference data? So we will use
reinforcement learning.
[00:37:03] How does it work? This is the most generic form. The idea this is the most
generic definition of RL. The idea is for a
given policy, which is generate the next token,
we generate this next token, we interact with an
environment, we get some reward from the environment if that
generated token was good or bad, and then update the
state of the world. In RLHF, the state is getting
updated from the prompts
[00:37:34] that are getting
fed into the policy. The action is updating and
finding what responses are. And then the
environment is actually a reward model where it
tells us how good a model-- tries to up a model
that preferences that this response is generally
preferred over the other one.
[00:38:01] So this is of how RLHF works. This reference data will fit
into a reward model, where reward model is actually
a neural network that is trained to tell us, for a
given prompt, which response is better? OK. How do we optimize this complex
situation through PPO training? Let's dig a little bit deeper. The idea is we want to
maximize the reward.
[00:38:31] We want to get the maximum
reward as possible such that we want to constrain
the model to stay as close as possible to the baseline model. We want the policy to don't go
that far from the originally trained model. So this is establishing
a very important balance between make sure you are
aligned with those preferences that are provided to you. However, don't go too far
from the original model
[00:39:03] that you have in mind. Now, in the last year or
so, many different variants are introduced on how to
optimize that objective. So last year, we had this
paper called direct preference optimization or DPO,
where the idea is, what if we just use gradient
ascent on this equation? OK, let's ignore all that.
[00:39:31] Now, we have this
reward model and then we want to optimize
for that reward. Let's directly optimize
for these human preferences and then model it
as a ranking model. So how does the
DPO training work. It's like this where we remove
a lot of these details here. And we directly go from the
preference reference data into policy. And then given that
reference model,
[00:40:01] we want to see how
close this preference data is to the policy. So many new variants of
GDPR also introduced. So here I'm summarizing them. This is the PPO, the
original formulation. Here is the direct preference
optimization, which directly optimizes the policy. Given the preference data, I
would always say think of it as some ranking objective,
and then the newer variants like, which even makes it more
simplified where it doesn't even
[00:40:34] use a preference-- a reference model, another
variant like length normalized PPO, which normalizes
the same log likelihood, but make it normalized
for the lengths. So in this work, we started
actually digging deeper into all these
algorithms that exist.
[00:41:02] Particularly, we looked at
comparing between DPO and PPO. So they are all different. They are getting different
types of parameters. They have different
implementation complexity, memory usage
throughput, and so on. Just to give you a very
brief idea, in general, we saw PPO performs better
than DPO in almost all cases. However, it is much more
complicated to implement
[00:41:31] and make it work, particularly
for larger models. Why? Because at P for PPO, we need to
have two models running like we. We have the reward model as
a neural network and also the policy model, which
is the actual language model that generates token. So it really depends on
the developers preference on which constraints they have. OK, so let me dig a little
bit deeper and tell you
[00:42:01] what things we ablated to
figure out which model to use. OK, for DPO, remember,
we had preference data and policy model. For PPO, we have all these
components, preference data, the type of reward model,
and the neural network that we have here. We have the generations the
prompts and the policy model. So I'm showing
the final results. I'm not going into
a lot of details. But here are the results.
[00:42:30] Let's say this is the average
performance on a lot of tasks that we've looked at. This is the initial
SFT result. When we do DPO with some
weaker preference tuning, we saw 2% boost. When we do a lot of ablations
and very careful curation of preference data, we
saw significant boosts. Look at this, we
go from 56 to 61 just with better data selection
and data curation here.
[00:43:02] Then we replace the DPO
with PPO we saw now we just use the exact same data. We just replace the
algorithm, DPO with PPO, and we saw one point boost here. Then we thought, OK, now
this is very promising. PPO is great. Let's now think of a
bigger reward model. Because remember, a reward model
plays this environment role and we try to make our
model as close as possible
[00:43:30] to this preference data. When we started using
a bigger reward model we didn't saw that much
improvement, less than about half a point improvement. And then finally, when we
started mixing prompts of, what type of specific design
prompts for some tasks? On average, we
didn't see much gain. However, I want to highlight
that this final step on average
[00:44:00] didn't show us a
lot of improvement. But very interestingly, when
we only focused on reasoning, particularly GSM8K, when
we started bringing up prompts that are very useful,
like for improving the reasoning capabilities, we saw significant
boosts here that here we learned when we introduce prompts that
are domain specific for some of those capabilities, they
play a really important role.
[00:44:30] OK, so if you look
at this whole thing, this was the choice
of algorithm, this was the choice of
data, algorithm model data. So again, we saw a
really big boost on data. So takeaways from this. The most important
factor in building a really good preference
tuning algorithm for us was high quality data. PPO works better than DPO. But DPO is much
cheaper to experiment
[00:45:00] with and do a ablations
on data, and it's more practical for development. Scaling RM reward models
help, but not significantly. Using in-domain prompts
yield performance gains, particularly for domains
like [INAUDIBLE]. OK, so now we put all
of those together when we want to build Tulu 3. So from our last study, we
learned prompt selection
[00:45:31] is really important. So we looked at many
different combinations on how to curate data. And this was our best mix. We want to use
some of the prompts that we already used in SFT. We thought this is
really good to maintain accuracy and performance. We also brought some
prompts, some new prompts that we hadn't
seen during SFT. And then we started
bringing in out of domain prompts, for
example, from domains
[00:46:00] that we did not study in SFT. OK, so we then did a lot
of response generation from all these models. So we had some weaker models
like 7B models, llama 7B, for example, almost 7B all the
way to very models like GPT-4 or because we want to look
at the preferences to see, which of these outputs
are more preferable?
[00:46:31] Importantly, we
brought on-policy data. Remember, we want to
improve our Tulu 3 SFT. This is the model. This is the policy model
that we want to improve upon. So we made sure to bring some of
these data points and these Tulu 3 completions such that we can
say this outcome is preferred over something worse or we
need to get to something better, which is, for
example, the outcome of GPT-4.
[00:47:01] So we also show that
it is important to use this on-policy data. Then we did
particularly RLAIF where we asked GPT-4 to tell us, which
of these completions are better? And we ask it to measure
across these four categories, helpfulness, instruction
following-- how accurately it could follow instructions--
how truthful, and how honest
these responses are.
[00:47:30] And then we binarize
them according to-- and then said, which is
chosen, which is rejected. To optimize the algorithm
for optimization, we did a DPO, PPO, and CPO. Again, similarly, we didn't
see much gains from PPO. And for simplicity, we
stick with DPO for this. OK, so here are
these bottom figures show some of our ablations. So actually let's
look at the most--
[00:48:01] the right-hand one, which
is what LLM as Judge we used for telling
us, which is preferred? Which is rejected? And we looked at many different
highly capable models like GPT-4 or Llama 4 or 5, and so on. And we saw a little bit
better results on GPT-4, and that's what we stick with. This middle figure
evaluates the off-policy
[00:48:32] versus on-policy preferences. And as you see, this is the
initial SFT with off-policy. We got to 60 adding on-policy. Only with on-policy we get 60.7
and then combining all of them, we got the best numbers. Here, we also checked
if it is useful to bring in new out of domain
prompts or we just
[00:49:00] reuse some of the prompts that
we had from the initial SFT. And as you see again,
bringing new prompts also improves results. OK, so what happened up to here? We did all our instruction
tuning, supervised finetuning. We did our preference tuning. And now I want to talk about our
third step, which we introduced as part of our Tulu 3 effort,
reinforcement learning with verifiable reward.
[00:49:35] OK, so let's look
at these curves. At the end of DPO or
preference tuning stage, I'm going to show you
these three figures. So this is training
steps on the x-axis. And on the y-axis,
we are looking at evaluation performance. And as you see over time, for
example, in the AlpacaEval,
[00:50:05] we see the improvements are
almost getting plateaued. For IFEval, which is how we
do instruction following, interestingly, we see when
we increase the training steps in for our DPO, we see a
little bit drop in performance. And for GSM8K, which is
our proxy for reasoning,
[00:50:31] we see initial improvement. But then after some time, we
started seeing overfitting and then dropping performance. So particularly, for
these more complex tasks like following instructions
and doing reasoning, over time we see over
optimization is happening, which is not good. Then we started thinking
a little bit about this. We are using this
neural reward model
[00:51:03] to tell us if some
preferences are good or bad. This neural network tries to
assign a score to every instance now. OK, so it tells us for
this give this reward model is trained to
tell, which is chosen? Which is rejected? But at the end of the
day, for every completion it tells us, what is the
score of this completion?
[00:51:31] For example, for something like
this, for some prompt like this, it would give us
this score of 10.5. If we change the input, it
might give us another score. Also there are studies
in the literature that this human feedback that,
OK, this A is preferred over B is not the gold standard of
saying what is the outcome? What is a good reward score
for this sentence, for example?
[00:52:02] Instead, we thought
for tasks that we can verify their correctness,
we can use a much, much simpler reward model or in fact, we
can replace this reward model with something rule-based. For example, if my query
is, what is 2 plus 2? We can easily say if
the answer is gold, return 1, otherwise return 0.
[00:52:31] If we were only using
that neural reward model, it might have given us another
score like 1,000 or it might have given us something
like, I don't know, 5.5. What is the intuition or what
is the meaning behind that score that the reward
model is giving us? So that was a very
question this. And then we said
for tasks that we can verify their final
outcome, what if we just remove that complex
setup and use a much
[00:53:02] simpler rule-based model. And this is exactly what we did. So let's look at our RL setting. The prompts come in. The state gets updated. The action are
generating next tokens. And then this reward
model tells us, what is the good outcome or what
is the good score associated with this generation? However, in problems like
math that we have ground truth answer, we can have this
verification function
[00:53:33] where the reward tells us, one,
if the final answer is correct, 0 otherwise. Pretty much we had
that for GSM8K, which is one of
our reasoning evals MATH and also precise
instruction following. Let's imagine we are giving the
model a bunch of constraints, make sure to start the
sentence with S then-- or to write a poem
that has five words.
[00:54:00] So you could verify if the
generated outcome follows these constraints or not. And then we can evaluate
how-- we can easily verify how good the
generated outcome is. So that was pretty
much what we did. We replaced the reward model
with the verification function. And the DeepSeek R1 model that
released earlier this year
[00:54:31] also is using
similar thing, which I think they call it a
different name, but a very, very similar intuitions. OK, to summarize,
this is our setup. We use gold final answer
or verifiable constraints as this environment, as
a proxy for environment. This is good because
for this we don't need intermediate chain-of-thought. We just need a final answer.
[00:55:01] Then we applied
classical reinforcement learning algorithm
to optimize this. And here we used PPO
for the optimization. And we tried it for three
data sets GSM8K math and if verification and
we show the results. Roughly, this is the number of
training instances that we have used almost in
the order of 110k. We also evaluated on big
bench heart, which is also
[00:55:32] roughly reasoning type task. And then we found that this
data set could be a good proxy to give us boosts on BPH. Some of the verification
steps are very easy, like math and reasoning. It's pretty much just
this if then else, which is if prediction is equal
to this number, say yes, otherwise zero. Some of it, for example, for
constraints and constraint
[00:56:01] satisfaction and
verification, it's a little bit more challenging
because we want to see, which of these
constraints are satisfied? And then we see, which
percentage of those constraints are satisfied? But in general, pretty similar. Pretty easy. So now, let's look
at the curves. So I'm just showing
this whole graph. But now let me go a
little bit deeper here. OK, so what does
this curve tell us? So on the x-axis, we
see the training steps.
[00:56:34] And on the y-axis, we show
the GSM8K, the math reasoning capability. This dashed green
line is the outcome of the supervised
finetuning model. The pink one is the
outcome of the DPO model. OK, so we applied a
RLVR at two stages just to see if it makes
improvement both at the end of supervised finetuning
and also at the end of DPO.
[00:57:01] So what do we see? This is interesting curves
show results are going up. We don't see that much over
parameter optimization here. The gains on top of
SFT is much higher. But the biggest gain
or the highest number is achieved by when
we apply it on DPO. Same things on math. Again, at the beginning,
we saw a little bit drop when we started with
DPO, but then, again, I start to see improvements.
[00:57:32] IFEval, which is the
verification and the constraint optimization like
instruction following. When we start from SFT,
we saw significant gains. On DPO, we saw less gains. We are still
investigating on this, but we think the reason is
we did not have enough data. And interestingly,
when we use VLAN data-- just to see, this was
if we did not finally
[00:58:00] include this in our RVR mix. But it was an interesting
observation just to see that doing some
reinforcement learning on VLAN, it shows some improvements on
some of the reasoning tasks. And it's worth exploring
this much more. And we are doing it
just seeing, what other types of verifiable
tasks out there such that we can apply RLVR on that? OK, we also applied the
same recipe on almost two
[00:58:31] and we can build upon this. This is actually a very
interesting setting. We stacked a bunch of
reinforcement learning steps one on top of each other. So here we started doing a bunch
of training and we cut it here. This is the average score. And then, again, it started
a little bit another step. And then another stacked
multiple RLVR and then did multiple stages. And over time, we saw
even more improvement.
[00:59:02] So the pipeline is there. We can do multiple
trials with this to see if we see
bigger gains or not. OK, I want to take a step back
and then talk about this thing. RLVR is not really new. This is actually the simplest
way of using RL with the data. But why did it work now?
[00:59:30] We realized it's because and
now base model qualities have improved a lot. Therefore, RL can
boost upon them. So what does this curve show me? So these are training steps. This is the accuracy. And the green bar
shows when we do RLVR applying on GPT-2, the
model that existed long time ago, which was really bad. So the original number,
the base numbers
[01:00:00] are very low unlike some
of these reasoning tasks. Therefore,
reinforcement learning didn't show improvement. However, because now our
base models are improving, then applying RLVR on top of
them shows significant gains. And this is very interesting to
observe because now model can start exploring more
and then exploit it once it sees it is
following with the reward, with this rule-based reward. OK, so putting
all this together,
[01:00:30] we scale this up from
7B to 70B to 405B. And this is our
results how it looks. And the pink portion, you see
the results of model applied on Llama 405B at the-- Here are the results of SFT,
DPO, and the final out of RLVR. Again, this is the
result comparing with DeepSeek V3 and GPT-4
or the latest version.
[01:01:00] On average, we are
very close to GPT-4 or better than DeepSeek V3. And it's a very exciting area. Here are showing our results
on 8B and 70B models, again, comparing with open rate models
like Qwen instruct and Llama instruct strike, which like
better significantly and also at 70B where the smaller
model are also comparable
[01:01:30] to the smaller size of GPT-4,
or mini, or cloud haiku. OK, one other
interesting observation was RLVR works better at scale. So here shows our improvement
on math in two cases. Oh, I didn't put legend. So here on the left-hand side,
you see how much improvement we see on a 70B model. And this is how much improvement
we saw on the right-hand side.
[01:02:03] You see how much
improvement we saw at 405B. And as you see here,
we started from 60. We went all the way to 67,
7% improvement on math. Whereas at the 70B scale
we go from 42 to 45. So it was interesting and
aligned with our hypothesis that when we have
better bass, we can start seeing a
lot more improvement during this RLVR step.
[01:02:32] So we are exploring a lot and
we know the community is also exploring a lot in this setup. For example, we have changed our
optimization algorithm from PPO to GRPO, which I'm not going
to go into the details. But now here are our
significant improvements. So as a reference,
Tulu 3 405B has 67%. And now, when we apply
our recipe on Qwen math
[01:03:04] model and then we apply GPU. Now, we are already getting
84.6, which is very exciting, shows a lot of progress
can be done in this domain. OK, so this is it. So these are putting together
all our Tulu 3 recipe. I first talked about
how we got ingredients ready by collecting data. Then we have different types
of data at different stages
[01:03:33] and we showed how we do
supervised finetuning or instruction finetuning
preference tuning, which we looked at the
preference data, and RLVR, which we just looked
at this verification step. And then putting all these
together, we have Tulu 3. Here is the model. We also have the
demo of the model available in
playground.allenai.org where you can play with this.
[01:04:00] We are using this
data to improve the next version of
the models and improve capabilities of Tulu 3. Also, all our code data and
the pipeline and the framework is ready. So whatever post-trained
model or adapted model you want to build, we
argue it's really important to bring in some of the
general capabilities to get better model. So I would encourage
you to use that data.
[01:04:32] OK, so this is a fully
open post-training recipe. We have applied it
to Llama-based model, Qwen-based model, and
also on our own OLMo models, which shows significant
boosts on the OLMo-based models as well. OK, so with that, I would end
my discussions on post-training. And I want to very briefly talk
about test-time inference, which
[01:05:01] is a very popular
topic these days. And a lot of people
are looking at how to bring in test improvements,
particularly in reasoning during test-time inference. So I first want to talk
about this paper called S1, which is led by
amazing Niklas Muennighoff. And it is actually the very
minimal recipe for reasoning and test-time scaling.
[01:05:31] So let me tell you how it works. Very similar to almost
everything else that is happening in
language models, it relies on really
carefully curated data. We call it s1K. Then we apply test-time scaling
algorithm, a very simple one and this is the outcome s1. OK, how do we curate data? We looked at a very
large collection
[01:06:01] of math, logical reasoning,
probability questions, and so on, more higher
level reasoning data. It's even beyond the Tulu
3 data where we mostly looked at grade
school and math, which was high school, a little
bit college level math. Here we are looking at much
more complex, like Olympiad math competition type data. So we looked at all these logic
puzzles math and we collected
[01:06:31] 59K question. But then we did a lot
of filtering here. We filtered for quality. We got into 52K data. We picked the ones that were
more difficult and then we moved to 24K. And then we emphasized diversity
and we removed the ones that they were very similar. We ended up having 1K. So spoiler alert, on our
benchmarks using 59K data and 1K
[01:07:01] data almost similar,
which is very interesting. So once we collected
these prompts, we started to distill
reasoning traces and answers. So for example, when we
have a problem like this, we gave this problem,
which is among our S1 data. And then we annotated the
reasoning chain-of-thoughts with Google thinking
Gemini model.
[01:07:31] And also we made sure
that this data also includes some of the
thinking tokens like, OK, this happens, but
let me think more. And so on. So we use this Google
thinking annotations. And most recently in S1, we
replaced Google Gemini result annotations with
DeepSeek r1 results where it actually improved
the final results, which was very interesting to see. OK, so this is the final
collection of data.
[01:08:03] The data varies across all these
domains from geometry number theory to even various smaller
portion on control theory, astronomy, and so on. OK, so this is the
data, test-time scaling. The simplest method possible,
which made all of us very surprised and excited where
we focused on budget forcing, where we have a
question like this.
[01:08:31] How many hours are in raspberry? We let the model
generate the response. But then if it didn't hit
the allocated token budget, we added a token called
weight and then let the model generate and basically force
the model to generate more in order to respond to that. We are using this weight token. We are hinting the model
that we are not sure if your answer is correct.
[01:09:01] So one more thing to add. We did not train a model to
decide when to add weight. We naturally added weight when
it didn't hit our token model. And then we let
the model generate more until the final answer
is achieved is obtained. OK, so now training and results. we trained a Qwen 32B
model on this data. And here are our results. On the x-axis, we
are seeing the number
[01:09:32] of tokens, the
average thinking time or the number of tokens that are
generated and then the accuracy. So when we push the model
to just generate 512 tokens, here is the accuracy, it's 65. One more thing. If the model wants to generate
more tokens than the budget, we put end of token there
or end of a sentence there. So with that, we
control the generation.
[01:10:02] So we go from 5 to
2048 for MATH500 data. And as you see over time
with more generated tokens, we see this scaling trend. On this Matt
competition data, which is much more challenging
data, we even want the model to generate
longer and longer token outcome. And as you see here, we
see, again, the same trend.
[01:10:31] And also PhD level
GPQA demand, again, generating longer and longer
tokens, which is very exciting. So zooming in here are a
little bit of how it works. I explained it already. So when the model wants
to generate more tokens, we pushed end of sentence to
be able to get these shorter sequences. And when we want the
model to generate longer,
[01:11:02] even go beyond 8,000 tokens, we
push this away token and force the model to generate more. We compared different types
of test-time scaling methods. Here are the budget forcing. This steeper curve shows the
budget forcing or sequential scaling. We also did parallel
scaling via majority voting
[01:11:30] where we let the model
generate multiple paths and then do majority voting
or the self-consistency check. And we saw some gains,
but not that significant. So this budget forcing
seemed much more successful and much simpler. So here are some
of these ablations that we have done in the model. So this is the final results
on the left-hand side of S1K on all those
three data sets.
[01:12:00] Comparing with full collection
of data like using 59K, we see that a little bit higher
numbers we get with the full data on AIME, but in other
cases pretty much similar. And our S1K data is
really high quality. If we just use random or just do
a bunch of constraints to find that 1,000 data points, the
results are much, much worse.
[01:12:33] We also did a bunch
of scaling ablations when we don't increase any-- let the model to train longer. This is the best number. So these are the gains
that we are having with this test-time scaling. If we replace the
weight with other tokens alternatively or just let the
model generate without adding any strings, we saw less gains.
[01:13:02] OK, so these are our results
for test-time scaling. I also want to highlight
two other approaches that we have been cooking up over time. And the idea is-- and I'm not going to talk about
any details on these next two methods, but the idea is
we want to be very aware and do self-guided
generation at inference time. In this work self-reg, we build
a rack-based model retrieval
[01:13:34] augmented generation model. But in this setting, we
trained a language model to generate tokens, but
then criticize its outcomes and self-improve. And we did it to the
whole loop with generating these critic tokens where the
model generates responses, but once in a while,
it generates tokens to say if the generated
response makes sense
[01:14:03] or not or if they retrieve
documents make sense or not. So these are also very
promising directions in pushing for
test-time scaling. We also showed that how
this self-guided improvement loop helps in synthesizing
scientific literature and answering very complex
questions about scientific tasks that require lots and
lots of reasoning.
[01:14:30] So please check out
these two papers. The results are
very interesting. We also have a demo, which is
openscholar.allen.ai, where you can play with this
system and type your question and then see how it
can answer and combine different pieces of information,
synthesize knowledge, and then answer queries for
this type of task. OK, this is a demo and I
would let you play with it.
[01:15:03] So I want to very
briefly also talk about how reasoning can get
integrated during pretraining. OK, so far what I talked about
was post-training integrating things at inference time. And now, let's go
backward and then say see how these things can
be added during training. Remember, when I
said RLVR didn't work
[01:15:31] when we had weaker base model. So we need to push to have
stronger and stronger base models. So this is of-- when we say
training-based model, it's not just training with
the next token prediction where learning rate
stays the same and so on. We usually do multiple
stages of training. In this first stage we
have the warm period, which is a very standard method. But then we use
cosine learning rate
[01:16:03] to train these models with
the next token prediction on trillions of tokens. But then toward the end of
training, we curate really, really high quality
data in a lot of cases designed to do more
complex reasoning. And then we take
the model that is here, the learning rate that is
here, and then a nearly to 0. Sometimes this stage
is called mid-training.
[01:16:32] The role of these
50 billion tokens is very important because we
still do next token prediction. But these tokens are very-- are trying to focus
on very complex tasks and emphasize on more
reasoning-oriented setting. And roughly this is called
nowadays pretraining and then mid-training. So the pretraining
stage, it uses
[01:17:02] most of the budget in
the training stage. It uses trillions of tokens. It's pretty much
unstructured, diverse text. Lots of it comes from web data. And we try to use
the best type of data that we could collect given the
compute budget that we have. During mid-training, it's
almost 1% of training. The idea is we're going
to upsample high quality data that we have
during pretraining
[01:17:30] and then to make sure that
we have some in-domain data. But then we make sure to bring
some event supervised fine tuning data, we bring in a
lot of reasoning type data coding data. And we try to emphasize the
quality of the data here. So this is for example,
the pretraining data mix that we use for OLMo 2, which
are some of the web pages. Some code data. I mean, the leftmost
column matters less, the rightmost categories
make more sense
[01:18:01] to follow right now, our
web pages, code data, academic papers, a stem papers,
some math web pages, and math proof, and so on. And in total we have
roughly 4 trillion tokens. But then during
mid-training stage, we started to bring in lots
and lots of math data, which started to patch
the math reasoning capabilities that the model
didn't originally have. For example, this was very
interesting observation.
[01:18:32] We realized at the
end of this stage the OLMo model was not that
good in doing multiplication, but much better in doing
addition and subtraction. So we started integrating some
synthetic multiplication data in the mid-training set. So we you cannot observe do
a lot of evaluations and then figure out, do some patching
to improve the model. And then inject that type
of knowledge in the model.
[01:19:02] So as you see in our
mid-training mix, we included a lot of
reasoning type data. And then we started
evaluating these models. So this is evaluating our
pretraining and mid-training together. On average, we see
significant boost in both setting like
from 50 we go to 60. From 56 we go to 68. And the biggest
gains are on GSM8K
[01:19:34] which is our math reasoning
capabilities and drop, which is also question answering
with math data, which is showing significant
boosts there, which is very interesting. OK, so putting all
these together, here are our two results, which
is on par with Llama 3 8B. Please refer to the
paper to look at the 13B. And most recently, we're
going to have a 32B results.
[01:20:03] OK, so with that, I
want to finish this that we've seen a lot of
progress in today's AI work. Still we need a lot of
research and innovation in many newer tasks. So here I've listed
a lot of them, a lot of them relevant
to reasoning agents, language models
for other domains, and so on, which I
really would be excited if I see you work on that.
[01:20:32] With that, I want to
thank a lot of people who are in my team, in the
OLMo and Tulu projects, and also my students at UW
and a lot of people at AI too. So thank you very much. Also, if you are
interested, we are hiring for all these projects. Thank you.
