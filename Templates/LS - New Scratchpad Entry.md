<%*
const today = tp.date.now("YYYY-MM-DD");
const folder = "Projects (Knowledge from implementation)/Learning System/Scratchpad";
const targetPath = `${folder}/${today}.md`;
const exists = app.vault.getAbstractFileByPath(targetPath);

if (exists) {
    await app.workspace.getLeaf().openFile(exists);
    new Notice(`Opened existing scratchpad for ${today}`);
} else {
    const content = `# ${today}\n\n`;
    const targetFolder = app.vault.getAbstractFileByPath(folder);
    const newFile = await tp.file.create_new(content, today, false, targetFolder);
    await app.workspace.getLeaf().openFile(newFile);
    new Notice(`Created scratchpad for ${today}`);
}
// Remove this trigger note
const currentFile = tp.config.target_file;
if (currentFile && currentFile.basename.startsWith("Untitled")) {
    await app.vault.delete(currentFile);
}
_%>
