<%*
// Prompt for project name
const projectName = await tp.system.prompt("Project Name");
if (!projectName) return;

// Base path
const basePath = `Projects (Knowledge from implementation)/${projectName}`;

// Create folders
await app.vault.createFolder(basePath);
await app.vault.createFolder(`${basePath}/Scratchpad`);
await app.vault.createFolder(`${basePath}/Dev Log`);

// Create Goal.md
await app.vault.create(`${basePath}/Goal.md`,
`## Reminder\n\n> What problem does this project solve?\n> What does success look like?\n\n## Issue\n\n\n## How to Solve\n\n\n## What Success Looks Like\n\n`);

// Create Scratchpad/Scratchpad.md (quick capture checklist)
await app.vault.create(`${basePath}/Scratchpad/Scratchpad.md`,
`# Scratchpad\n\nQuick capture — jot anything here, sort it out later.\n\n- [ ] \n`);

// Create Dev Log homepage
const today = tp.date.now("YYYY-MM-DD");
await app.vault.create(`${basePath}/Dev Log/Dev Log.md`,
`---\ntype: devlog-index\nproject: "${projectName}"\ncreated: ${today}\n---\n\n# ${projectName} — Dev Log\n\n## Actions\n\n> [!tip] Quick Actions\n> - 📝 Add today's scratchpad → create \`Scratchpad/${today}.md\`\n> - ➕ Add a new task → use **Task** template in Dev Log folder\n> - 📊 View all tasks → open \`tasks.base\` in Dev Log\n\n## Task Tree\n\n*(Add task links here as the project grows)*\n\n`);

// Create the project homepage
await app.vault.create(`${basePath}/${projectName}.md`,
`---\ntype: project\nstatus: active\ncreated: ${today}\nupdated: ${today}\ntags:\n  - project\n---\n\n# ${projectName}\n\n> [!info] Status\n> **Phase:** Planning\n> **Started:** ${today}\n\n## Navigation\n\n- 📋 [[${projectName}/Dev Log/Dev Log|Dev Log]] — organized decisions & tasks\n- 💭 [[${projectName}/Scratchpad/Scratchpad|Scratchpad]] — quick capture\n- 🎯 [[${projectName}/Goal|Goal]] — what we're solving\n\n## Current Focus\n\n- [ ] Define the goal\n- [ ] First planning session in Scratchpad\n`);

// Navigate to the new project homepage
const file = app.vault.getAbstractFileByPath(`${basePath}/${projectName}.md`);
if (file) await app.workspace.getLeaf().openFile(file);

new Notice(`Project "${projectName}" created!`);
-%>
