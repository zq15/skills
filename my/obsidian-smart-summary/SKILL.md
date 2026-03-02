---
name: obsidian-smart-summary
description: "Generate intelligent summaries for Obsidian vault folders or multiple notes, providing a quick overview of content landscape and key insights. Use when user says: '帮我总结一下这个文件夹', 'summarize my vault', '这里都有什么', '帮我做个知识盘点'."
metadata:
  { "openclaw": { "emoji": "📚", "requires": { "bins": ["obsidian-cli"] } } }
---

# Smart Summary — Obsidian Vault & Folder Summarization

Generate intelligent summaries for an entire vault folder or a set of notes, helping users quickly understand content landscape, key themes, and important insights.

## When to Use

- User wants an overview of a vault folder or topic area
- User says "帮我总结一下这个文件夹", "summarize my vault", "这里都有什么"
- User wants a summary of multiple related notes
- User says "帮我做个知识盘点", "generate a summary from my notes"
- User wants a periodic knowledge review

## Required Tools

- `obsidian-cli list [folder]` — List notes in vault or a specific folder
- `obsidian-cli search "<topic>"` — Find notes by topic for topic-based summaries
- `obsidian-cli search-content "<topic>"` — Search inside notes
- `obsidian-cli print "note/path"` — Read full note content

## Workflow

### Step 1: Identify Scope

Determine what the user wants summarized:

**Option A: Entire vault or specific folder**
```bash
obsidian-cli list
# or a specific folder:
obsidian-cli list "FolderName"
```

**Option B: Specific topic across vault**
```bash
obsidian-cli search-content "<topic keywords>"
```

**Option C: User specifies exact notes**
Proceed directly to reading them.

### Step 2: Get Note List

For folder summary, list the notes:

```bash
obsidian-cli list "FolderName"
```

This gives all note names and structure within the folder.

### Step 3: Sample and Read Notes

For large folders (>20 notes), use a sampling strategy:

1. **Read all notes** if ≤10 notes
2. **Sample strategically** if >10 notes:
   - Read README or index notes first
   - Pick 2-3 notes from each major subfolder
   - Prioritize recently modified notes
   - Read up to 10-15 notes total

```bash
obsidian-cli print "folder/note-name"
```

State the sampling approach clearly: "文件夹共有 X 篇笔记，我抽样阅读了 Y 篇进行分析。"

### Step 4: Analyze and Categorize

As you read, track:
- **Main themes** — What topics are covered
- **Content types** — Tutorials, references, notes, specs, etc.
- **Coverage depth** — Which areas are well-documented vs sparse
- **Freshness** — How recently content was updated

### Step 5: Generate Summary

```markdown
## 📚 知识摘要：「[文件夹/主题名称]」

### 概览
- **笔记总数**：X 篇
- **涵盖文件夹**：[列表]
- **主要语言**：中文/英文/混合

---

### 🗂️ 内容结构

1. **[板块名称]**（X 篇笔记）
   - [简要描述]
   - 代表笔记：[[笔记标题]]

2. **[板块名称]**（X 篇笔记）
   - [简要描述]

---

### 🔑 核心要点

1. **[要点 1]**：[2-3 句话概括]
2. **[要点 2]**：[2-3 句话概括]
3. **[要点 3]**：[2-3 句话概括]

---

### 📊 内容健康度

| 指标 | 状态 |
|------|------|
| 内容覆盖 | [全面/有缺口/待补充] |
| 更新频率 | [活跃/一般/较少更新] |
| 结构清晰度 | [清晰/一般/需要整理] |

---

### 💡 建议

- [建议 1：如"XX 主题内容较少，建议补充"]
- [建议 2：如"部分笔记已较久未更新，建议检查时效性"]
```

## Guidelines

- Be upfront about sampling when you can't read everything
- Focus on actionable insights, not just listing note titles
- Highlight gaps and opportunities — what's missing is as valuable as what's there
- Use `[[wikilink]]` format for note references

## Error Handling

| Situation | Action |
|-----------|--------|
| `list` returns empty folder | Inform user the folder appears to be empty |
| `print` fails for some notes | Skip those notes, continue with others |
| Vault/folder has >50 notes | Sample 10-15 notes, clearly state the sampling approach |
| User doesn't specify folder | Ask which folder or topic to summarize |
