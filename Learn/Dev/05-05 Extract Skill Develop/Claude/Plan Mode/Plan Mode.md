 I tried to use plan mode in Claude to work on this, because I think plan mode might be smarter ? but I think it wasn't acting as what I thought. Plan mode would go through everything I have in the workspace, which I think might actually contaminate the context ? I don't know if there are any researches about this. Like do LLMs have attention like human do ? or do humans also get contaminated by the context (environment) but we just aren't aware of it. Anyways, I didn't want Claude to work through the whole thing on it's own and wanted Discussion like progress 
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
