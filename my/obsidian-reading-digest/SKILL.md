---
name: obsidian-reading-digest
description: "Distill Obsidian notes or external content into structured reading digests with key takeaways, summaries, and reading notes. Use when user says: '帮我总结这篇笔记', 'summarize this', '生成阅读摘要', '这篇文章讲了什么', '帮我提炼要点'."
metadata:
  { "openclaw": { "emoji": "📖", "requires": { "bins": ["obsidian-cli"] } } }
---

# Reading Digest — Document Summarization & Reading Notes

Help the user quickly distill a note or article into a structured reading digest with key takeaways, core arguments, and actionable insights.

## When to Use

- User wants a summary of a long note or article
- User says "帮我总结这篇笔记", "summarize this", "生成阅读摘要"
- User wants to extract key points from content for future reference
- User says "这篇文章讲了什么", "帮我提炼要点"

## Required Tools

- `obsidian-cli search "<keywords>"` — Find the target note by keyword
- `obsidian-cli search-content "<keywords>"` — Search inside notes
- `obsidian-cli print "note/path"` — Read full note content
- `obsidian-cli create "Reading Notes/[title]" --content "..."` — Save the digest

## Workflow

### Step 1: Locate the Content

The user may provide:
- A note title or keyword
- A direct path to a note
- Raw content pasted inline (article, transcript, etc.)

If the user provides a keyword or title:

```bash
obsidian-cli search-content "<keyword>"
# or
obsidian-cli search "<title>"
```

If the user pastes content directly, skip to Step 3.

### Step 2: Read the Note

```bash
obsidian-cli print "folder/note-name"
```

If the note is very long, note the total length and proceed with the full content.

### Step 3: Generate the Reading Digest

Analyze the content and produce a structured digest:

```markdown
# 📖 阅读摘要：[标题]

> **原文**：[[笔记名称]] 或 [外部来源]
> **阅读日期**：YYYY-MM-DD

---

## 🎯 一句话总结

[用一句话概括核心观点或目的]

---

## 📌 关键要点

1. **[要点 1]**：[简要说明]
2. **[要点 2]**：[简要说明]
3. **[要点 3]**：[简要说明]
4. **[要点 4]**：[简要说明]
5. **[要点 5]**：[简要说明]

---

## 🧠 核心论点与逻辑

[梳理核心论证逻辑，2-3 段]

---

## 💡 启发与思考

- [启发 1]
- [启发 2]
- [可以应用到的场景]

---

## 📝 原文金句

> [摘录值得记住的精彩段落 1]

> [摘录值得记住的精彩段落 2]

---

## 🔗 相关延伸

- [可以进一步阅读的方向 1]
- [可以进一步阅读的方向 2]

---

> 本摘要由 AI 助手生成，建议结合原文阅读。
```

### Step 4: Review with User

Present the digest to the user and ask:
- "摘要是否准确？有需要调整的地方吗？"
- "要保存到你的 Obsidian vault 吗？"

### Step 5: Save to Vault (Optional)

If the user wants to save:

```bash
obsidian-cli create "Reading Notes/📖 阅读摘要：[原文标题]" --content "<formatted digest>"
```

### Step 6: Confirm

```markdown
✅ 阅读摘要已生成并保存！

📄 **[[📖 阅读摘要：原文标题]]**
📁 已归档到：Reading Notes/

### 摘要概览
- 提炼了 X 个关键要点
- 摘录了 X 条原文金句
```

## Guidelines

- Preserve the author's original intent — don't distort or over-simplify
- Key points should be specific and actionable, not vague generalizations
- Include direct quotes from the original for important claims
- The "启发与思考" section should be personalized — relate to the user's context if known
- Default language is Chinese; match the source content language
- For very long content (>5000 words), break the digest into sections

## Error Handling

| Situation | Action |
|-----------|--------|
| `search` / `search-content` returns no results | Ask user for the exact note path |
| `print` fails (note not found) | Ask user to provide the note path or paste content directly |
| Content is very short (<200 words) | Generate a brief summary instead of full digest template |
| User pastes content inline | Process it directly, offer to save as a note |
