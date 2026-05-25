---
date: 2026-04-25
purpose: Compare 4 ways to visually wrap AI replies inside a markdown note while still rendering markdown inside.
---

# Block Format Comparison

Each section below contains the **same reply content** so you can compare visual styles directly. Open this file in Obsidian (reading view) to see how each renders.

What to evaluate as you scroll:

1. Does inline `code` render?
2. Does the ```` ``` ```` fenced code block render?
3. How visually distinct is the wrapper from surrounding prose?
4. Does it feel like "fighting with the original context"?
5. Is it collapsible?

---

## Type 1 — Plain `>` block quote (current default)

Some surrounding context paragraph here, pretending to be the body of a deep-dive note. The user leaves a `%%` comment asking a question.

> **回覆：**
>
> The `cat` command outputs file contents to stdout. You can also use it with heredoc:
>
> ```bash
> cat << 'EOF'
> hello
> world
> EOF
> ```
>
> The single quotes prevent shell expansion of `$VAR` etc.

More surrounding context after the reply.

**Expected issues:** The triple backticks render as literal ``` ``` ``` characters inside the quote (not as a code block). Inline `backticks` may or may not render depending on theme.

---

## Type 2 — Obsidian callout (basic, `[!note]`)

Some surrounding context paragraph here, pretending to be the body of a deep-dive note.

> [!note] 回覆
> The `cat` command outputs file contents to stdout. You can also use it with heredoc:
>
> ```bash
> cat << 'EOF'
> hello
> world
> EOF
> ```
>
> The single quotes prevent shell expansion of `$VAR` etc.

More surrounding context after the reply.

**Expected behavior:** Code block renders correctly. Inline backticks render. Callout has a colored left border + icon + header. Always expanded.

---

## Type 3 — Obsidian callout (collapsible, `[!quote]-`)

Some surrounding context paragraph here, pretending to be the body of a deep-dive note.

> [!quote]- 回覆 (click to expand)
> The `cat` command outputs file contents to stdout. You can also use it with heredoc:
>
> ```bash
> cat << 'EOF'
> hello
> world
> EOF
> ```
>
> The single quotes prevent shell expansion of `$VAR` etc.

More surrounding context after the reply.

**Expected behavior:** Same as Type 2, but **collapsed by default**. Click the header to expand. Use `[!quote]+` instead if you want collapsible-but-open-by-default. The `[!quote]` type has gentler coloring than `[!note]`.

---

## Type 4 — HTML `<details>` tag

Some surrounding context paragraph here, pretending to be the body of a deep-dive note.

<details>
<summary>回覆 (click to expand)</summary>
The `cat` command outputs file contents to stdout. You can also use it with heredoc:

```bash
cat << 'EOF'
hello
world
EOF
```

The single quotes prevent shell expansion of `$VAR` etc.

</details>

More surrounding context after the reply.

**Expected behavior:** Native HTML disclosure widget. Collapsed by default. Markdown renders inside (the blank lines around content are required). Visually minimal — just a small triangle + summary text. No colored border or icon.

```
Turns out that you have to look at this section with book mode. CMD + E to turn into book mode. It's pretty interesting.
```


---

## Other callout types worth comparing

If you like Type 2/3 but want a different vibe, swap the type keyword:

> [!info] info — blue
> Lighter blue, info icon.

> [!tip] tip — green
> Green, lightbulb icon.

> [!example] example — purple
> Purple, list icon.

> [!abstract] abstract — teal
> Teal, document icon.

> [!quote] quote — gray
> Gray, quote icon. Probably the most muted.

---

## My guess at your preference

Given you said callouts felt like "fighting with the original context," **Type 4 (`<details>`)** is probably the closest to what you want: collapsible, markdown renders, minimal visual wrapper. **Type 3 with `[!quote]-`** is the runner-up if you want a little more visual distinction.

Open in Obsidian reading view and see which one actually feels right.
