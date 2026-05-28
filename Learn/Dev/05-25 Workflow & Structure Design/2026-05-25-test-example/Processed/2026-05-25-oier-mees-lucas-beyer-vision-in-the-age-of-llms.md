---
id: 0XB7fNS_ONg
url: https://www.youtube.com/watch?v=0XB7fNS_ONg
title: "Lucas Beyer: Vision in the Age of LLMs [ETHZ Robot Learning 2026]"
aliases:
  - "Lucas Beyer: Vision in the Age of LLMs [ETHZ Robot Learning 2026]"
channel: Oier Mees
channel_url: https://www.youtube.com/channel/UCHHkvupYInGs6sdcrWTOj6g
duration: 4144
upload_date: 20260514
processed_at: 2026-05-25T00:00:00
thumbnail: https://i.ytimg.com/vi/0XB7fNS_ONg/maxresdefault.jpg
view_count: 5700
transcript_file: "[[0XB7fNS_ONg|0XB7fNS_ONg]]"
type: youtube-digest
state: active
---

# Lucas Beyer: Vision in the Age of LLMs [ETHZ Robot Learning 2026]

> [!quote]- Source description (cleaned)
> Guest lecture for the ETH Zurich course "Robot Learning: From Fundamentals to Foundation Models" (Spring 2026), hosted by Oier Mees. Lucas Beyer (Meta Superintelligence Labs) traces the frontier of multimodal foundation model training, from pre-training through post-training.
>
> Course website: https://cvg.ethz.ch/lectures/Robot-Learning/

> [!info] Orientation
> Lucas Beyer is a researcher now at Meta Superintelligence Labs, previously a long-tenured member of Google Brain / DeepMind's Zurich multimodal team, where he was a core contributor to Vision Transformers, SigLIP, and PaliGemma — the open-weight VLM that underpins many of the VLAs covered earlier in this robot-learning course. This is a ~70-minute guest lecture aimed at graduate robot-learning students who already know what a VLM / VLA is but want the *history* of how vision pre-training got to its current recipe. Beyer explicitly frames it as "the least robotics lecture in this robot-learning course" — he is telling the story of how computer vision went from barely working to a converged pre-train / mid-train / fine-tune recipe, so students can build on top of it rather than redo it. The talk doubles as a tour through his own research arc (VTAB, BiT, SigLIP, PaliGemma) and ends with a long, opinionated Q&A.

## TL;DR

The community has converged on a simple, almost boring recipe — **pre-train at scale on weakly-supervised image-text pairs, mid-train to install core skills like reading and locating, fine-tune on a few hundred examples per task, optionally RL-tune** — and Beyer argues this recipe essentially solves *pure perception*. The story of how we got here is a sequence of hard-won, often counter-intuitive lessons:

- **Self-supervised pre-training lost.** Different SSL pre-text tasks gave inconsistent transfer; the only reliable signal was "bigger model is better." Once they sprinkled a few labelled examples into pre-training, supervised scaling crushed SSL — and the whole team pivoted.
- **You must scale three axes together.** More data alone, or bigger model alone, or longer training alone, looks like *nothing happens*. Only data × model × duration, each an order of magnitude up, unlocks the effect. The community wasted years declaring negative results from scaling only one axis at a time.
- **List images, not classes.** Hand-curated class lists (COCO's 80 classes literally came from a researcher's 8-year-old kid) cap creativity. CLIP/SigLIP flipped this — crawl images, take whatever text is near them, learn to match — and freed vision from North-American-kitchen vocabulary. Then the community immediately ruined it by filtering to English-only, ImageNet-like data; Beyer's group spent a project pushing back, showing the filter mistakes Tehran's Milad Tower for Toronto's CN Tower.
- **CLIP can't learn relations.** In a random web mini-batch, "cat sitting left of dog" almost never has a counterfactual to contrast against, so the model shortcuts to bag-of-concepts. The fix is unglamorous — add a captioning loss; SigLIP v2 has it.
- **Look at the data.** The "VLMs are blind" benchmark with "the grass is eating the horse" vs. "the horse is eating the grass" is solved by a *blind* captioner. Every PhD generation re-discovers broken benchmarks.
- **Mid-training is where skills get installed** (OCR, locations, detection-as-text, segmentation via VQ-VAE tokens), pre-training is too crude for them, fine-tuning is too small.
- **Perception is "solved" in the sense that ~128 fine-tuning examples + a good pre-trained VLM nails almost any pure-perception task in an afternoon.** Reasoning, planning, and "understand a new task from words alone" are the open frontier — and the Q&A pushes hard on streaming video, distillation for deployment, JEPA, and whether memorization is masquerading as intelligence.

## Chapters

| #            | Chapter                                                                       | Time    | Uploader's chapters |
| ------------ | ----------------------------------------------------------------------------- | ------- | ------------------- |
| **Part I**   | Framing                                                                       |         |                     |
| 1            | [[#1. The goal: general perception, and a benchmark to measure it (01:44)]]   | 01:44   | —                   |
| **Part II**  | Pre-training                                                                  |         |                     |
| 2            | [[#2. Self-supervised lost; supervised scaling won (08:50)]]                  | 08:50   | —                   |
| 3            | [[#3. Scaling needs data, model, and patience — all three (16:50)]]           | 16:50   | —                   |
| 4            | [[#4. From class lists to CLIP: learning from web text (20:17)]]              | 20:17   | —                   |
| 5            | [[#5. The English-only filter trap and globally diverse data (25:30)]]        | 25:30   | —                   |
| 6            | [[#6. CLIP's relational blindspot, the captioning fix, and "look at the data" (29:08)]] | 29:08   | —                   |
| **Part III** | Mid-training and after                                                        |         |                     |
| 7            | [[#7. Mid-training: installing core skills the VLM needs (34:30)]]            | 34:30   | —                   |
| 8            | [[#8. Fine-tuning, "perception is solved," and what's still hard (41:30)]]    | 41:30   | —                   |
| **Part IV**  | Q&A                                                                           |         |                     |
| 9            | [[#9. Q&A: small-scale pre-training, augmentations, frozen encoders, JEPA, distillation, and making humans smarter (46:50)]] | 46:50   | —                   |

---

## 1. The goal: general perception, and a benchmark to measure it (01:44)

Beyer opens by warning this will be the *least* robotics-flavored lecture in a robot-learning course: VLAs sit on top of VLMs, and almost every VLM the course has touched descends from PaliGemma, the open VLM his team released. The lecture is the story of *what comes before* — how vision went from barely working to a converged recipe — so that students working on robot policies understand the substrate they're standing on.

The personal motivation is unchanged from eight years ago: a robot a non-technical person can teach to do anything, *without programming*. The bet then was that two things were needed — robust general perception, and learning from a few examples. The second one was already on a good track. The first, in his judgment, wasn't, so he went to work on vision. Language models since then have softened the "few examples" requirement (a few *instructions* may now do), but robust general perception is still the load-bearing piece.

What does "general perception" mean concretely? Beyer demonstrates by playing the few-shot game with the audience — show five flowers labelled A/B/C, then ask the class of a new one; same with satellite scenes, same with an obscure microscopy-style image — and the room gets them all right. *That* is the target: a representation that can adapt to any reasonable visual task from a handful of examples, the way a human visual cortex does.

To make progress measurable, his team introduced the **Visual Task Adaptation Benchmark (VTAB)**: sample a wide range of perception tasks, give the model a few train examples per task plus your adaptation algorithm of choice (fine-tuning being the default), score it on test examples, average. The point is breadth — no one task wins; representational generality does. With the target framed and the benchmark in place, the rest of the talk follows the recipe the field eventually converged on: *pre-train, mid-train, fine-tune, RL-tune, done* — though RL-tune gets dropped so people aren't late to dinner.

---

## 2. Self-supervised lost; supervised scaling won (08:50)

Five-to-eight years ago the field was sure the path to general representations ran through self-supervised pre-training — reconstruct, predict the next video frame, contrast crops — anything to avoid the human bias of labels. Beyer's team did the obvious thing: reimplement a large subset of the SSL methods and rank them on VTAB.

The result was sobering on two fronts. First, **no SSL method consistently won** — the leaderboard was noisy across tasks. Second, and worse, **the only stable trend was that bigger models were always better, within each method**. The pre-text task you chose mattered surprisingly little.

Then the deeper failure: across SSL methods, **there was almost no correlation between pre-training-task performance and downstream performance**. A model that did better at its self-supervised objective wasn't reliably better at the thing you actually cared about. The bubbles on the plot were scattered; the only clear gradient was, again, "make the same setup bigger." This is a point Beyer flags as likely true for robotics too — the proxy task you train on is rarely well-correlated with the real task you care about.

Given that disconnect, what do you actually do? You have to *pick* which pre-trained model to deploy, which means evaluating multiple, which means you always have at least *some* labelled examples in hand — even if it's just you sitting down and writing "good / bad" on the robot's behavior. So the team did the unglamorous thing: take any SSL method, throw a few labelled examples *into pre-training*, and check the downstream curve. Transfer became dramatically easier — the orange curve cleared the blue one immediately.

That experiment ended self-supervised pre-training inside Beyer's team. The conclusion: drop the SSL purity, go fully supervised, and **scale**.

The fully-supervised story then got its own striking plot. A wave of papers around the GPT-1/2 era were scaling models on ImageNet (~1M images) and reporting modest gains — 50% to 55% — at huge cost. The team's BiT-style runs reproduced this slope. The unlock was the *data* axis: same architecture, jumping pre-training data by 15×, then another 20×, broke open performance — and not just on ImageNet's canonical images but on ObjectNet, where objects appear in weird poses and locations. Out-of-distribution generalization tracked the scaling trend, which is the property you actually wanted.

---

## 3. Scaling needs data, model, and patience — all three (16:50)

Why did the community take so long to accept "just scale it"? Because **scaling only one or two of the three axes makes scaling look like a dud**. The team replicated a then-circulating negative result: take the standard ResNet-50 / ImageNet recipe, swap in 10× more data, performance gets *worse*. Several blog posts at the time concluded that 1M images was about the ceiling.

The catch was that to see the benefit of 10× more data you also needed 10× more training time, and ideally a bigger model. Each axis on its own does nothing visible; pairs help a little; only all three together — data, model, duration — show the *large-scale pre-training is nice* effect.

Two slides ram the patience point home. Beyer's *favorite* plot of his career is a training curve: zoomed into the first 8 GPU-weeks, the loss looks dead flat — any reasonable person would kill the job. Zoomed out to 8 GPU-*months*, it's still climbing meaningfully. They were not reasonable, and that's why the result exists. The companion lesson is hyperparameter foresight: a weight-decay sweep where the eventually-winning value looks like the worse one in the first few preliminary runs. Pick on early curves, you kill the right model. This kind of detail-sensitivity is why scale wasn't just "obvious" — it required a lot of experience-built patience.

---

## 4. From class lists to CLIP: learning from web text (20:17)

Even granting "scale supervised pre-training," there's still the data bottleneck: where do you get labels? Up to this point everyone was doing the same thing — write a list of classes, then scrape or search the web for images per class. Beyer's favorite anecdote is COCO: 80 classes for over a decade of detection research, and **the classes came from the senior PI asking his 8-or-so-year-old American kid to list things they could think of** — microwave, pizza, frisbee, baseball. The whole community's detectors became excellent at recognizing what a North American 10-year-old thinks about. Always, the data ceiling was the creativity of whoever wrote the class list.

The escape is to **flip the procedure**: don't list classes and find images, list *images* and take whatever text is already attached to them on the web — alt text, captions, surrounding paragraphs. Most of it is junk ("thumbnail for version blah") but plenty of it is genuinely informative ("Frankfurt airport skyline") — and crucially, no class-list designer would ever have invented "Frankfurt airport skyline" as a category.

CLIP turned this raw web signal into a training procedure. The setup: take a big mini-batch (say 32k) of image-text pairs, encode each image and each text into a vector, and ask the model to match them — for each text, classify which image it goes with (softmax over dot products), and vice versa. Train both encoders end-to-end. **SigLIP** later simplified this into binary per-pair "do these match? yes/no" with sigmoid targets — same matrix structure, easier to scale, no global softmax. The breakthrough is conceptual more than algorithmic: the model can now learn whatever concepts the web happens to depict, not whatever a kid thinks of.

---

## 5. The English-only filter trap and globally diverse data (25:30)

What the community *did* with this newfound freedom was, to Beyer's frustration, to throw most of it away. A typical CLIP-data paper would take a giant raw image-text dataset and "improve" it by filtering: keep only pairs whose text words appear in English Wikipedia; keep only the English-language subset of LAION (the 2B everyone uses is the English-only slice of the 5B full set); use the *original* CLIP model — itself trained on English-only — to score and filter pairs; finally, keep only images that *look like* ImageNet examples. Each filter improved ImageNet eval, so each filter was declared good.

The problem is that ImageNet itself is North-American-biased, so this filtering pipeline silently pushes the model back into exactly the kind of cultural narrowness CLIP was supposed to escape from. Beyer's group ran a clean controlled experiment: pre-train with vs. without the English-only filter, evaluate on geographically diverse imagery. The English-filtered model identifies Tehran's Milad Tower as Toronto's CN Tower, and a cathedral in Brazil as one in Montreal. The unfiltered model gets both right.

The audience-thought-experiment that lands the point: close your eyes, think of a toilet. The American-data toilet you pictured is one of many — squat toilets and other regional variants are also toilets, and you won't see them in filtered data. The team built a globally-diverse benchmark to formalize this, showed that ImageNet-correlated benchmarks (COCO included) decouple from global-coverage benchmarks as you over-filter, and spent a project arguing the community out of the filtering habit.

---

## 6. CLIP's relational blindspot, the captioning fix, and "look at the data" (29:08)

There is a structural limit even an unfiltered CLIP can't escape. Consider a clean image of a cat sitting left of a dog with its perfect caption. The training task says: among all the captions in the mini-batch, find the matching one. To win that game the model only needs to spot *cat* and *dog* — if there's no other cat-and-dog image in the batch, it can ignore "sitting" and "left" entirely. To learn "sitting" it would need another mini-batch image with a cat-and-dog *not* sitting; to learn "left of" it would need one of them sitting the other way around. The combinatorics of waiting for these counterfactuals in random web data are hopeless, even at million-example batches. **CLIP shortcuts to bag-of-concepts.**

The fix, in hindsight obvious, is to add a generative objective: caption the image word-by-word, like an LLM. When the model is forced to choose "left" vs. "right" as the next token after "sitting," the relational structure has to be in the representation. The original CLIP paper had a figure declaring captioning "horribly less efficient" — Beyer's team reproduced that figure but showed it was a setup artifact, not a fundamental property. With the artifact removed, the captioning model nails the relational benchmarks.

This sets up the take-anything-away lesson of the lecture: **look at the data**. The flagship "vision-language models can't do relations" benchmark turned out to be solvable by a *blind* captioner — a model that captions without ever seeing the image — because items like "the horse is eating the grass" vs. "the grass is eating the horse" are decidable from text alone. The benchmark was broken; the field was getting fooled. This kind of breakage, Beyer notes, happens roughly every PhD generation in computer vision; every researcher should make a habit of opening their benchmarks. With proper relational benchmarks, captioning-pretrained models really do nail them — which is why **SigLIP v2 ships with a captioning loss and is the one you should use.**

---

## 7. Mid-training: installing core skills the VLM needs (34:30)

"Mid-training" is a recently-named stage — Beyer cites a tweet that describes it well: the steps after the bulk of self-supervised pre-training, for *shaping core capabilities*, before fine-tuning with RL for *exact behaviors*. The skills shaped here are ones you know will be useful across many downstream tasks but that pre-training won't give you cleanly: image-text matching or captioning won't teach a model "top-left" or "two meters away."

The canonical example is PaliGemma's architecture, which most VLMs share: an image encoder (a CLIP/SigLIP) produces a sequence of image tokens, they're concatenated with text tokens (typically a question or task spec), and a language model produces the answer — or for a VLA, actions. Mid-training is where you take these two pre-trained pieces, stitch them together, and feed them a curated mixture designed to *install skills*.

The mixture should be reasonably large but doesn't need to be pre-training-scale, and it doesn't need to be end-user-useful — its job is to force the skill into the model. Examples:

- **Captioning** of arbitrary images — baseline grounding.
- **OCR** — feed the model images with text and ask it to spit out the text or random chunks. The user doesn't care about "read this whole image" as a task, but the *capability* unlocks downstream document tasks.
- **Object presence, detection, segmentation, regional captioning** — "is X in this image?", "what's in this region?", question/answer inversions ("given this answer, what was the question?"). These are deliberately included in PaliGemma's mix to make it useful for robotics-style spatial reasoning.

Mid-training is also where you scale axes you couldn't afford during pre-training. The big one for vision is **resolution** — pre-training high-res is computationally hopeless, but mid-training can climb to higher resolutions where fine detail matters. For video, the analogous axis is context length; for 3D, more slices.

To get *non-text* outputs from a text-output model, the common trick is **VQ-VAE-style tokenization**: train a discrete dictionary in the bottleneck of an autoencoder, so any structured output (e.g. a segmentation mask) becomes a sequence of new discrete tokens that you simply add to the LLM's vocabulary. The detection-as-text version is even simpler — bin the x-axis into ~1024 bins (near pixel resolution) and emit bounding boxes as textual coordinates. With these tricks, almost any vision output is reachable from a single VLM trunk.

The payoff arrives in fine-tuning, where **skill transfer** happens: a model that learned segmentation on natural photos and learned satellite-image Q&A separately turns out to be able to segment things in satellite imagery — a task that was in neither mid-training nor fine-tuning explicitly.

---

## 8. Fine-tuning, "perception is solved," and what's still hard (41:30)

Beyer skips fine-tuning's mechanics — it's "a large mix of tons of specialized tasks" — and goes straight to a slightly provocative claim: **this recipe solves perception**.

The obvious counter is the "VLMs are blind" genre of papers — tasks like "how many intersections do these two kinked lines have?", which any human nails and frontier VLMs flunk. How can perception be "solved" if the benchmarks say no?

Beyer's answer is that the recipe is solved, not the deployed models. Any specific perception task — including the intersection-counting one — yields to ~128 examples of fine-tuning. He generated 128 examples of the intersection task and fine-tuned PaliGemma to ~95–96% accuracy; since it's a pure classification problem he also fine-tuned a bare SigLIP and got ~97%. The intrinsic skill (counting line intersections) is there in the pre-trained model; 128 examples are nowhere near enough to *learn* that skill, but they are enough to teach the model **what the user wants from this task**. The bottleneck is task-understanding, not perceptual capability.

So the recipe in practice: think of a perception task you need; collect a few hundred examples in an afternoon; fine-tune a good open VLM; ship — RL-tune if needed. Beyer is careful to caveat: "perception" here means *pure* perception. Tasks layered on top of perception — solve-my-homework, explain-why-this-is-funny, make-me-a-cappuccino-as-a-plan — need reasoning and planning, which this recipe doesn't deliver.

The hopeful endnote: this same recipe is now visibly working in other domains beyond language and vision — he flags a chemistry paper that lifts the entire structure. The unsatisfying part is the gap between *fine-tune-with-128-examples works* and *understand a new task from text alone* — robot learning lives squarely in that gap.

---

## 9. Q&A: small-scale pre-training, augmentations, frozen encoders, JEPA, distillation, and making humans smarter (46:50)

The Q&A runs long and surfaces several opinions worth their own headlines:

- **"Small-scale pre-training" is an oxymoron.** If you have a small data budget, fine-tune a pre-trained model; don't pre-train. The exception is synthetic-data-driven studies of pre-training dynamics. For fine-tuning hyperparameters, Beyer points to the PaliGemma paper, which catalogs which parameters are sensitive and in what order to tune them — and otherwise says fine-tuning is cheap, sweep them, and *trust your held-out split*.

- **Augmentations cap at ~10× equivalent data, and only after expensive tuning.** Their "How to train your ViT" paper studied this directly: augmentations help when you can't get more data, but if more data is at all gettable, get the data. **Deduplication is non-negotiable** — held-out benchmarks must not appear in pre-training, even fuzzily; their pipelines remove ~10M near-duplicates per 1B pre-training images using nearest-neighbor search on image embeddings, tuned for high recall (over-removal is fine). Without it, you're not measuring generalization, you're measuring leakage.

- **Don't freeze the encoder in your VLM.** PaliGemma's image trunk is a CLIP-style model, so it inherits CLIP's relational blindspot (the choice of CLIP over a captioning encoder was "big-corp technicalities"). The reason the resulting VLM still works on relational and locational tasks is precisely that PaliGemma does *not* freeze the encoder during mid-training/fine-tuning. Many open VLMs do freeze it — Beyer wouldn't use them for fine-tuning anything serious. The mid-training mix includes captioning so the encoder's bag-of-concepts limit gets corrected by gradient flow.

- **Try prompting first, in-context second, fine-tuning when needed.** Prompting is fine if it works (and if it works, the task was already in the SFT mix). In-context learning has gone back and forth in the literature and he doesn't rely on it. Fine-tuning is "annoying and boring, but just do it" — an afternoon of data collection is cheap.

- **On JEPA.** Beyer disputes the framing more than the direction: self-supervision in latent space has been around forever; JEPA mostly renames it. The direction is reasonable; the *hype* that JEPA outranks LLMs for reasoning, he doesn't share.

- **Perception "solved"? — pushback on streaming video.** A student presses that real perception is *streaming* — animals understand video as it arrives, focus where it matters, drop irrelevant tokens. Beyer concedes the streaming-efficiency problem isn't solved (and isn't in current SFT mixes much) but frames it as an *optimization* problem rather than a missing-capability one — VLMs can mostly do the *understanding* of video; the open work is doing it efficiently and online. He explicitly declines to opine on architectural details.

- **Web-scale dependency vs. humans.** A student asks whether we can reduce the data dependency. Beyer's answer is sharp: if you want a *general* model, no — a robot that has never seen a chair can't learn anything about chairs without continual learning. If you only need a *narrow* model (say, robot in a fixed factory), then yes — you don't need to have seen chairs, so the dependency drops accordingly.

- **Inference speed and distillation.** Especially for VLAs predicting long action chunks, real-time is a real problem. Beyond papers from PI-Robotics, Beyer wishes he'd put distillation in the slides: do everything to make the best model possible (pre-train, mid-train, fine-tune, RL-tune), *then* distill it into the small fast version with the latency you need. Distillation training is expensive but worth it — it can turn an unshippable model into a shippable one.

- **Memorization vs. fluid intelligence.** Asked whether fine-tuning evidence implies frontier VLMs have low fluid intelligence and are memorizing, Beyer doesn't endorse the EBM-style alternative but does agree this is the unsatisfying part of the current recipe. He sketches the camps: one says "keep adding tasks until generalization is forced" (which is partly happening in text); another says that approach is hopeless; another explores automatically generating few-shot examples from text prompts via a reasoning model and coding. Open problem.

- **Image encoders without text (DINO v3).** Not a fan. The text is there; why throw it away? DINO is the only no-text approach that gets reasonable performance at all, and even so it's clearly worse than text-supervised approaches. He grants it's intellectually interesting, but considers it self-imposed difficulty.

- **Making humans smarter.** Asked, half in jest, if his next adult job were to make *humans* smarter, how would he do it? — Beyer admits he doesn't have a good idea, but notes that LLMs are already a wonderful tool for *learning*: he'd have loved access to one 15-20 years ago instead of reading 20 mediocre tutorials. The frame slides to: maybe outsourcing cognition is fine the way the calculator was, as long as we're conscious about what we're outsourcing.
