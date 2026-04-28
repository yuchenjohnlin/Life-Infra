---
source_url: https://www.youtube.com/watch?v=zvI4UN2_i-w
source_type: youtube
title: "Adv. LLM Agents MOOC | UC Berkeley Sp25 | Reasoning, Memory & Planning of Language Agents by Yu Su"
author: Berkeley RDI
channel_slug: berkeley-rdi
video_id: zvI4UN2_i-w
captured_at: 2026-04-28
processed_at: 2026-04-28
duration_seconds: 5559
status: processed
content_type: foundation
score:
  signal: 5
  depth: 5
  implementability: 2
  credibility: 5
  novelty: null
  overall: null
tags:
  - language-agents
  - memory
  - reasoning
  - planning
  - hippo-rag
  - grokking
  - mechanistic-interpretability
  - world-model
  - web-agents
raw_file: "[[berkeley-rdi-zvI4UN2_i-w]]"
---

# TL;DR

Yu Su argues for an **agent-first** view of language agents — not "LLM with a thin scaffold" but the classical AI-agent agenda upgraded with a new core capability: using language as the substrate for both communication *and* reasoning. Built on that framing, he walks through three deep dives from his group: **HippoRAG** (a hippocampal-indexing-inspired graph augmentation that gives RAG the pattern-completion ability vector similarity lacks), **Grokked Transformer** (showing transformers *can* learn implicit reasoning, but only via a long grokking phase that forms different "generalizing circuits" for composition vs. comparison — and that data distribution, not data size, is what controls it), and **WebDreamer** (model-based planning where an LLM simulates the next state of a website so a web agent can avoid the irreversible-action problem of tree search). He closes on safety and continual learning as the still-open frontiers.

# Viewing path

- 👀 Worth — Segment 1 (00:00-04:30): Hype check; LLM-first vs agent-first framing
- ⭐ Must — Segment 2 (04:30-11:30): Why "language for reasoning" is the actual upgrade — the unifying thesis
- 👀 Worth — Segment 3 (11:30-17:00): Conceptual framework / hierarchy of core competencies for language agents
- ⭐ Must — Segment 4 (17:00-25:00): Why parametric continual learning fails (catastrophic forgetting) and why non-parametric memory works
- ⭐ Must — Segment 5 (25:00-42:30): HippoRAG — hippocampal-indexing theory → Personalized PageRank over an LLM-extracted KG; v2 makes it a drop-in RAG replacement
- 👀 Worth — Segment 6 (42:30-54:30): Implicit reasoning setup — why study it, the synthetic-KG ID/OOD setup
- ⭐ Must — Segment 7 (54:30-1:00:00): Transformers *can* learn implicit reasoning — but through grokking; data distribution dominates
- ⭐ Must — Segment 8 (1:00:00-1:16:30): Mechanistic interpretation: composition (staged circuit) vs comparison (parallel circuit); cross-layer weight sharing fixes OOD; grokking = phase transition rote → generalize
- ⭐ Must — Segment 9 (1:16:30-1:27:30): Planning paradigms (reactive / tree search / model-based) + WebDreamer for web agents
- 👀 Worth — Segment 10 (1:27:30-1:32:30): Future directions: continual memory, reasoning under fuzzy rewards, planning, and the broad attack surface of language agents

## Segmentation

| Segment | Title | Time range |
|---|---|---|
| 1 | Agent hype & two views (LLM-first vs agent-first) | 00:00-04:30 |
| 2 | Reasoning as the new core capability | 04:30-11:30 |
| 3 | Conceptual framework for language agents | 11:30-17:00 |
| 4 | Memory motivation: why parametric continual learning fails | 17:00-25:00 |
| 5 | HippoRAG: hippocampal-indexing-based RAG | 25:00-42:30 |
| 6 | Implicit reasoning: setup & research questions | 42:30-54:30 |
| 7 | Grokking findings: composition vs comparison; data distribution | 54:30-1:00:00 |
| 8 | Mechanistic interpretation of grokking & circuits | 1:00:00-1:16:30 |
| 9 | Planning paradigms & WebDreamer (model-based planning) | 1:16:30-1:27:30 |
| 10 | Takeaways & future directions | 1:27:30-1:32:30 |

## Segments

### Segment 1: Agent hype & two views (00:00-04:30) [👀 worth]

Yu Su opens by acknowledging both the hype (Bill Gates, Andrew Ng, Sam Altman: 2025 = "year of agents") and the backlash ("just thin wrappers around LLMs", "autoregressive LLMs can never truly reason"). He grounds the discussion in Russell and Norvig's classical agent diagram to remind viewers that AI agents are not new — they've been a core pursuit of AI since the beginning. The cleanest split he draws in the community: an **LLM-first view** (start with a powerful LLM, scaffold around it with prompting and engineering — which is exactly the "thin wrapper" critics see) vs. his preferred **agent-first view** (the classical agenda — perceive, reason about state, build world models, plan — just upgraded with one or more LLMs integrated as a new substrate for reasoning and communication).

**Takeaway:** The framing matters because it changes what problems you think you're solving. LLM-first naturally leads to prompt engineering and orchestration; agent-first forces you to revisit the classical AI questions (state representation, world models, planning) through the lens of LLMs, plus tackle new opportunities like synthetic data at scale and o1-style internalized search. The rest of the talk is structured under the agent-first frame.

### Segment 2: Reasoning as the new core capability (04:30-11:30) [⭐ must]

This is the thesis segment. Yu Su argues the genuinely new thing LLMs bring to agents is using **language as a substrate for reasoning** — not just for communication. Communication-via-language we've been doing in dialogue systems for decades; what's new is that test-time token generation lets a model spend an *adaptive* amount of compute per problem (vs. classical ML where you pay a fixed compute per decision and have one shot). And in agents, reasoning is never reasoning for its own sake — it's reasoning for *better acting*: inferring environment state, self-reflection, dynamic replanning. He folds this back into the agent diagram by adding a new action type ("reason by generating tokens") and an internal environment (the inner monologue), so self-reflection becomes meta-reasoning. He also defends calling it "reasoning": LLMs only have one cognitive substrate (token generation) that blends Kahneman's perception, intuitive inference, and symbolic reasoning, so "reasoning" is the appropriate umbrella term — and "thoughts" risks over-anthropomorphizing.

**Takeaway:** Language-for-reasoning is the unifying capability, not "LLM-as-API". Adaptive compute (long CoT, o1-style search) becomes natural under this view. The naming choice — **language agents** — is deliberate: "multimodal agents" overweights perception; "LLM agents" makes the implementation incidental, while what's truly characteristic is universal language understanding/production, which an LLM is just one means to.

### Segment 3: Conceptual framework for language agents (11:30-17:00) [👀 worth]

Yu Su zooms out to the evolutionary history of AI agents — earlier generations could only capture single facets of human intelligence (symbolic reasoning, single-modality perception); multimodal-LLM-based language agents are the first time a model can encode multi-sensory inputs into a unified neural representation that's also conducive to symbolic reasoning. He compares language agents against logical agents on expressiveness (much higher — fuzzy and flexible is a feature not a bug, because the world itself is fuzzy), reasoning style (semi-explicit chain-of-thought vs. logical inference), and adaptivity (very high). He then shares his personal research framework: a loose hierarchy of core competencies — perception, memory, embodiment at the bottom, reasoning above them, planning above that, with cross-cutting concerns like safety, evaluation, synthetic data, and efficiency.

**Takeaway:** This framework is what he uses to map any new agent paper to a contribution slot — useful for orienting your own reading. The rest of the talk picks three slots from this hierarchy: long-term memory (HippoRAG), reasoning (Grokked Transformer), and planning (WebDreamer).

### Segment 4: Memory motivation: why parametric continual learning fails (17:00-25:00) [⭐ must]

The memory section opens with Eric Kandel's "memory is everything" and biology — humans are 24/7 learners; even sleep replays the day to consolidate long-term memory via synaptic plasticity. The problem: replicating this in LLMs runs straight into **catastrophic forgetting**. Because of distributed representations, edits cause unintended ripple effects — the canonical example is "Leonardo is now a citizen of Syria": you'd expect downstream facts (he speaks Arabic, etc.) to update consistently, but in practice the negation of the original statement still predicts Syria, the language field also becomes Syria instead of Arabic, and so on. Continual learning by parameter editing is fundamentally hard. The good news is **non-parametric memory** — keep new experience external to the model and retrieve as needed (i.e. RAG). For this to work, LLMs must be receptive to external evidence even when it conflicts with parametric memory. Their "Adaptive Chameleon or Stubborn Sloth" study showed they are highly receptive — a coherent counter-memory will flip the answer (good for non-parametric memory; mildly worrying for safety, but he flags and moves on).

**Takeaway:** Three load-bearing points: (1) catastrophic forgetting blocks parametric continual learning for LLMs, so memory has to be external; (2) RAG-style non-parametric memory is the practical path forward; (3) the receptiveness study justifies trusting the external memory channel — but it's the same receptiveness that makes prompt-injection attacks effective.

### Segment 5: HippoRAG: hippocampal-indexing-based RAG (25:00-42:30) [⭐ must]

The bulk of the memory section. Yu Su critiques vanilla embedding RAG with a running example: "which Stanford professor works on the neuroscience of Alzheimer's?" If the relevant facts are split across separate passages (one says X is at Stanford, another says X works on Alzheimer's), embedding similarity ranks all Stanford professors and all Alzheimer's researchers equally — the model has to manually scan to find Professor Thomas. Human memory doesn't work this way; we form **associations** that allow **pattern completion** — recovering whole memories from partial cues. He grounds this in the **hippocampal indexing theory**: raw memory lives in neocortex, but a structured index in the hippocampus links disparate units. HippoRAG mimics this: an offline indexing phase uses an LLM as the "neocortex" to extract triples (open IE — schemaless KG), consolidates them with a dense retriever, and builds a graph; the online phase, given a query, does NER to find seed concepts, finds matching nodes, then runs **Personalized PageRank** from those seeds. Nodes at the intersection of multiple seeds (Professor Thomas being connected to both Stanford and Alzheimer's) accumulate the most weight, and these weights re-rank the original passages. Results on multi-hop QA beat dense retrievers by a large margin and complement iterative methods like IRCoT. **HippoRAG v2** fixes a big practical gap — v1 (and other graph-augmented methods like GraphRAG, LightRAG, RAPTOR) underperformed large embedding models like Grit / NV-Embed on simple QA and discourse tasks, so they couldn't be drop-in replacements; v2 closes that gap so it's now broadly comparable or better.

**Takeaway:** The principled idea: vanilla RAG ≈ neocortex without a hippocampus, which is why multi-hop and association-style queries fail. The engineering takeaway: schemaless KG built by LLM-IE + Personalized PageRank is a surprisingly simple recipe that recovers the missing structure, and v2 means there's no longer a tradeoff between "structured retrieval" and "raw retrieval quality." If you build long-term memory for an agent, this is a strong reference design.

### Segment 6: Implicit reasoning: setup & research questions (42:30-54:30) [👀 worth]

Setup for the reasoning section. Implicit reasoning = no chain-of-thought; ask the model to predict the answer in a single forward pass. Why study it when CoT is everything right now? Three reasons: (1) it's the *default* mode of pre-training — the cross-entropy next-token objective forces the model to do implicit reasoning to compress data; (2) it determines how well the model acquires structured representations of facts and rules; (3) one plausible hypothesis for how o1/R1-style long CoT emerges from RL is that the base model *already* contains implicit reasoning circuits (self-reflection, analogical reasoning), and RL with verifiable rewards just incentivizes the right combinations. Prior work concluded LLMs struggle with implicit reasoning (the "compositionality gap"; even GPT-4 fails comparison reasoning like "Trump is 78, Biden is 82, who's older"). Yu Su's group disagreed and ran a careful study with two questions: can transformers *ever* learn implicit reasoning, and what controls it? Setup: standard GPT-2 decoder; synthetic data — a random KG with atomic facts, plus inferred facts via a composition rule (h-r1-b + b-r2-t ⇒ h-r1-r2-t). They split into ID/OOD where OOD = atomic facts seen but never composed before, testing **inductive learning of deduction rules**.

**Takeaway:** The motivation for studying implicit reasoning is that it's the substrate everything else (including CoT) sits on. The OOD = "systematic generalization" definition is the bar — if a model passes it, it has learned the rule, not memorized examples.

### Segment 7: Grokking findings: composition vs comparison; data distribution (54:30-1:00:00) [⭐ must]

The headline result. Transformers *can* learn implicit reasoning — but only through **grokking**: training accuracy hits 100% (overfit) very early, but test accuracy stays low; only if you keep training ~20× *more* steps (log scale!) does generalization suddenly emerge and test accuracy jump to 100%. Two surprises follow. First, the level of systematicity varies by reasoning type: **composition never generalizes OOD**, but **comparison does**. Second, contrary to a popular hypothesis in the grokking literature that there's a critical *data size* threshold, their experiments show it's the **data distribution** that matters — specifically the ratio φ (inferred facts ÷ atomic facts). Holding the ratio fixed and scaling data size doesn't speed up generalization; holding data size fixed and increasing φ from 3.6 to 18 dramatically speeds it up, eventually making generalization as fast as overfitting.

**Takeaway:** Two practical-ish lessons. (1) "LLMs can't reason implicitly" is false — they *can*, given the right training regime; but the regime is severe (long training past overfit), which has implications for how pre-training corpora should be designed. (2) For continual training or RL on reasoning, increase the ratio of *derived* facts to atomic facts in your data, not just the volume — distribution > size.

### Segment 8: Mechanistic interpretation: circuits & phase transition (1:00:00-1:16:30) [⭐ must]

Why the difference between composition and comparison? Using logit lens and causal tracing, Yu Su's group shows that after grokking the transformer forms different **generalizing circuits** for the two reasoning types. Composition develops a **staged circuit**: lower layers (≈layer 0–5 in their setup) memorize the first-hop atomic facts and produce the bridge entity b at the r1 position; the model also has to *defer* processing of r2 and store the second-hop atomic facts in *upper* layers, so that once b emerges it can be combined with r2 to predict t. OOD generalization for composition fails because in OOD the model has only seen each atomic fact individually, so it has no incentive to also store the second-hop facts in upper layers — extra effort with no training-time payoff. Comparison develops a **parallel circuit** instead: lower layers retrieve both attribute values (78, 82) in parallel and upper layers do the comparison; only one copy of the atomic facts is needed, so OOD works automatically. They validate the hypothesis with a clean intervention: **cross-layer parameter sharing** (tie lower and upper layer weights). Boom — composition now generalizes OOD, because the lower-layer atomic facts are automatically available in upper layers. The second half of the segment explains *what* grokking is mechanistically: it's a **phase transition from rote learning to generalization**. Right at overfit, the bridge entity b is already present in the residual stream (MRR=1 at the right position), but r2 isn't there yet at the bridge position; the model is using a memorize-everything circuit that ignores r2 and directly predicts t. Through grokking, r2 gradually appears at the right position, and causal tracing shows the bridge entity gains causal strength over the final prediction. The intuition for *why* grokking happens past overfit is **circuit efficiency under regularization** — the generalizing circuit is more efficient than the memorizing circuit, and L2 regularization gradually favors it once training loss is saturated.

**Takeaway:** This is the most conceptually rich slide cluster of the talk. Three concrete things to walk away with: (1) different reasoning types have *structurally different* circuits, and architecture interventions like cross-layer weight tying can directly fix systematic generalization gaps; (2) grokking ≠ magic — it's a regularization-driven shift between two coexisting circuits; (3) the "can't reason" critique misreads what's happening internally — the right question is not "can it?" but "under what training regime does the generalizing circuit win?"

### Segment 9: Planning paradigms & WebDreamer (1:16:30-1:27:30) [⭐ must]

Planning gets a working definition: given goal g, choose actions a0..an reaching a state passing g. Yu Su contrasts language-agent planning with classical planning: goal specification is now natural-language (much more expressive than formal languages), action spaces are open-ended (especially for web agents, where actions are dynamically populated by the page), and the goal test is harder to automate — but fuzziness is an inherent property of the world and that's OK. He pitches the work series MindWeb → SeeAct → UGround as moving toward a human-like embodiment for computer-use agents (pixels in, pixel-level operations out). Three planning paradigms: **reactive** (ReAct) — fast and easy, but greedy and short-sighted; **tree search** — backtracking gives systematic exploration, but real environments contain irreversible actions (placing orders, accepting terms, changing privacy settings on amazon.com — there's no universal undo) and exploration is unsafe and slow; **model-based planning** — simulate candidate actions with a world model first, evaluate long-term value and safety, then commit. The hard part is getting a world model: classical RL world models work for simple environments with millions of trials, but the internet is far too complex. Yu Su's group's insight: LLMs already have enough common-sense knowledge from pre-training to reasonably predict state transitions ("if I click this shirt icon, the next page is a product detail page with sizing options"). **WebDreamer** uses GPT-4o as the world model: at each state, simulate each candidate action (multistep is possible), use another LLM as the value function, take the highest-valued action. On VisualWebArena it beats reactive planning and slightly trails tree search — but tree search is only feasible in a sandbox; on real websites it would break, while WebDreamer remains workable, cheaper, and faster.

**Takeaway:** The argument structure to internalize: tree search is the canonical answer to "I want lookahead", but it assumes reversibility — a property real environments don't have. Model-based planning with an LLM-as-world-model is the practically deployable lookahead strategy for web/computer-use agents. If you build agents that act on real systems, this is a more honest baseline than ReAct.

### Segment 10: Takeaways & future directions (1:27:30-1:32:30) [👀 worth]

Yu Su closes by identifying what's still open. **Memory** — personalization and continual learning are barely touched; episodic memory with spatial-temporal aspects has no good solution. **Reasoning** — making o1/R1-style RL reasoning work for *language agents* with fuzzy rewards and external state is hard. **Planning** — better world models beyond LLM-simulators, and balancing reactive vs. model-based planning (you don't simulate every step, only hard ones — like humans). **Safety** is the one that "keeps me up at night": the attack surface of language agents = the entire internet for web agents (e.g., a benign-looking page can trick OpenAI's deep research agent into leaking private info); risks split into endogenous (incompetent agent takes irreversible action) vs. exogenous (environment attacks the agent). On the bright side, agentic search / deep research has the clearest business case for 2025, and he's personally excited about agents for science.

**Takeaway:** Useful as a "where does the field go next" map. The two safety categories (endogenous vs. exogenous) are a clean mental model worth borrowing. If you're building, the strongest practical pointer is to evaluate WebDreamer-style baselines and HippoRAG-style memory before defaulting to ReAct + vanilla RAG.

---

# Novelty (fill after watching)

<!-- Fill in after watching: which ideas were new vs. already-known but better-articulated? -->
