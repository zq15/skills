---
name: obsidian-style-extract
description: "Analyze the writing style of Obsidian notes and extract style characteristics including structure, tone, vocabulary, and formatting patterns. Use when user says: '分析一下这篇笔记的写作风格', 'extract the style', '帮我总结一下我的写作特点', '我想保持和这篇一样的风格'."
metadata:
  { "openclaw": { "emoji": "🎨", "requires": { "bins": ["obsidian-cli"] } } }
---

# Style Extract — Obsidian Note Writing Style Analysis

Analyze one or more Obsidian notes to extract writing style characteristics, helping users learn from excellent notes or maintain consistent writing style.

## When to Use

- User wants to analyze the writing style of a specific note
- User says "分析一下这篇笔记的写作风格", "extract the style"
- User says "学习这篇文档的风格", "帮我总结一下我的写作特点"
- User wants to maintain consistent style across notes
- User says "我想保持和这篇一样的风格"

## Required Tools

- `obsidian-cli search-content "<keywords>"` — Find target notes
- `obsidian-cli search "<title>"` — Search by title
- `obsidian-cli print "note/path"` — Read full note content for analysis
- `obsidian-cli list [folder]` — Browse notes to find examples

## Workflow

### Step 1: Identify Target Notes

The user may provide:
- A specific note title or path
- A keyword to search for the note
- A request to analyze their overall writing style (multiple notes)

If a specific note path is given:

```bash
obsidian-cli print "folder/note-name"
```

If the user gives keywords:

```bash
obsidian-cli search-content "<keywords>"
# Then read top results:
obsidian-cli print "folder/matched-note"
```

For overall style analysis, read 3-5 recent notes from the vault.

### Step 2: Analyze Style Dimensions

Examine the note(s) across these dimensions:

| Dimension | What to Look For |
|-----------|-----------------|
| 📐 结构 (Structure) | Heading hierarchy, section organization, use of lists vs paragraphs |
| 🎯 语气 (Tone) | Formal/informal, technical/conversational |
| 📝 用词 (Vocabulary) | Technical depth, jargon usage, Chinese/English mixing patterns |
| 📏 篇幅 (Length) | Average section length, paragraph density |
| 🎨 格式 (Formatting) | Use of tables, code blocks, callouts, emoji, wikilinks |
| 💡 表达 (Expression) | Use of examples, analogies, rhetorical questions |

### Step 3: Extract Style Profile

```markdown
## 📊 写作风格分析报告

### 笔记信息
- **笔记**：[[笔记标题]]
- **字数**：约 X 字

---

### 📐 结构特征

- **层级**：[如：使用 H2/H3 两级标题]
- **组织方式**：[如：总分总结构，先给结论再展开]
- **段落长度**：[如：每段 2-4 句，简洁明了]

### 🎯 语气与风格

- **整体基调**：[如：专业但不刻板]
- **人称使用**：[如：多用"我们"，营造协作感]
- **典型句式**：[引用 1-2 个代表性句子]

### 📝 用词特点

- **术语密度**：[高/中/低]
- **中英混用**：[如：技术名词保留英文，其余用中文]
- **高频词汇**：[列出 5-8 个特征性词汇]

### 🎨 格式偏好

- **常用元素**：[如：大量使用表格、代码块、wikilinks]
- **视觉节奏**：[如：每 2-3 段插入一个列表或表格]

---

### 🎯 风格摘要（一句话）

> [用一句话概括这个写作风格]

### 📋 风格复用建议

如果你想模仿这个风格写作，注意以下要点：
1. [具体建议 1]
2. [具体建议 2]
3. [具体建议 3]
```

### Step 4: Compare Styles (Optional)

If the user provides multiple notes for comparison:

```markdown
## 📊 风格对比

| 维度 | 笔记 A | 笔记 B |
|------|--------|--------|
| 语气 | [特征] | [特征] |
| 结构 | [特征] | [特征] |
| 用词 | [特征] | [特征] |
| 格式 | [特征] | [特征] |

### 共同点
- [共同特征 1]

### 差异点
- [差异 1]
```

## Guidelines

- Use concrete examples from the actual note — quote specific sentences or patterns
- Be objective and descriptive, not judgmental
- When analyzing multiple notes, identify both consistent patterns and variations
- The style profile should be actionable — someone should be able to write in a similar style after reading it
- Use `[[wikilink]]` format for note references

## Error Handling

| Situation | Action |
|-----------|--------|
| Note not found | Try alternative search keywords, then ask user for exact path |
| Note too short (<100 chars) | Inform user the note is too short for meaningful style analysis |
| `print` fails | Ask user to provide the note path directly |
| User provides no specific note | List recent notes and ask which to analyze |
