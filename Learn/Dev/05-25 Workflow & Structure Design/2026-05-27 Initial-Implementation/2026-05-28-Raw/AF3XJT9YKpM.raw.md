---
# === meta ===
schema_version: 1

# === identity ===
id: AF3XJT9YKpM
type: youtube
url: "https://www.youtube.com/watch?v=AF3XJT9YKpM"
title: "Prof. Judy Fan: Cognitive Tools for Making the Invisible Visible"
aliases:
  - "Prof. Judy Fan: Cognitive Tools for Making the Invisible Visible"

# === pipeline ===
status: extracted

# === creator ===
channel: MIT Siegel Family Quest for Intelligence
channel_url: "https://www.youtube.com/channel/UCd0u8dJSDWbriMvEBmYcXBQ"
channel_follower_count: 38800

# === time ===
duration: 4286
upload_date: 20250408
fetched_at: "2026-05-25T13:06:15+00:00"

# === visual ===
thumbnail: "https://i.ytimg.com/vi/AF3XJT9YKpM/maxresdefault.jpg"

# === content structure ===
chapters:
  - {start: 0, title: Introduction}
  - {start: 232, title: Understanding Cognitive Tools}
  - {start: 780, title: Leveraging Visual Abstraction to Communicate Concepts}
  - {start: 2237, title: Harnessing Multimodel Abstraction to Support Statistical Reasoning}
  - {start: 3439, title: "Q&A"}
chapters_usable: true

# === language ===
language: null
original_language: en

# === subtitles ===
manual_track_languages:
  - en
auto_track_languages: []
transcript_status: available
transcript_source: manual_en
transcript_target: null
is_translated: false

# === engagement ===
view_count: 1120629
like_count: 31642

# === availability ===
availability: public
live_status: not_live
---

# Prof. Judy Fan: Cognitive Tools for Making the Invisible Visible

## Description

BCS Colloquium, co-hosted by the MIT Quest for Intelligence, March 20, 2025.

In the 17th century, the Cartesian coordinate system was groundbreaking. It exposed the unity between algebra and geometry, accelerating the development of the math that took humans to the moon. It was not just another concept, but a cognitive tool that people could wield to express abstract ideas in visual form, thereby expanding their capacity to think and generate new insights about a variety of other problems. Research in my lab aims to uncover the psychological mechanisms that explain how humans have come to deploy these technologies in such innovative ways to learn, share knowledge, and create new things. In the first part of this talk, I will provide an overview of our work investigating drawing — one of humanity's most enduring and versatile tools. Across several empirical and computational studies, I’ll argue that drawing not only provides a window into how people perceive and understand the visual world, but also accelerates the ability to learn and communicate useful abstractions. In the second part of this talk, I will preview an emerging line of work in our lab investigating the cognitive foundations of data visualization — one of humanity's more recent inventions for making the invisible visible. I will close by noting the broader implications of embracing the continually expanding suite of cognitive tools for accelerating the development of new technologies for augmenting human intelligence.

Bio: Judy Fan is an Assistant Professor of Psychology at Stanford University. Research in her lab aims to reverse engineer the human cognitive toolkit, especially how people use physical representations of thought to learn, communicate, and solve problems. Towards this end, her lab employs converging approaches from cognitive science, computational neuroscience, and artificial intelligence. She held a previous faculty appointment at the University of California, San Diego, earned her PhD in Psychology from Princeton University, and received her AB in Neurobiology and Statistics from Harvard College.

To learn more about the MIT Quest for Intelligence, visit quest.mit.edu.

Video Chapters:

0:00:00 — Introduction
0:03:52 — Understanding Cognitive Tools
0:13:00 — Leveraging Visual Abstraction to Communicate Concepts
0:37:17 — Harnessing Multimodel Abstraction to Support Statistical Reasoning
00:57:19 — Q&A

## Transcript

[00:00:04] JOSH TENENBAUM: It's
my great pleasure to introduce Judy Fan, who's
our colloquium speaker. Judy is one of my favorite
cognitive scientists really of any age. I think she's definitely
one of the leading-- by any objective
standard leading of the younger generation
people who are-- have just junior faculty or I
don't even know how junior you are, but she's-- been assistant professor at
Stanford for a couple of years.

[00:00:29] I think that's a good estimate. And she's by any means one of
the rising or glowing superstars of our field. She's won a number of awards-- the Glushko Dissertation
Prize, the NSF Career Award. I think you won that. Real-time talk introduction. But none of that really
is-- that's not the reason that we invited her. I think of Judy as one of
the most creative researchers I know of any
stage in any field,

[00:01:01] and I really mean that deeply. She has a background coming out
of neuroscience, and in that in many ways is it--
is very much at home talking to all the sorts
of people who inhabit this building, who record
signals from brains and try to make sense
of them computationally. She's done a lot of that. She's worked with colleagues
of ours whose work we know well like Dan Yamins was
one of her mentors,

[00:01:24] and she has studied vision. She's-- a lot of her background
is in visual psychophysics and visual neuroscience and
computational neuroscience. But if you look at her research,
some of which you'll see today and a lot of which you
won't even see today, she's gone in many
other directions or let's just say one key
direction, which is from basic-- some of the most basic
processes of perception and the things that
you can describe

[00:01:52] with nice, elegant
computational models to aspects of cognition that
really are what make us human, both biologically
and also culturally. And you're definitely going
to see some of that here. And so that means
she studied things like artistic expression
or creative expression in visual and other media. She's very interested
in narrative expression. She's really interested
in education, learning, and teaching and
how we make sense of the world

[00:02:19] symbolically and through
data and explanation. And she's-- so she's really
moved towards these much more complex cognitive processes that
are really distinctively human both biologically and culturally
and increasingly really of great import in our current era. But she hasn't given
up any of the rigor or I would say her
taste for rigor. And I know from a lot of
interactions with Judy that what keeps
her up at night is

[00:02:46] this is a struggle and
the challenge of how do you get at these really
important, hard things with the kind of rigor and
precision that many of us grew up valuing and
being inspired by in, for example, visual neuroscience
and computational neuroscience. And I can't say she's completely
solved that problem because it might take a while, but it's
a really great challenge. It's one that inspires me,
the way she works on it,

[00:03:10] and I hope that it's one that
we can all learn from and be inspired by and to
see where she is and where she's going with this. So, Judy, please tell us. JUDY FAN: OK wow. [APPLAUSE] I wasn't totally
prepared for that. That was incredibly kind, Josh. I really-- thank you and
thank you all for being here. It's-- I can't actually express
how wonderful today has been so far. I have a lot of
affection and respect

[00:03:40] for this department
and community and the kind of values,
scientific and otherwise, embodied in the work
that you all do here, and so it really is a treat to
spend a few minutes telling you about some of the work
that we've been doing. So we study cognitive tools. What are those? Let's start with something
as familiar and simple as the number line. I've been told not to move
around as much because we're

[00:04:04] using this mic. I'm going to try to do that. Nature didn't give
us the number line. We invented it. So as the Spanish architect
Antoni Gaudí once put it, there are no straight lines
or sharp corners in nature, but that didn't stop us. We created them anyway, and
we extended the number line, of course, a few
hundred years ago to create rectangular
coordinates, which turn out to be super useful. They were genuinely cutting
edge tools for thought,

[00:04:34] for deriving new
mathematical discoveries. When René Descartes
and his contemporaries realized that you could link
up algebraic expressions with geometric curves
in order to solve all kinds of
mathematical puzzles including this one
that has stumped the world for
millennia-- how many are familiar with this
particular-- the Delian problem, this riddle of the
Oracle of Delos? It's the problem of
how do you double

[00:04:57] the volume of a perfect cube? It's really, really
difficult to do using the mathematical methods
of that community and time. And here's the
solution for that. And it'd be really
hard to overstate the impact of this invention
over the last four centuries. That technology converted
all kinds of problems like these where you might want
to find the set of values that satisfies two equations into
essentially problems that

[00:05:25] relied on locating points of
intersection between two curves. Now imagine what happened next
to that revolutionary tool. It became something that
we could take for granted. It became so useful that it's
become basically indispensable to the way every
generation is educated. Virtually every mathematics
curriculum on the planet introduces a combination of
symbolic and graphical notation for representing
and manipulating

[00:05:53] mathematical objects. And the question that we wrestle
with is how did we get here and what is it about
the human mind that makes that kind of continual
innovation possible. There are lots of ways of
approaching that question from many different disciplinary
perspectives including history, anthropology,
economics, and I think that cognitive science also has
a really important contribution to make here.

[00:06:22] And I think the story begins at
least 30,000 to 80,000 years ago when anatomically modern humans
began to mark up their physical environments, essentially-- including these cave
walls here, iconically repurposing objects and
surfaces in their surroundings into carriers of meaning. We obviously didn't
stop at cave walls. The story of human
learning and discovery is deeply intertwined with
the story of technologies

[00:06:55] for making the
invisible visible. So here are just a few examples
from the history of science which I love. We've got Darwin's finches
and these illustrations produced by John Gould,
the ornithologist that Darwin worked
very closely with. Only when you see these
cases side by side does the kind of
morphological variation begin to really become
salient and pop out. We have the telescope
that Galileo

[00:07:20] used to observe the movement
of the moons around Jupiter. The kind of resolution
that he needed in order to question the orthodoxy
when it came to how the solar system was organized. We have Ramón y Cajal's
much celebrated drawings of the retina as seen under
the microscope, showing us what different parts of that-- part of the nervous system were
like and how they were hooked up to one another. And in the 20th century, we have
Feynman diagrams, named after,

[00:07:53] of course, the physicist
Richard Feynman, showing us subatomic particles
winking in and out of existence, events that we literally could
not and will never be able to observe directly
with the naked eye. And more than any
other species, we leverage this understanding,
this expanding understanding of the world in order to-- well, what-- maybe to
go back just one beat is that I want to
draw your attention

[00:08:26] to the variation on this slide. So notice that some
of these images are quite detailed and
faithful if you will to the way the
visual world looks to us when we open our eyes. Let's take Darwin's finches
at the top left, for example. Others are much more
schematic, but what all of these examples
share in common is they leverage what I've
been calling visual abstraction to communicate what we see and
know about the world in a format

[00:08:51] that highlights what
is relevant to notice. And then building
on that, we leverage that expanding understanding
of the natural world through the use of those
tools for learning in order to create new things. So, for example, our
detailed understanding of physical mechanics allowed
us to design and then build high precision
timekeeping devices, and a lot of this
technological progress has been driven by our ability
to continually reformulate

[00:09:20] our understanding of
the world in terms of those useful
abstractions that make it possible to re-engineer
the physical world according to our design. So translating
biological insights into bioengineering,
physical theory into advanced physical
instrumentation, neuroscience into
medical devices, and quantum mechanics
into modern electronics. So this is sampling
the kind of phenomena that I take a lot
of inspiration from,

[00:09:45] and the question we
continue to wrestle with is what about us makes
all of that possible. This is a schematic
that I've been using over the last
few years to help me think about the key
behavioral phenomena in play, and that will also serve as
a framework for embedding the different lines of work
that I'll be sharing with you. So this is one way
of illustrating the traditional mode in
cognitive psychology, my home

[00:10:08] discipline, which focuses on
how people process information supplied by the external world. Here's how that
picture is enriched by the study of social
cognition, which considers the behavior of multiple
individuals at once and how they interact
with each other. When those activities
are used in the service of learning about the world
and sharing that knowledge with others, they've been argued
to share important similarities

[00:10:29] with formal science even
when pursued by non-experts in everyday contexts. So building on that
tradition and with the goal of understanding how humans made
all those remarkable discoveries and inventions that I shared
with you just a minute ago, I'd like to argue that there's
still two critical ingredients missing from this picture. First is an account of
cognitive tools or technologies, material objects that
encode information intended

[00:10:55] to have an impact on our
minds, how and what we think. Second, I would like to
argue that the time has come to embrace science's
natural complement, engineering, how people leverage their
understanding of the world whether it's through
direct experience or socially mediated to
create new and useful things. Because without a serious
consideration of the engineering half of this picture,
I would venture

[00:11:21] to say that we'll never
be able to explain how and why the world as
we know it came to be. So at its core, if I had
to state it really bluntly, research in my group
aims to close this loop to develop psychological
theories that explain how we go
about discovering useful abstractions that explain
how the world works jointly with theories that explain how
we then apply those abstractions to go make new things.

[00:11:48] And my plan today is to tell
you about some of the work that we've done so
far along two lines. In the first part, I'm
going to share with you what I think we've figured out
about how people leverage visual abstraction
to communicate semantic knowledge
using freehand drawing as a central case study there. Ordinarily, in
the second part, I would then have told
you about our work investigating how people
learn and coordinate

[00:12:14] on procedural abstractions when
building physical things aligned with the engineering segment. But today, I want to try
something new with you all. So I wanted to
instead share with you some of our emerging work. So I'm really
curious to hear what you think exploring the
cognitive foundations of data visualization in which people
harness multiple information modalities, graphical elements,
words, and numbers to engage

[00:12:43] in statistical reasoning. In other words, to learn from
finite amounts of evidence about aspects of
the world that might be difficult or impossible to
learn through direct observation by a single individual. And I'm still happy to chat
with folks about our work on physical assembly
and physical reasoning probably at the reception. So to dive into
part one, how do we begin to think
about how people use

[00:13:06] visual abstraction to
communicate what they know and what they see? Here I think it's useful to
think about three behaviors that build successively
on one another. So first, of course,
visual perception, the problem of how we
transform raw sensory inputs into semantically
meaningful perceptual experiences that in turn makes
it possible to even contemplate visual production, that ability
to generate a set of markings

[00:13:32] that leave a meaningful
and visible trace in the physical environment. And those come together
during visual communication, how we decide just how to
arrange those graphical elements and in what order in order to
have a particular kind of impact on other minds whether it is
to inform or teach, persuade, collaborate, or any
other purpose that we can put those marks to. So this is a--
this is going to be

[00:13:59] an overview of the three studies
that I'll be walking through. First, we'll begin
with the question of what is the perceptual
basis for understanding what a certain class a subclass
of pictures represents. So to get off the
ground, we started by considering maybe the
most concrete and familiar instantiation of
visual abstraction, creating a drawing
by hand that looks like something in the world. What makes it so easy
to tell that the drawing

[00:14:35] on the left of
this slide is meant to correspond to the realistic
bird rendering on the right. There have been a
lot of different ways of responding to that question. Two have been really dominant. So the first is that-- the first
view is that we essentially see drawings as meaningful
and representing things because drawings simply
resemble objects in the world. Like this drawing literally
looks like the bird and that's

[00:15:06] how we know. The second response is that
drawings denote objects primarily as a
matter of convention, and we only learn which drawings
go with which objects in meanings from other
people, so if you take this Chinese
character, for example. So in an earlier line of
work, my collaborators-- close collaborators Dan Yamins
and my PhD advisor Nick Brown, and I discovered that general
purpose vision algorithms--

[00:15:33] so in this case neural networks
that compose multiple layers of learnable spatial
convolutions trained on natural photographs-- were
capable of generalizing fairly strongly to even quite sparse
sketches that didn't look photo-realistic
per se, suggesting that the problem of pictorial
meaning and resemblance might be resolved simply
by building better models of the ventral
stream of visual processing,

[00:16:01] especially ones that
accurately capture those operations performed
in those brain regions. We were not the only
ones to discover this. There are easily thousands of
computer vision papers indexed by Google Scholar that
use some kind of ConvNet or other neural
network based backbone to encode sketches
and natural images for a variety of applications. All of those results
you can think of as vindicating an updated
modern resemblance based

[00:16:29] account. It was also a really
useful insight for us locally with other
practical consequences. So in some more recent work led
by Charles Lu, a former master's student in the lab
and in collaboration with Xiaolong Wang
at UCSD, we built on top of those early findings
to further stress test that resemblance
account, basically taking a ConvNet
backbone and then training a decoder
on top that could map local elements in a sketch
to particular-- to corresponding

[00:16:58] elements in a photograph
under the constraint that you could warp
or rumple the sketch but not tear any holes in it. And the success
of that approach-- I'm just demoing here. It's not really a result.
It's more of a demo-- the success of that
approach suggests that fairly strong
spatial constraints govern how the parts
of sketches correspond to the parts of real objects
that they're meant to represent.

[00:17:23] So that's great. We've got good enough trainable
models of sketch understanding to build downstream applications
that work pretty well. I guess we can pack
up and go home. But, of course, that's
not the whole story. A static deterministic
account of visual processing falls short of explaining
how we generate and make sense of drawings like
these, which you might find all around this building. What these blobs and boxes,
squiggles, and arrows mean

[00:17:57] depends on what
we're talking about. So our next goal
was to figure out how to incorporate that
information about context to begin to account
for a greater variety of graphical
representations that we, in fact,
use to communicate, ranging from more faithful
pictures like those on the left here to the more obvious
symbolic tokens on the right. Our first paper
tackling that issue asked how people
knew when they needed

[00:18:24] to produce a more
faithful drawing and when they could
get away with something more schematic or abstract. So in that study, we
paired two people up to play a drawing game. The sketcher saw a display that
looked something like this where their goal was to draw
the highlighted target object, the third
one here, and we varied what the other
objects in the display were. On close trials,
the distractors all

[00:18:48] belong to the same basic level
category whereas on far trials the distractors were from
different categories. Using this really
simple manipulation, we discovered how
readily ordinary folks can adjust the way they use
depiction to communicate, making more detailed
and faithful drawings on those close trials when
they needed their drawing to uniquely identify
a particular exemplar but then sparser drawings
on the far trials

[00:19:14] when they could get away
with these category level abstractions. So here are some examples
of actual drawings that we collected in that study. And we found that sketchers
used fewer strokes on far trials,
less ink, less time to produce those drawings while
still achieving sealing accuracy on the fundamental
task of communicating the identity of the
target visual concept to the viewer, who themselves
took less time on those trials

[00:19:42] to make their decisions. Then to capture that
behavioral pattern, we proposed a
computational model of the sketcher that
consisted of two parts. So a ConvNet to
encode visual inputs into a generically abstract
feature space, and then a second probabilistic
decision making module that inferred what kind
of drawing to make depending on the context. I'm just going to give you
the take home from that study

[00:20:08] because I'm really excited to
get to other work in this talk. So the take home from our
model ablation experiments was that both the capacity
for visual abstraction, which you operationalize
as the network layer in the visual encoder
module and sensitivity to context were critical for
capturing how people manage to communicate
about these objects at the appropriate
level of abstraction. And then in more recent work,
we pushed that idea even further

[00:20:37] to understand not
only the impact of the current referential
context on how people communicate but also the
conditions under which new graphical conventions
might emerge when memory for previous interactions
with the same person leads people to produce
even more abstract, maybe even proto
symbolic tokens over time whose meaning depends even more
strongly on that shared history. So all of that was really
exciting progress to me, but,

[00:21:06] of course, people possess
much richer knowledge about the world than just
what things are called or what they look like. And a particularly important way
that we use visual abstraction, especially in science, is to
transmit mechanistic knowledge about how things work. So what is going on in people's
minds when they make that move? Going beyond what
is visually salient let's say about a
specific bird to highlight

[00:21:33] underlying physical mechanisms,
for example, how birds achieve flight in general. So you can imagine
my excitement when Holly Huey, a
wonderful former PhD student in the lab who's
now at Adobe Research, was also fascinated
by this question. And while we knew
from very cool work by Frank Kyle and colleagues
that people privilege mechanistic explanations
when learning from others and from work by Barbara
Tversky, Micki Chi, Tania

[00:22:00] Lombrozo, and others that
people can learn by producing explanations, we
realized there was a lot that we didn't know
about how people thought about visual explanations like
what do people think is supposed to go into a diagram that
illustrates how something works and what makes those different
from an ordinary illustration that is just intended
to look like something. One possibility
that I'll sketch,

[00:22:27] which I'll call the
cumulative hypothesis, is that people basically
think of visual explanations as being like extended augmented
versions of ordinary depictions. So in this table, explanations
would have all the things that depictions
have to communicate visual appearance and
then tack on information about physical mechanism. An alternative
possibility, which I'll call the
dissociable hypothesis,

[00:22:52] is that people think
of explanations as being images that pick
out mechanistic abstractions while greatly de-emphasizing
visual appearance. There's a kind of
selectivity there. So to tease apart
those possibilities, Holly designed a study to probe
this question in two ways, first, by characterizing the
content of visual explanations in detail and comparing
them to visual depictions, and, second, to measure how well
either of those kinds of images

[00:23:20] actually help downstream
viewers perform the task-- extract information
that they really needed whether it's about
appearance or about mechanism. So rather than a lesson
on bird flight, which is fascinating but
complicated, Holly constructed six
novel contraptions with a clearly observable
mechanism for closing a circuit and turning on a light. So here's an example of
one of those machines and the instructional video
that participants watched.

[00:23:58] Participants in the study
actually saw that twice-- those who demonstrated
twice, but there you go. So notice that this
machine consists of three different kinds of parts. There are causal parts that need
to rotate to turn the light on. There are non-causal parts
that look very similar but don't actually cause
the light to turn on. And then background
structural elements that are colorful and
hoist up the other parts

[00:24:22] are really important
but don't directly participate in the light
activation circuit. Every participant produced
explanations of some machines and depictions of other ones. On explanation trials,
they were asked to imagine that their drawing
would be used by someone else to understand how
the object worked. And then on the
depiction trials, they were asked to imagine
that their drawing would be used by someone
else to identify

[00:24:46] which object it was out
of a lineup of similar looking objects. That's manipulation. Really simple. Using that procedure, we
collected a large number of depictions and explanations
of each of these six machines. Eyeballing them, the drawings
seemed to look different. For example, maybe there's
a little bit more background in the depictions. Maybe there's some more
arrows in the explanations. But Holly wanted to be
really systematic about this,

[00:25:16] so she crowdsourced
tags, assigning every single stroke
in every drawing to one of four categories,
so one for each of the three kinds of physical parts,
background, causal and non-causal, and then
her fourth category that was a catch all for symbols. So in this particular
context, we're talking about arrows
and motion lines and then used those
tags to compare what kind-- what balance of
semantic information people

[00:25:43] emphasize in these
two conditions. What she found was
that while people drew causal and non-causal
parts in both conditions, they allocated more strokes to
the causal part and explanations than the non-causal ones. They also emphasize
the background a bit more in depictions than
explanations and as we suspected spent more of their ink
on symbolic displays of motion and parts interacting
in explanations than depictions.

[00:26:17] So already these
results are incompatible with a strong version of the
cumulative hypothesis, which would have predicted the
relative emphasis on background. Causal and non-causal parts
would be maintained even in the presence of errors. But however reliable,
those differences might just amount to
stylistic variation that doesn't have any impact on how
useful they are for the tasks that they are
intended to support.

[00:26:42] So to measure those functional
consequences of those decisions, Holly designed three
different inference tasks. The first asked how easily you
could tell what kind of action would be needed to
operate the machine, so here pull,
rotate, or push, what you might expect a good
mechanistic explanation to make clear. The second was to measure
how well each drawing could be used for object
identification, exactly what

[00:27:13] depictions are supposed to do. And then the third
was a more challenging visual discrimination
task where you had to determine which
of two highlighted parts was the causal one,
requiring you to establish a detailed mapping between
the parts of the drawing to parts of the actual
machine, something that you really only expect from
a mechanistic explanation that also preserved
enough information about the overall
appearance and organization

[00:27:41] of the parts of the machine. So under the cumulative
hypothesis, what we should see is that explanations
are at least as good as depictions for all tasks
but under the dissociable hypothesis that they might
be better for the action task but worse for the object task. And what Holly found
was more consistent with the dissociable
account where explanations better communicated
how the mechanism worked.

[00:28:06] But depictions were better for
communicating object identity. Interestingly, explanations
were not better in this sample for conveying the identity
of the causal part in that challenging third task
consistent with the idea that by leaving out a lot of
the background details and some of those explanations
that they may have abstracted away the very information
that would make it easier to link up specific
parts of the drawing

[00:28:30] with parts of the machine. And the bottom line
from those studies is that people share
intuitions about what is supposed to go into
a visual explanation even if this is the
first time they've been asked to generate one. And it can mean
sacrificing visual fidelity to emphasize more abstract,
mechanistic information. And more generally this
work shows how important communicative
context and goals are

[00:28:57] for understanding why
people draw the way they do, why depictions look the
way they do, and provided some experimental and analytic
tools for characterizing the strategies people
use to communicate visual information that is
goal and context relevant. And then in this
next section, we'll be asking what would it take to
develop artificial systems that are capable of human-like
visual abstraction. And here's why.

[00:29:27] We fundamentally want
useful scientific models of visual communication, and
the work I've presented so far is representative of where we've
prioritized making investments, namely the development of
experimental paradigms and data sets to measure and characterize
those behaviors in fuller ways across a broader
range of settings. Meanwhile, we've also been
investing considerable energy in evaluating how well
any member of the steadily

[00:29:52] advancing cohort of
machine learning systems might continue to be relevant
and promising candidates for capturing more detailed
patterns of human behavior in these high dimensional
tasks, specifically as models of human image
understanding as well as models of image creation. So the task setting
that we consider takes inspiration from
this famous series of drawings by Pablo Picasso. Some of these are very detailed.

[00:30:20] The last few are
very, very abstract yet all unmistakably bulls. Any scientific model of
human visual abstraction worth its salt ought
to be able to represent the ways in which
these bowls are all different from one
another and somehow at the same time all bullish to
their core or rather as bullish as they actually look
to real human observers. So in this work, that
was a huge team effort led by Kushin Mukherjee,
who is defending

[00:30:53] this Friday before joining
the lab as a postdoc, with contributions
again from Holly as well as Charles Lu, Yael
Winkler, who's here actually, and Rio Aguina-Kang. We began from the premise that
a strong test of whether we're on the right track towards
those scientific models is that we'll be able
to build algorithms that can generate and understand
abstract images the way that people do. Sketch understanding is one
of these deceptively simple

[00:31:26] yet poses a
fundamental challenge for general purpose
vision algorithms because, for one, it
requires robustness to variation in sparsity
like some sketches are more detailed than
others you could say. And, two, because
sketches demand tolerance for semantic ambiguity
because sketches can reliably evoke
multiple meanings. So we created a
benchmark which we call SEVA to pose those
challenges explicitly.

[00:31:59] So we collected 90,000
hand-drawn sketches made by about 5,500 people of 128
visual concepts under varying production budgets. So here are some
examples of what it looks like when people had to
create sketches cued by a photo. These are photos taken
from the THINGS data set, if you're familiar with
that, in less and less time. So by the time we get
to the four seconds, they're real, real sketchy.

[00:32:27] We then took those drawings and
then showed them to both people and 17 different then
state-of-the-art vision algorithms representing a
broad array of different kind of architectural commitments
and strategies and training protocols. Yes. TENENBAUM: Quick question
of clarification. Do people get to think about
it before you start the timer, or do they see it and then
they have four seconds? JUDY FAN: That's
something that's

[00:32:49] been haunting me for two years. Not enough. I think they-- no no, no. And I think-- so
what we're studying-- TENENBAUM: That's finding
both thinking and drawing. JUDY FAN: Thinking and drawing. So they see the image, and
then they have to go OK. So this is-- so we
don't know exactly how-- we-- there is this restriction
on the overall trial duration. I think that to really get
at the bowl phenomenon,

[00:33:12] I would want to give them
unlimited planning time and then just limited execution
time, and that would have been the way to do it. This is not that. So there's another
data set that has yet to be born that isolates
that more directly. Yes. So the four-second
drawings are quite derpy. That's the technical
term of art for that, but they are what
people did in this-- in those settings. So we had all of these
different sketches.

[00:33:39] They look the way they look
under those conditions. Then both people and
those vision algorithms perform the same sketch
categorization task, allowing us to measure the full
distribution of labels evoked by every individual sketch. The first thing
we established was that as you give people
more time to think and make a detailed-- think about how
to make and then go and make a detailed sketch,
those sketches

[00:34:04] get more recognizable
to models and people. They're less
ambiguous as measured by the entropy of the
label distribution. And even when the guess
is wrong, not the top one, it's more likely
to at least be in the right semantic
neighborhood estimated by language embeddings. So that's reassuring, but
then we dug in a little bit deeper and found that while some
models do honest to goodness perform better the recognition
task in other models,

[00:34:32] the variation across models
in terms of performance is totally dwarfed by
the gap between models and people, the reliable
signal in human recognition, in terms of both
performance on the left and also relative uncertainty
about the meaning of a sketch. So that suggests there's
still a sizable human model gap in alignment to
close here in terms of-- for sketch understanding. Nevertheless, at the time
we conducted this benchmark,

[00:35:02] we noticed that the
clip trained models were outperforming the others,
making it a reasonable candidate to begin to explore generative
models of sketch production built on top. So we explored the capabilities
of a particularly cool sketch generation algorithm
named CLIPasso whose development was led by Yael Winkler. We asked CLIPasso to generate
some sketches as well and also manipulated
its production budget.

[00:35:28] And in this case, the
unit now, the currency, is the number of strokes, which
is different, which I know. And what we found is that
even while human drawings and CLIPasso's drawings
were similarly recognizable across the four
production budgets-- by the way, this overlap in
recognition-- in recognizability is totally coincidental
given how the units are totally different. But we found that human--

[00:35:56] the really intriguing
discovery here is that humans and CLIPasso
sparsify their drawings differently. So what I'm plotting on the
y-axis on the right hand side here is the divergence
between the label distributions assigned by people to sketches
produced by other people and sketches
produced by CLIPasso under those different budgets. So in other words,
if you take a-- if you take seriously a
functional view of sketches

[00:36:20] as being for
communicating concepts and characterize
their meaning in terms of the full distribution
of the labels and meanings that it evokes, then even
though the 32 stroke CLIPasso drawings and the 32
second human sketches look different when
you look at them-- stylistically they are
different-- they are also quite functionally similar in
terms of the set of meanings that they convey in the
distribution of meanings

[00:36:47] they evoke. On the other hand, as you
tighten the production budget, that's where you really start
to see much larger divergences between people and CLIPasso. And we're hoping that
this SEVA benchmark will be a useful resource
for others who are interested in
developing models of human-like
visual abstraction. Now in the second and
I think shorter part, I'll give you a sneak preview
of our newest and mostly

[00:37:22] unpublished work on
multi-modal abstractions and how they are used to
support statistical reasoning. So back to that Cartesian
coordinate plane. We're a room full of scientists. You don't need me to tell when
you're making observations about the world it's
never this clean. Instead of perfect
lines, we might actually collect something like this,
a collection of data points. They land where they
land and from which

[00:37:53] we try to infer some
underlying structure with the actual generator--
the actual generative process that gave rise to them. That inferential move is a
fundamental building block of scientific
reasoning, and we sure don't do it just by memorizing
everything we've ever seen and thinking real hard. We use technologies. At the beginning of
my talk, I showed you these examples of the
use of drawings produced

[00:38:17] by hand as a
particularly enduring and versatile and
accessible tool for making the invisible visible. I think that's remarkable
and worth understanding. But perhaps one of the
most impactful technologies to have been developed
in the modern era was the invention of
data visualization. Like the telescope
and microscope, plots help to resolve
parts of the world that you can't see directly. But unlike either of those
optical technologies,

[00:38:50] it allows you to see
patterns and phenomena that might be too large,
too noisy, too slow to see with our own eyes. They're ubiquitous in
the news, the cornerstone of evidence-based decision
making and business and government. And they're indispensable
in every field of science and engineering. What I'm showing you here is one
of the first time series plots drawn ever by William Playfair
in 1786 to show the balance

[00:39:14] of imports and exports from
England over an 80-year period from 1700-1780. For a while, imports
exceeded exports, but then the relationship
flipped in the 1750s as exports really took off. Here's the thing. Unlike a drawing of one
of Darwin's finches, if you haven't seen one of
these kinds of images before, it may not be obvious
what you're looking at. But once you learn how,
it's a kind of superpower.

[00:39:45] So many individual
observations can be distilled into a
single graphic that tells a story that you
can read just by looking. And that's not even
all the reasons to care about plots
because they're such a powerful tool for helping
people update and calibrate their beliefs about
a complicated world, developing the skills to
read and interpret and even make graphs has long been
a goal of STEM education

[00:40:10] in this country, something
that's becoming even more important over time. The New York Times
broke a story-- this is actually from
about a year ago now-- about recovery from
COVID-related learning loss in mathematics
based on work led by some of our
education colleagues at Stanford and
Harvard, and it looks like across a bunch
of different states, the orange arrows
are there, which means that there's
been some recovery.

[00:40:34] But there's still
a long way to go. And I think that
successful theories that explain how people use
these kinds of images, discover, and communicate
important quantitative insights will help us equip people with
the kind of quantitative data literacy skills they
need more generally. So I'm going to
highlight briefly three directions that we're
pursuing in this vein. Our first question asks about
the underlying operations that

[00:41:03] are needed to understand plots. So the strategy that
we've been taking is to obtain machine
learning systems that can handle questions about
data visualizations at all, assess alignment with
people, and then interrogate the source of any
of those gaps-- any gaps there might be. What we need, of course,
to get off the ground is some way of
measuring understanding. So here's what that
might look like.

[00:41:30] Say we're looking together
at this stacked bar plot and someone asks you
about the cost of peanuts in Las Vegas. Take a moment to take it all in. Scan around. Suppose that person then gave
you four options to choose from.

[00:41:50] I added the little
charcoal thing. Now if you thought it was
A, you would be right. But that's not what some
prominent visual language models say given this
very same question. So in a Herculean
benchmarking effort led by Arnav Verma, a current
RA in the lab who's actually headed to the ECS program
right here in the fall, we've conducted
careful comparisons between humans and AI systems
on six commonly used tests

[00:42:26] of graph-based reasoning sourced
from across the education, health, visualization,
psychology, machine learning communities. All six of these tests were
administered in as parallel a manner as possible to both
human participants and several of these so-called multi-modal
AI systems and that had been-- the ones that made it
into this benchmark had been claimed
displaying competence on other kinds of visually
grounded reasoning tasks.

[00:42:59] We then recorded not only the
overall score achieved by humans and these models but the
full set of error patterns they produced, which
allowed us to assess even when a model or a person
got a question wrong to see if they're getting things
wrong in similar ways. What did we find? Here I'm going to show you
for each of the six tests we included, they have funny names
like GGR, VLAT, CALVI, HOLF, HOLF-multi-- actually
we made those--

[00:43:29] the bad name there is my fault-- and also Chart-QA, a
subset from Chart QA. We recorded how well--
we computed how well each of the models-- so these are the ones that
are showing up on the xticks in blue, orange,
purple, and red-- how well they did compared
to how well humans did. That will show up in green. And these were US adults who had
taken at least one high school math class. First, I want to
give you a sense

[00:44:00] of how well these people did. That's our reference point here. This is how well
all the models did. So we have in this
study two variants of Blip2-FlanT5, three
variants of lava-based models, specialized systems such as
matcha and its base model picks destruct, and finally a closed
proprietary model, GPT 4 V. Across all these assessments,
we did see a meaningful gap between models and humans
both under more lenient

[00:44:33] and a strict-- a more strict grading protocol. This is a gap that we might have
missed had we relied exclusively on the chart understanding
benchmarks that are currently most popular in the machine
learning literature, so this is chart-- this is the reason why we
included Chart-QA, which is the rightmost facet
on this slide where the gap seems a lot smaller. CALVI, which is the third
one, is really interesting

[00:44:56] because these are
adversarially designed plots that have funny
y-axis limits that require you to really attend closely. So that's one where we also
see somewhat larger gaps. We also analyze their
full error patterns so-- which can be really telling
when no one is quite at ceiling. Again, there's only one way to
get all the questions right, but there are lots
of ways that you can be wrong and wrong reliably.

[00:45:22] So we found that even
though GPT 4 V might look to be approaching human
level performance, none of these models, GPT 4
V included, generated human-like error patterns. So this is shown by all
the dots here falling well below the green shaded area
which represents the human noise ceiling. So the upshot is that
while currently developing, VLMs remain exciting
and promising testbeds for developing
and parameterizing

[00:45:53] the hypothesis space
of possible cognitive models of visualization
understanding, there still are these
systematic behavioral gaps that are worth interrogating
further to realize those models' full potential. In parallel, we've
also been developing experimental paradigms to probe
a related facet of visualization understanding, the
ability to select-- design select-- the
appropriate plot to address your epistemic goal.

[00:46:22] So I'm going to talk
to you about that next. The way we set up the
problem is to imagine that there's some question
that you have about a data set. Some what I've been calling
epistemic goal that a person is trying to satisfy
like, for example, like which group is better. Let's say the left
agent is trying to pick the plot to
help shift the person's beliefs appropriately,
but if they had a different
question in mind,

[00:46:48] maybe they might need
a different plot. That's the intuition. So this is a line of work that
was launched by Holly Huey, and we formulated in a study
hundreds of different questions that could in principle be
answered by using real, publicly available data
sets, in this case, your data sets that
ship with base R. So here's an example
of a scary one, tracking airplanes
and bird strikes. What is the average speed of
aircrafts flying in overcast

[00:47:16] skies that encounter bird
strikes at 0 to 5K miles? We then presented
participants with a menu. AUDIENCE: Judy, can
I ask a question? JUDY FAN: Sure. AUDIENCE: What is 5K miles? JUDY FAN: Altitude. Yeah. AUDIENCE: You sure
it's not 5,000 feet? JUDY FAN: Sorry, five-- hold on. Hold on.

[00:47:37] That might be a-- that
might be a typo on my part. I don't think the
question inherited that. AUDIENCE: [INAUDIBLE]
Anyways, don't worry about it. JUDY FAN: I'm not-- I'm-- I'm-- I'm starting to, but
I'm going to resist that urge right now. No, no I think that-- yeah. So-- so-- AUDIENCE: But
these-- a lot if this is the standard that they're
full of all sorts of typos. JUDY FAN: This is a templated--
there's a templated thing.

[00:48:00] I think there are-- basically
a lot of these questions are funny, and I think
they could have been smoothed over a bit more. So this is like-- the-- yeah. Yeah, yeah, yeah. No, no, it's good. It's good. So we had all these questions. Some of them were
better put than others, but we presented participants
with a menu of possible graphs that they might show
someone else in order to help them answer
that question.

[00:48:23] However, they interpreted
that question. Whatever it is,
those are the strings that we're showing to people. And they could choose from this
menu either a bar plot, line plot, or scatter plot. Some of them were
more distilled. Some of them were
more disaggregated. And then we measured how often
they picked each one in order to construct a choice
distribution over plots. So here's what it looked like on
average for the retrieve value

[00:48:52] questions in our stimulus set. This is one kind
of task, and there are other ones that'll
ask you to compute some kind of difference
between two values. This is the retrieve
value subset of items. We then tested various
hypothetical strategies that people might have used to
pick the plots that they did. Clearly they are
showing some kind of bias here, the black curve. The purple curves here
represent the predictions

[00:49:16] of bar plot, line plot,
or scatter plot purists. They just always
went for the bar plot but just didn't care whether
they had three variables plotted or more. We also considered
the possibility that people might prefer more
targeted visualizations overall but not really care about what
type of graph they were sharing. Maybe they might prefer ones
that show more of the data, maybe ones that hide less of
the variation in the data.

[00:49:47] The best candidate we found that
we considered was the proposal that people are maybe actually
sensitive to the features of those plots that were
relevant for answering the question and, in
fact, actually predicted the performance of about 1,700
other participants who tried answering every one of those
questions, however weirdly put, when paired with
every possible plot. So we went and actually
measured performance,

[00:50:13] and then we constructed
the distribution based on those
performance levels and then use that task in order
to-- use the data from that task in order to generate
predictions of the audience sensitive hypothesis. And this is where we-- this is how the
shape of those curves look when we're only considering
the true value items. But if you look at the
data set as a whole, we found that this audience
sensitive proposal did well

[00:50:42] across the board. So what I'm showing here is
essentially a model fit measure defined over the divergence
between the predicted and the actual human
choice distributions. Has a name, the Jensen-Shannon
divergence, the average of KL divergence but both ways. So I'm excited about that
result as an initial validation of a strategy for
measuring visualization understanding using
more open ended tasks

[00:51:11] and also because it suggests
that even non-experts you could say, people who might not
be professional scientists, are sensitive to those features
of plots that make some suitable for answering
some questions than others and honestly as someone who
teaches intro stats for a living gives me hope.

[00:51:35] In the final final
leg of our journey, we're going to take
another critical look at this problem of measurement. So a few minutes ago, I
showed you some results when using these six tests
of data visualization understanding. These are the ones that we have
today, which is why we use them in our benchmark study. Our question in this last
study in work that's actually now in press and led by
this extraordinary postdoc

[00:52:06] in our lab, Erik Brockbank,
also with Arnav Verma, we're asking what are these
tests actually measuring, and are they measuring the
skills in the best possible way? And can we do better? So here are some initial
steps towards answering those questions. To get some traction, we started
with these two GGR and VLAT, these being some of the most
widely used and established tests. We gave GGR and VLAT
as a composite test

[00:52:37] to a large and diverse
sample of US adults-- actually two samples,
one that was recruited on the UCSD campus
and another that was recruited over prolific
under the constraint that it had to be a
demographically representative sample. And what I'm showing
on the left is that we get a pretty convergent
estimates of the difficulty of individual items in both the
college campus sample and the US representative sample,
which I think is reassuring.

[00:53:05] On the right, what
I'm showing is that people who did
well on one test often did well on the other,
suggesting that maybe the two tests are measuring some of the
same things or similar things. And the question is like what? What are those things? One possibility is
that those two tests track how much easier some plots
are to understand than others. If so, those plots
should be reliably hard or easy across the
board like maybe bar plots

[00:53:34] or easy but stacked area
charts are more challenging. It seemed to us
that clearly there's a lot more going on here. Performance wasn't
consistent for a given kind-- it wasn't always
consistent for a given kind of plot within
or across tests, and there weren't
even enough items to be able to establish a direct
link between the type of graph and performance because
actually in each of these tests,

[00:54:01] there's generally one instance
of each class of graph. So that also made
it challenging. We also dug into the
patterns of mistakes that people made and
found that the best way to predict those
patterns on these two tests wasn't the kind of plot or
even the type of question. Maybe find the max
or identify clusters or characterize distribution
or retrieve value. These are all common ways of
describing the ontology of tasks

[00:54:31] involving plots, but it really
seemed from this analysis that other underlying factors
that aren't well described by the ontology are really
accounting for error patterns much more efficiently. So here I'm showing you how
much better a parsimonious four factor model does than one that
uses the groupings that you might think of to-- use to organize
the set of skills needed to understand any graph.

[00:55:01] So I'm not going to unpack
everything on this slide, but this is just
meant to illustrate that there seems to be something
that is going on here that isn't obviously mappable to the
ways that we talk about what the component skills are
that you might actually see in textbooks or in instructional
materials when it comes to how to break into data
visualizations. And even if existing
assessments might not

[00:55:26] be testing and characterizing
visualization understanding in the best possible
way, we're really trying to take that
as a glass half full call to action to develop
improved measures. So stay tuned for those. More generally,
the reason I think this work establishing the
perceptual and cognitive foundations of data
visualization is so important is because it will
give us a chance to use what we learn to
eventually help people, learners

[00:55:58] in real educational
settings, calibrate their understanding of a
complicated and changing world that we can ever only
observe a part of. And these kinds of
integrative efforts if you will that connect
fundamental science to that wider world that we
all inhabit exemplify where we're going with all of this. We really want to develop
psychological theories that explain how people use the
suite of cognitive technologies

[00:56:28] that we've inherited and
continue to innovate on. We want to understand why that
toolkit looks the way it does, what future cognitive tools
might work even better. In the long run, I
think that understanding how these tools work and
how to make them better really matters because
it's like these tools that are at the heart of two of our
most impactful and generative activities. First, education, which is
the institution and maybe more

[00:56:58] importantly the expectation
that every generation of human learners
should be able to stand on the shoulders of the last
and see further and design the suite of activities
and habits of mind that help people
continually reimagine how the world could
be better, and then go out and make it true. So with that, I
want to thank all of the folks who've
been involved in this work and other
lines of work in the lab.

[00:57:23] It would not have been possible
without an amazing research team and network of
collaborators and colleagues in many different
places including here. So I want to thank all of them,
all of you, for your attention, and I'm happy to
take questions if we have time, which we might not. Great. Thank you. [APPLAUSE]

[00:57:44] I see hand, hand. Hand, hand, hand AUDIENCE: Thank you
so much for the talk. One thing I'm curious about is
so in a lot of your examples specifically relating
to depictions, there seems to be this
one-dimensional axis between things that are
more detailed and faithful or versus more sparse. But I'm curious about cases
where people watching diverge and produce things
that are actually false or counterfactual.

[00:58:07] So I'm thinking if I'm
drawing a glass of water and I want to indicate
that it's full, I'll shade it in blue
even though in real life, glasses aren't blue
when they have water. And I feel like that depends
a lot on culture and language and stuff like that. I speak a language where
water is described as blue. I have been around pools
which are usually painted blue on the inside and so on. And that could depend.

[00:58:30] So I'm just wondering how
you thought about some of those cases? JUDY FAN: Yeah. Yeah. There's a large
literature in philosophy in the area of aesthetics
that I take inspiration from that begins from a similar
premise, which is how is it possible that we
understand pictures that are false like pictures
of fictional individuals or unicorns or glasses
with blue water even if it doesn't
look that way.

[00:58:55] The tech that we've been taking
in our own empirical work is to not begin from
that premise, which is that rather than
thinking of them as false, this is the actual data
that people are generating under some objective. And we just-- we're trying
to figure out what that is. And so the reasons
why they might render the water depicted
in that depicted glass is for some reason-- and we're interested in those
stakes that you identified--

[00:59:22] to what degree it captures the-- faithfully the visual
appearance, the phenomenology of looking at a glass of water
in a room where the glass is in front of you as opposed
to a kind of acquired convention for how you
depict water, for example. I think those are very
reasonable sources of constraints on
why people make those representational
decisions. So I think those are
the kind of questions that just rather than thinking
of some drawings as good or bad,

[00:59:51] false or true, we just
find it a lot more useful and productive
to think of these are the drawings people
make under those conditions. Why? Why do they look that
way, not another? If that helps. Thanks for your question. AUDIENCE: Sure. Thank you very much. I am curious about-- so I thought something you
only very briefly touched on is super potentially interesting
is the human likeness of errors

[01:00:17] that artificial systems make
in graphics and visualization. And I guess in a
way actually that seems especially useful
for an artificial system because if I am producing
a visualization, I know what people
will understand it to be if they understand it
correctly, but I don't know-- I might have a lot of
difficulty imagining how it would be misunderstood. And so that actually seems
like a task which was literally

[01:00:52] how else might this
be misunderstood. I maybe understood would be
it's very, very valuable thing, and I want to ask what's-- what
is our state-of-the-art model of that and how graphs
are misunderstood. Usually they're misunderstood. And is it an interpretable
state-of-the-art problem from a scientific-- JUDY FAN: Oh, gosh. AUDIENCE: Give us
insights into the workings of the actual inner workings.

[01:01:20] JUDY FAN: It's really,
really good question. So I'm going to
engage with it, which is so there's a phenomenon
which some of us in the room study which is
perspective taking, which is hard but doable
in some contexts. It can be possible to imagine
what the world must look like from the
viewpoint of someone else and their various
paradigms for studying that. It also seems like the
capacity for doing that

[01:01:45] very quickly and accurately
can change with practice. And so there's a role for
expertise and experience to play in shaping your
ability to do that. One way in which
that manifests-- I'm not going to refer to
the VLM results at all here, but just to sketch the
shape of the problem, it's teachers, the
kind of expertise-- one of many kinds of
expertise that teachers-- really skilled teachers
develop is the ability

[01:02:13] to diagnose-- notice it
is called misconceptions-- when they listen to learners
describe how they're thinking about a problem. So it may be that
the final response or answer that a student gives
to a math problem is wrong, but it's not only
that it's wrong. The relevant
question isn't always that it's wrong or
right but rather what is the nature of the
misconception or misperception or what is the gap between
the normatively correct way

[01:02:41] of representing the
problem and proceeding through the different steps
and whatever the student did. So one way in which I think-- maybe I will just very,
very briefly, if it's OK, speak to how we've been
thinking about this question in the modern era of
extremely large machine learning systems
is to interrogate the kind of operations
and conceptual primitives so to speak that these
systems rely on when they get

[01:03:10] an answer right or wrong,
using the suite of tools that go under the banner of
mechanistic interpretability. But you could-- we could
call it cognitive systems neuroscience for
artificial neural networks in order to diagnose where
right answers and wrong answers come from, and it'd be
really, really nice. I'm not going to go into those
in detail because of the-- But that's a kind
of like strategy

[01:03:32] you might take to connect what
is the operations that are being performed in these systems
that do not immediately lend themselves to those kind of
interpretations at the same time and then connect those to
what has been called knowledge graphs-- the underlying knowledge graph
that a person might hold or not hold. So that's like a-- like a way of setting up the
problem I think, and sometimes the issue, the bottleneck
might be perceptual as such.

[01:04:07] And other times, it might be
like a bottleneck or the gap might have to do with
a reasoning step, and the goal is to really
expose what those steps are, have tools for diagnosing
them so that in principle you could use them to diagnose
those misconceptions or misperceptions,
mistakes, missteps in any body or any system. That's very, very,
very hard, of course. But these challenging problems
are I think like a tool

[01:04:36] that we can use in-- towards that end. I hope some of that made sense. I-- a lot of thoughts about. AUDIENCE: Can I ask a follow up? JUDY FAN: Yeah. Yeah. AUDIENCE: So I
think it makes it-- so in particular, you helped
us out here by highlighting-- JUDY FAN: I know. AUDIENCE: That red, the
right part of the graph to pay attention to. JUDY FAN: I did do that. AUDIENCE: And one
of the reasons why you might have trouble
answering this question--

[01:05:00] I'm just trying to
see if I understand-- JUDY FAN: Yeah. AUDIENCE: Is that you might not
know which part of the thing to pay attention to to
answer the question. JUDY FAN: Yeah. AUDIENCE: Or but-- or you
might know what part-- but you might not know
what to do with it how to take that red
rectangle and relate it to the information
on the y-axis. Or you might not
know even if you know how to do that
how to turn that

[01:05:24] into the ends of the question. So those are the
kind of that's that-- JUDY FAN: Well, yeah. Those are the kind
of teaching moves that a human educator
might actually take. AUDIENCE: You could. JUDY FAN: Yeah. AUDIENCE: People have even
tried to break this down like some of Erik
Schultz's group, for example, where they
say you could ask the model or people how big is the
rectangle, red rectangle on the second column.

[01:05:45] JUDY FAN: Yeah. AUDIENCE: It doesn't require
any reasoning but just-- JUDY FAN: Yeah. Yeah. Yeah. AUDIENCE: Or something or which
blue rectangle is the highest. JUDY FAN: Yeah. AUDIENCE: For example, is that
the kind of thing you're doing? JUDY FAN: Yeah. Yeah. Yeah. So we started with
stimuli like these. So this is a very,
very new work that's being led by-- yes, exactly. So this is being led by Alexa
Tartaglini in collaboration

[01:06:03] with Chris Potts. And the-- we started
with stimuli like these, like the real wild
plots and questions, and then realized we
wanted to drill down. So there's both
taking these plots and asking a variety of
different questions including these more basic
ones so to speak. Also we've realized that
really stripping these down to much simpler
versions of it that still contain the core
multi-modal integration

[01:06:31] challenge. Even we're currently running
these studies on number line stimuli essentially
to understand how you might judge the
distance between two data points on the number line. For example, but they're like
all these different routes to it because this is like-- this-- the point is that
this is complicated, and so decomposing it is
part of the challenge. AUDIENCE: [INAUDIBLE]
--if there could be like--

[01:06:59] JUDY FAN: Yeah.
Yeah. AUDIENCE: [INAUDIBLE] how
you teach these skills. JUDY FAN: Yeah. AUDIENCE: Break them down into-- JUDY FAN: Exactly. Yeah. That's right. That's right. Yeah, right. So there's assessment
and then also the reason why this
black shaded charcoal rectangle is there
is because there's some guess that I had about what
might be a bottleneck to rapidly looking at the appropriate
feature of the plot.

[01:07:24] AUDIENCE: Could I follow up? JUDY FAN: Yeah, sure. OK, this is-- OK. AUDIENCE: When I first
looked at this plot, I thought it was
actually ambiguous, and I wasn't sure whether
the height of the bars all started at 0 and
we're seeing one of them in front of another. JUDY FAN: I know. I know. PRESENTER: With
the cheapest ones-- JUDY FAN: It's like
dodge equals true. Yeah. AUDIENCE: But that's
not my question.

[01:07:43] My question is this
you've been focusing on for adults who've
been exposed to lots of different kinds of media. What are what are the best
ways to present information so that people can get it and
get it efficiently so forth? But there's another
question, which is I think for when we first
see a new kind of graph this might actually
be the first time I ever saw one that
stacked up, at least it's been a while since--

[01:08:07] JUDY FAN: That's exciting. AUDIENCE: [INAUDIBLE]
--stacked up like this. JUDY FAN: They look like-- AUDIENCE: It's not so obvious
when you first see it. JUDY FAN: Yeah, it's not. AUDIENCE: As we get very
used to seeing them, seeing things that are different
can become really harder. So, for example, event
related potentials where negative goes
up drives me crazy-- JUDY FAN: Right! AUDIENCE: Every time I see it.

[01:08:24] JUDY FAN: Yeah. Right. AUDIENCE: So I
wonder what do you think about the question of how
these kinds of representations should be structured so that
they're easy for kids to learn. JUDY FAN: Yeah. Oh. AUDIENCE: You start out with
none of these representations. What would you put
into the earliest ones that you want kids
to learn about? How would you
progress from there? JUDY FAN: Yeah. That's a good question.

[01:08:46] Yes. And actually there
are versions-- I feel like there's
a few minutes ago. Nancy and I were talking about
something kind of related when it comes to
how people break into this class of
visual inputs at all. There's a sense in
which you're building on top of a lot of neurotypical
ordinary visual and cognitive development in order to grasp
the presence of different shapes in certain spatial arrangements.

[01:09:14] There's-- it relies on literacy
as such being able to-- You have-- there are a
bunch of primitive-- there are a bunch of conceptual
primitives and more basic competencies that you might
need to build up first. It might be that there is
a sequence of experiences that build from the-- that's a really good question. I don't have answers to that
curriculum design question, but I think it's
a great question.

[01:09:39] And it feels like there
are thoughts that I've-- yeah. AUDIENCE: It seems like the
whole back third of the cortex does vision, and it's a
spectacular set of machinery that extracts all these
different rich kinds of visual representations
from orientations to heights to shapes to
landscapes, all of which are possible spaces we can use. And so it seems like the
essence of making a good graph is figuring out how to
make a visualization that

[01:10:09] taps into some of that
machinery to build a map. JUDY FAN: What makes visual
scenes in general easier and more fluent to process? Things that aren't
particularly cluttered. If you're if you're interested
in the kind of problem of visual search
over those scenes, there are aspects of those
processes that are co-opted in order to identify the
appropriate sub-region of this image to look at. You might imagine
designing those initial--

[01:10:34] those initial graphs to cohere
more with those kinds of scenes. And then there's
the step of mapping the components of these scenes
to concepts that you also need to learn about and that
can be really hard initially and then become faster and
faster and easier and easier over time. And I think it's really
fascinating what is happening as that takes place. Yes. And also yes. But then also--
what should I do?

[01:11:04] PRESENTER: And one-- this-- why
don't we-- this is really cool. Why don't we wrap
up and allow people to who need to leave to go? JUDY FAN: Yeah. Yeah. PRESENTER: But other
people, please linger here. You'll be here for
a little while. We have a reception. We have 45 minutes or so for
people to interrogate you. JUDY FAN: Amazing. Thank you. Thank you. Thank you. [APPLAUSE]