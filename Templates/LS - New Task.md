<%*
const taskName = await tp.system.prompt("Task Name");
if (!taskName) { return; }

const folder = "Projects (Knowledge from implementation)/Learning System/Tasks";
const today = tp.date.now("YYYY-MM-DD");
const content = `---
type: task
status: todo
priority: medium
project: Learning System
created: ${today}
updated: ${today}
tags:
  - task
---

# ${taskName}

> [!question] Problem
> What needs to be done and why?

> [!success] Decision
> *(Fill in when decided)*

## Subtasks
- [ ]

## Debug
> [!bug]- Debug notes
> Symptom:
> Cause:
> Fix:
`;

const targetFolder = app.vault.getAbstractFileByPath(folder);
const newFile = await tp.file.create_new(content, taskName, false, targetFolder);
await app.workspace.getLeaf().openFile(newFile);
new Notice(`Task "${taskName}" created!`);

// Remove this trigger note
const currentFile = tp.config.target_file;
if (currentFile && currentFile.basename.startsWith("Untitled")) {
    await app.vault.delete(currentFile);
}
_%>
