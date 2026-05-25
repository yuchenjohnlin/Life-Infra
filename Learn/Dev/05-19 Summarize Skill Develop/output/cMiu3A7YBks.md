---
id: cMiu3A7YBks
url: https://www.youtube.com/watch?v=cMiu3A7YBks
title: "Adv. LLM Agents MOOC | UC Berkeley Sp25 | Open Training Recipes: LLM Reasoning by Hanna Hajishirzi"
aliases:
  - "Adv. LLM Agents MOOC | UC Berkeley Sp25 | Open Training Recipes: LLM Reasoning by Hanna Hajishirzi"
channel: Berkeley RDI
channel_url: https://www.youtube.com/channel/UCB67PxhB5LAWEbI4etQS7aw
duration: 4853
upload_date: 20250303
processed_at: 2026-05-25T00:00:00
thumbnail: https://i.ytimg.com/vi/cMiu3A7YBks/maxresdefault.jpg
view_count: 8475
transcript_file: "[[Learn/Dev/05-19 Summarize Skill Develop/input/cMiu3A7YBks|cMiu3A7YBks]]"
type: youtube-digest
state: active
---

# Adv. LLM Agents MOOC | UC Berkeley Sp25 | Open Training Recipes: LLM Reasoning by Hanna Hajishirzi

> [!quote]- Source description (cleaned)
> _(No description provided by the uploader.)_

> [!info] Orientation
> A guest lecture in UC Berkeley's Spring 2025 *Advanced LLM Agents* MOOC (Berkeley RDI) by **Hanna Hajishirzi**, who co-leads NLP at the Allen Institute for AI (Ai2) and is a professor at the University of Washington. Hajishirzi heads the **OLMo** (open language model) and **Tulu** (open post-training recipe) efforts at Ai2 — both fully open in weights, data, and code. The talk surveys what her group has learned about building reasoning-capable LLMs across three orthogonal axes (pretraining / mid-training, post-training, and test-time inference), with particular emphasis on the Tulu 3 recipe and the introduction of **RLVR** (reinforcement learning with verifiable rewards). It is pitched at a research-literate graduate audience already familiar with RLHF, DPO/PPO, and chain-of-thought.

## TL;DR

A working tour of how Ai2 builds a frontier-comparable reasoning model entirely in the open — and what each stage actually contributes. The throughline: **data quality dominates algorithmic cleverness at every stage**, and modern post-training is best understood as a three-step recipe (SFT → preference tuning → RLVR) layered on a base model whose mid-training has been deliberately patched for reasoning.

- **Post-training is where reasoning is mostly built.** Tulu 3's recipe — SFT, then preference tuning, then RLVR — applied on Llama 3 405B reaches parity with GPT-4o and beats DeepSeek V3 on average.
- **SFT lives or dies by the data mix.** Hybrid human + synthetic data, persona-driven prompt generation for diversity, and aggressive decontamination matter more than fancy training tricks. Self-consistency filtering throws away ~40% of synthetic CoT data with no quality loss.
- **For preference tuning, PPO > DPO but only marginally, and data swamps both.** Switching DPO → PPO buys ~1 point; better preference data alone buys ~5. On-policy completions and in-domain prompts are the main levers.
- **RLVR is the new ingredient.** Replace the neural reward model with a rule-based verifier (gold answer match, constraint satisfaction) for tasks where correctness is checkable. Simple, stable, and — crucially — it only works once the base model is strong enough to explore productively. Scales better at 405B than at 70B.
- **Test-time scaling can be embarrassingly simple.** S1 fine-tunes on just **1,000** carefully curated reasoning traces and forces longer thinking by appending a `"wait"` token whenever generation tries to stop early. That alone produces clean inference-time scaling curves on AIME and MATH500.
- **Mid-training is the secret pretraining step.** The last ~1% of pretraining tokens, at a decayed learning rate, is upsampled high-quality math / code / reasoning data — and is what lets RLVR work downstream. Patching specific weaknesses (e.g. injecting synthetic multiplication data after noticing OLMo couldn't multiply) is part of the loop.

## Chapters

| #            | Chapter                                                                  | Time    | Uploader's chapters |
| ------------ | ------------------------------------------------------------------------ | ------- | ------------------- |
| **Part I**   | Why fully open, and what Ai2 has shipped                                 |         |                     |
| 1            | [[#1. The case for a fully open LLM ecosystem (00:00)]]                  | 00:00   | —                   |
| 2            | [[#2. Snapshot of OLMo 2 and Tulu 3 results (04:15)]]                    | 04:15   | —                   |
| **Part II**  | The Tulu 3 post-training recipe                                          |         |                     |
| 3            | [[#3. Why post-training is where reasoning is built (06:04)]]            | 06:04   | —                   |
| 4            | [[#4. Curating prompts and decontaminating evals (11:08)]]               | 11:08   | —                   |
| 5            | [[#5. SFT data mixing across capability verticals (13:43)]]              | 13:43   | —                   |
| 6            | [[#6. Reasoning data: CoT, personas, and self-consistency filtering (20:21)]] | 20:21   | —                   |
| 7            | [[#7. The final SFT mix and ablations (30:14)]]                          | 30:14   | —                   |
| 8            | [[#8. Preference tuning: RLHF, DPO vs PPO (33:32)]]                      | 33:32   | —                   |
| 9            | [[#9. The Tulu 3 preference-tuning recipe (45:24)]]                      | 45:24   | —                   |
| 10           | [[#10. RLVR: replacing the reward model with a verifier (49:28)]]        | 49:28   | —                   |
| 11           | [[#11. Why RLVR works now, and how it scales (58:49)]]                   | 58:49   | —                   |
| **Part III** | Test-time scaling                                                        |         |                     |
| 12           | [[#12. S1: a 1K-example recipe and "wait"-token budget forcing (1:04:23)]] | 1:04:23 | —                   |
| 13           | [[#13. Self-RAG and OpenScholar: self-guided generation (1:12:33)]]      | 1:12:33 | —                   |
| **Part IV**  | Back to the base model                                                   |         |                     |
| 14           | [[#14. Mid-training: patching reasoning into the base model (1:14:57)]]  | 1:14:57 | —                   |
| 15           | [[#15. Closing: what is still open (1:19:37)]]                           | 1:19:37 | —                   |

---

## 1. The case for a fully open LLM ecosystem (00:00)

Hajishirzi opens with a position rather than a result: today's AI progress exists *because of* open scientific research and access to fully open models, and that openness is now eroding. The conclusion she rejects is that language-model science is therefore "done" — there is still a great deal to understand about how these models work, how to push them beyond chat into health and science, how to mitigate bias and risk, and how to make them efficient enough to deploy. To do that science, the community needs models that are transparent (data is inspectable), accessible, and reproducible. This is the mandate behind the two efforts her team leads at UW and Ai2: **OLMo** — fully open pretraining — and **Tulu** — fully open post-training. Both projects insist that artifacts, data, and code be released together, not just weights. She is careful to position this open ecosystem as one piece of a larger landscape, not a claim that closed labs are unnecessary.

The talk is then organized around three orthogonal axes where the team has worked to improve reasoning: pretraining, post-training, and test-time inference.

---

## 2. Snapshot of OLMo 2 and Tulu 3 results (04:15)

Before the methods, the headlines. **OLMo 2** ships at 7B and 13B; at the end of pretraining the base model is on average on par with Llama 3 and Qwen 2.5 of the same size, while using *fewer* training tokens — placing it on the Pareto frontier of average benchmark performance vs pretraining FLOPs. **Tulu 3** is the post-training recipe; applied on top of Llama 3.1 **405B**, it lands on par with or better than DeepSeek V3 and roughly matches GPT-4o. The point is not just the numbers but the existence proof: a fully open, fully documented recipe can close the gap to leading proprietary models. The rest of the talk unpacks what that recipe actually contains, starting with post-training because that is where most of the reasoning capability is shaped.

---

## 3. Why post-training is where reasoning is built (06:04)

A modern LLM is built in two large stages. **Pretraining** does next-token prediction on trillions of tokens of mostly web text; the resulting model is not safe, does not follow instructions reliably, and is not particularly good at reasoning. **Post-training** is what turns that base into something usable — it teaches the model to chat, to follow instructions, to use tools, to refuse unsafe requests, and, importantly, to reason through problems like multi-step arithmetic. Three ingredients carry through every stage: **data**, **model architecture** (a transformer in essentially every case), and a **thorough evaluation loop** that tells you where you are improving and where you are not. The talk's recurring claim is that *data* — what kind, from where, mixed how — is the dominant lever; algorithms come second.

The Tulu project, started in 2023, has converged on a three-step recipe applied on top of a base model: **instruction tuning** (SFT), **preference tuning**, and a new third step Hajishirzi will spend most of the talk justifying — **reinforcement learning with verifiable rewards (RLVR)**. The same recipe is applied to Llama, Qwen, and OLMo bases and reproducibly improves them.

---

## 4. Curating prompts and decontaminating evals (11:08)

Before any training, two foundational moves. First, establish the targeted skills and pin down the evaluations for each: general chat, knowledge, math and reasoning, coding, safety and refusal, multilinguality, and precise instruction-following under constraints. Some of these evaluation sets are public; some the team built themselves. They split eval sets into dev and held-out and only touch the held-out at the end — basic discipline that is, in Hajishirzi's telling, often skipped.

Second, **collect prompts and decontaminate ruthlessly**. The team checks licensing and consent, then runs decontamination against every evaluation set they care about. This matters more than people credit: it is easy for a complex instance to leak into training in a slightly altered form and silently inflate benchmark numbers. Their `open-instruct` toolkit ships the decontamination code; using it is the price of trusting any of the downstream numbers.

---

## 5. SFT data mixing across capability verticals (13:43)

SFT is mechanically simple — take a `(prompt, completion)` pair, fine-tune the base to imitate the completion. The interesting question is *which* prompts and completions. Three sources are available: human annotation (accurate but slow, expensive, high-variance, and increasingly impractical for complex reasoning), synthetic generation via a self-instruct loop using a stronger LLM (cheap and diverse but noisy and biased to the generator), and — what the team has converged on — a **hybrid** of the two.

The mixing problem is real. Add too much creative-writing data and math drops; add too much math and creative writing drops; the goal is high accuracy *across* the verticals simultaneously. Tulu 1's approach was to enumerate the available public datasets, evaluate each one against each capability vertical (chat, knowledge, reasoning, coding, multilinguality, safety), and combine the ones that scored well on different verticals. The result was a human + synthetic blend. ShareGPT showed strong early signal on chat but was dropped in later versions because its licensing and collection process were not defensible — a recurring theme: a dataset's *provenance* gates its long-term usability, not just its scores.

---

## 6. Reasoning data: CoT, personas, and self-consistency filtering (20:21)

Reasoning data needs special treatment. Take a word problem: "buy 2 get 1 free on $25 shirts, Sarah wants 7, how much?" If you SFT on `(question, "$125")`, the model learns very little. If you SFT on `(question, full chain-of-thought that decomposes the deal step by step, then "$125")`, the model learns a *procedure*. CoT data helps because it lets the model handle multi-step problems explicitly, makes errors locally inspectable, surfaces a reasoning skill the model has already been exposed to in pretraining, and resembles how humans explain things. The catch: collecting high-quality CoT manually is expensive, requires experts for hard problems, doesn't scale, and isn't diverse.

The team's answer is again hybrid, plus a trick they borrowed from the literature: **persona-driven synthetic generation**. Instead of asking GPT-4 to "write a hard math problem," they ask it to "write a math problem *for a chemical kinetics researcher*," or for a six-year-old, a computer scientist, a musician. The persona forces diversity along an axis that bland prompting collapses. With this approach they generated **150K hard math problems, 50K grade-school problems, and 35K coding / precise-instruction problems**, with GPT-4o and Claude Sonnet producing the step-by-step solutions.

Ablations show that increasing the persona-driven share of the math mix consistently improves MATH; GSM8K barely moves, because the existing public data was already adequate for grade-school problems. A second filtering step uses **self-consistency** — sample multiple reasoning paths from GPT-4 per problem and keep only the ones whose final answer matches the majority vote. This discards roughly 40% of the synthetic CoT data, and the remaining 60% matches the full set on MATH and *outperforms* it on GSM8K. Less but better data wins.

Alternative CoT-generation routes exist — converting math problems into Python (correctness guaranteed by execution but the reasoning is less naturally explanatory) or letting a strong base model self-generate CoTs (scalable but quality-bound by the base). The team uses a combination.

---

## 7. The final SFT mix and ablations (30:14)

Combining everything produces the Tulu SFT mix. The ablation table tells a consistent story: pulling any single component out hurts the vertical it targeted. Remove the wild-chat data and AlpacaEval scores collapse; remove persona data and math drops; remove the math data and math drops harder still. **Safety data was added without measurable damage to general capabilities** — an important negative result, since the worry about safety tuning is that it tax-es helpfulness. Against the popular alternatives (MAmmoTH-style and RLHF-collection-style mixes), the Tulu SFT mix wins on average. That closes step one of the recipe.

---

## 8. Preference tuning: RLHF, DPO vs PPO (33:32)

Step two is preference tuning, and the framing is important: in practice its main visible job is **style** — making chat responses better-formed — and it shows the biggest gains on chat evaluations. It still helps the other capabilities, just in smaller absolute amounts. Preference data is a `(prompt, response A, response B, preferred=A or B)` tuple, annotated either by humans or, increasingly, by another strong LLM (this is **RLAIF**). The format works because comparing two completions is far easier than scoring one in isolation.

Hajishirzi walks through the mechanics of RLHF: the policy generates the next token, gets reward from a reward model (a neural net trained on the preference data), and is updated by **PPO** — maximizing reward while constraining the policy to stay close to the reference SFT model. A wave of variants followed: **DPO** skips the explicit reward model and directly optimizes the policy against the preference data as a ranking objective; SimPO drops even the reference model; length-normalized PPO normalizes the log-likelihood by length.

The team did a systematic DPO-vs-PPO comparison. The headline: **PPO wins in almost every case, but only by ~1 point**, and it is substantially harder to implement at scale (two large models running concurrently — policy and reward model). The bigger gains came from elsewhere. Going from a weak DPO baseline to careful preference-data curation took average performance from 56 to 61 — *five points* — whereas swapping DPO for PPO on the same data added one more point. Scaling up the reward model gave less than half a point. The largest *targeted* gain came from injecting **in-domain prompts** for specific capabilities like GSM8K, which barely moved averages but produced significant boosts on reasoning. Takeaways: data quality dominates, DPO is the right choice for ablation-heavy development even if PPO wins at the finish line, reward-model scaling is a weak lever, and in-domain prompts are the precision tool.

---

## 9. The Tulu 3 preference-tuning recipe (45:24)

Translating those lessons into the Tulu 3 build: reuse some SFT prompts (to maintain accuracy on what already works), add some new in-distribution prompts, and bring in out-of-domain prompts for capabilities not seen in SFT. Generate completions from a wide range of models — small ones like Llama 7B all the way up to GPT-4 — so the preference comparisons span quality levels. Crucially, include **on-policy data**: completions from the Tulu 3 SFT model itself, so the preference pairs can pull it toward something better (a GPT-4 completion) or away from something worse. Use GPT-4 as the LLM-as-judge across four axes (helpfulness, instruction-following, truthfulness, honesty), binarize into chosen/rejected, optimize with DPO (PPO again didn't help much, and DPO is simpler).

The ablations are clean: on-policy alone gets to 60.7, off-policy alone to 60, combining both is best. New out-of-domain prompts beat reusing SFT prompts. GPT-4 as judge beat Llama-class judges by a small but real margin. None of these is a revolution; together they are the practical recipe.

---

## 10. RLVR: replacing the reward model with a verifier (49:28)

End of DPO. The training curves are telling: AlpacaEval plateaus, IFEval *drops* with more steps, GSM8K initially improves then **overfits and drops** — the model is over-optimizing against a neural reward model whose score for any given completion is essentially uninterpretable ("why 10.5? why not 1000? what does the score even mean?"), and the underlying human preferences it was trained on are themselves not a gold standard for reasoning quality.

The insight: **for any task whose correctness can be verified, the reward model can be replaced with a verifier.** If the question is "what is 2+2?" and the gold answer is 4, the reward is `1 if match else 0`. No neural net, no preference labels, no over-optimization on a wobbly proxy. They apply this to GSM8K, MATH, and precise instruction-following (where the verifier checks whether the generated text actually satisfies the stated constraints — "start every sentence with S," "write a five-word poem"). PPO does the optimization. DeepSeek R1, released around the same time, uses essentially the same idea under a different name.

The RLVR curves are qualitatively different from DPO: training accuracy on GSM8K and MATH **goes up and stays up**, no obvious over-optimization. Applied on top of SFT it helps; applied on top of DPO it helps more — the highest absolute numbers come from stacking RLVR on the DPO checkpoint. IFEval gains are smaller on the DPO base (likely a data-quantity issue, still being investigated). They even tried RLVR on FLAN data as a quick probe and saw improvements, suggesting the set of usefully verifiable tasks is larger than the obvious math/constraint cases.

---

## 11. Why RLVR works now, and how it scales (58:49)

RLVR is methodologically old — it is one of the simplest possible ways to use RL with reward data. So why does it suddenly work? The answer is the **base model**. Apply the same RLVR to GPT-2 and nothing happens, because the base model's reasoning accuracy is too low for productive exploration. Modern base models start strong enough that RL can find and amplify good behaviors. This is the same lesson the wider community is drawing from R1-style results — RL doesn't conjure capability, it polishes and extends what the base already has.

A consequence: **RLVR scales with model size**. On Llama at 70B, math improves from 42 to 45; at 405B, from 60 to 67 — a 7-point gain, more than twice as much. Better bases give RLVR more to work with. They also stack RLVR runs: cut training, start another stage, gain more, repeat. And switching the optimizer from PPO to GRPO applied to a Qwen math base pushes MATH performance to **84.6** — well above Tulu 3 405B's 67% — showing how quickly the frontier is moving in this regime. The Tulu 3 recipe is open and applies to Llama, Qwen, and OLMo bases; the demo is at `playground.allenai.org`.

---

## 12. S1: a 1K-example recipe and "wait"-token budget forcing (1:04:23)

Pivoting to test-time scaling, Hajishirzi presents the **S1** paper (led by Niklas Muennighoff) as a study in how minimal a recipe can be. Two ingredients: a carefully filtered training set (`s1K`) and a near-trivial inference-time mechanism.

The data starts as 59K hard reasoning problems — olympiad math, logic puzzles, probability — well beyond the high-school level Tulu 3 targets. Filter for quality down to 52K, for difficulty down to 24K, for diversity down to **1K**. The spoiler is that 1K performs essentially the same as 59K on their benchmarks. Each prompt is paired with a long reasoning trace distilled from a strong thinking model (initially Google's Gemini Thinking; later swapped for DeepSeek R1, which improved results). The traces deliberately include thinking-style tokens ("OK, this happens, but let me think more...").

Fine-tune Qwen 32B on this 1K set. At inference, apply **budget forcing**: if the model wants to stop generating before hitting the token budget, append the literal token `"wait"` and force it to continue; if it tries to run past the budget, append end-of-sentence and force it to stop. This is *not* a learned controller — there is no trained "decide when to wait" head; the harness just inserts the token. The result is a clean test-time scaling curve on MATH500, AIME, and PhD-level GPQA — more tokens, higher accuracy. Sequential budget forcing outperforms parallel majority voting. Replacing `"wait"` with other tokens (or not adding anything) loses much of the gain — the specific cue matters. Selecting the 1K via random sampling or just constraint matching is much worse — the filtering matters.

The lesson is uncomfortable in a productive way: a great deal of test-time reasoning can be unlocked with thoughtful data selection and a hack on the decoder loop.

---

## 13. Self-RAG and OpenScholar: self-guided generation (1:12:33)

Two other test-time directions, sketched briefly. **Self-RAG** trains the model not just to generate but to interleave **critic tokens** that judge whether retrieved documents are relevant and whether its own generated response makes sense — a self-supervised, in-loop critic rather than an external one. **OpenScholar** applies the same self-guided improvement loop to scientific literature synthesis, where producing a defensible answer requires combining many sources and reasoning about their consistency. A demo lives at `openscholar.allen.ai`. Both are presented as promising rather than complete — directions worth checking out — and reinforce a theme: at inference time, the model needs mechanisms for *being aware of what it is doing*, not just for generating more tokens.

---

## 14. Mid-training: patching reasoning into the base model (1:14:57)

The final axis returns to where the talk could have started: the base model. RLVR's dependency on a strong base means pretraining itself has to be designed with reasoning in mind. Modern pretraining is no longer one undifferentiated run; it has a **mid-training** stage at the tail end, occupying roughly 1% of training tokens, where the learning rate decays toward zero and the data is upsampled toward very high quality — heavily math, coding, and reasoning-oriented.

The pretraining body for OLMo 2 is ~4T tokens of web pages, code, academic and STEM papers, math web pages, and math proofs. The mid-training mix swaps in much more reasoning-heavy data and some SFT-style content. The effect is measurable: average benchmark scores jump from 50 to 60, and from 56 to 68, with the largest gains on GSM8K and DROP. Mid-training is also where you can do **targeted patching**: noticing that OLMo could add and subtract well but was weak at multiplication, the team injected synthetic multiplication data into the mid-training set and the deficit closed. The pretraining → mid-training split makes pretraining itself iterative — evaluate, find a hole, patch it before post-training.

The combined OLMo 2 results sit on par with Llama 3 8B (and a forthcoming 32B is in flight).

---

## 15. Closing: what is still open (1:19:37)

Closing with a deliberately open-ended list: a great deal remains — extending reasoning, building genuine agents, applying LMs to non-text domains like health, scaling test-time inference further, and continuing to push base models. The talk is also a recruitment pitch: the OLMo and Tulu projects at Ai2 and UW are hiring across all of these directions. The implicit closing argument matches the opening: this work is possible *because* the models, data, and pipelines are open, and progress will accelerate to the extent that the community keeps them that way.
