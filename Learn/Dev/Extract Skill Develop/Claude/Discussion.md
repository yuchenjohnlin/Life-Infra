So where am I right now ? Going back to the step before [[../Generate Chinese Subtitle/]], I just finished the clarification for yt-dlp and yt-api. 
Now I have enough understanding to come up with the skill, but there is still a long way from a well written skill. 
1. Confirm the steps for extracting metadata and subtitles. 
	1. Decide if the extraction for metadata and subtitles should be put in the same skill. Do they share enough relevant context to be put in the same skill ?
2. What is the seam or the format for the extracted metadata and subtitles. 
	1. Would I look at the raw subtitles ? 
	2. Do I need an interface to interact and manage the intermediate files ? 
	3. What if there are too much records to keep track of, will the file become too big ? 
3. How do I write good skills ? 
	1. Any references or resources ? 
	2. Should I have a file for reference so that in the future when I ask AI to generate skill, it can refer to the principles and methodology of the file ? 
---
#### Notes about Claude Plan Mode 
%% I tried to use plan mode in Claude to work on this, because I think plan mode might be smarter ? but I think it wasn't acting as what I thought. Plan mode would go through everything I have in the workspace, which I think might actually contaminate the context ? I don't know if there are any researches about this. Like do LLMs have attention like human do ? or do humans also get contaminated by the context (environment) but we just aren't aware of it. Anyways, I didn't want Claude to work through the whole thing on it's own and wanted Discussion like progress 
AI says : 
Plan mode is a Claude Code-specific mode (toggle with Shift+Tab to cycle through modes). While it's on:

- The agent can only read. No edits, no writes, no non-readonly bash. The single exception is a designated plan file the system tells the agent to write to.
- It forces a workflow: explore → design → write a plan to that file → call ExitPlanMode to surface it for approval. The user can edit the plan file directly before approving. After approval, normal mode resumes and the agent implements.
- The agent literally cannot start coding until the user approves, even if it wants to. That's the structural guarantee.

Is plan mode better for step-by-step discussion?

For what we've been doing — back-and-forth, you correcting me, me verifying with experiments, then small edits — normal mode is actually better. Plan mode optimizes for one-shot "agree on the plan, then go execute it". Our workflow has been the opposite: discuss, edit, discuss, edit. Forcing a plan-then-execute split would interrupt that.

You'd want plan mode when:
- The next step is a large change and you want to commit to an approach before any files get touched.
- You're worried the agent will jump to implementation before alignment (e.g., a fresh agent without your accumulated context).
- You want the plan itself as a written deliverable.

You'd stay in normal mode when:

- The work is exploratory / research-heavy.
- You want continuous incremental edits as you talk.
- You trust the agent to ask before doing risky things (which my system prompt requires).
Can normal mode plan?

Yes — normal mode is a strict superset. I can write a plan in chat, ask clarifying questions, and wait for your "go" before touching files. That's what we'd been doing implicitly until you flipped on plan mode for the skill-design step. The difference is: in normal mode, the discipline is mine; in plan mode, the discipline is enforced by the harness.

For your specific workflow — discussion-driven development with documentation as you go — I'd suggest normal mode by default, and only flip on plan mode when you want a written plan deliverable before a multi-step change. The skill-design step we just did was actually a good fit for plan mode (multi-step, well-scoped); Phase E (write a single methodology file) is small enough that normal mode is fine.
%%

### 
