---
name: obsidian-note-refine
description: "Refine and restructure existing Obsidian notes into well-organized, deduplicated, and enriched documents. Use when user says: '帮我整理笔记', 'refine my notes', '把这些笔记理一下', '这些笔记太乱了', '帮我重新组织一下'."
metadata:
  { "openclaw": { "emoji": "✨", "requires": { "bins": ["obsidian-cli"] } } }
---

# Note Refine — Restructure & Polish Obsidian Notes

Help the user transform scattered, rough notes into well-structured, deduplicated, and enriched documents. Turn chaos into clarity.

## When to Use

- User wants to clean up messy notes
- User says "帮我整理笔记", "refine my notes", "把这些笔记理一下"
- User has accumulated daily captures and wants to consolidate them
- User says "这些笔记太乱了", "帮我重新组织一下", "去重整理"

## Required Tools

- `obsidian-cli search-content "<keywords>"` — Find target notes to refine
- `obsidian-cli search "每日捕获"` — Find daily capture notes
- `obsidian-cli print "note/path"` — Read full note content
- `obsidian-cli create "path" --content "..."` — Save refined document
- `obsidian-cli create "path" --overwrite --content "..."` — Update in place

## Workflow

### Step 1: Identify the Source Notes

The user may provide:
- A specific note to refine
- A date range of daily captures to consolidate
- A topic keyword to find related scattered notes
- Multiple note references to merge

If the user says "整理我最近的笔记":

```bash
obsidian-cli search "每日捕获"
```

Or for topic-specific notes:

```bash
obsidian-cli search-content "<topic keyword>"
```

### Step 2: Read All Source Notes

For each identified note, read its full content:

```bash
obsidian-cli print "folder/note-name"
```

Read up to 5-10 source notes. If there are more, prioritize by recency and relevance.

### Step 3: Analyze and Plan

Before refining, analyze the raw content:

1. **Identify themes** — Group related content by topic
2. **Find duplicates** — Flag repeated ideas or information
3. **Spot gaps** — Note where information is incomplete
4. **Assess structure** — Determine the best organizational approach

Present the analysis to the user:

```markdown
## 📋 笔记分析

**来源**：X 篇笔记，共约 XXXX 字

### 主题分布
- **[主题 1]**：X 条相关记录
- **[主题 2]**：X 条相关记录

### 发现
- 🔄 发现 X 处重复内容
- 🕳️ 发现 X 处信息缺口
- 📊 建议整理为 X 篇主题笔记

要按这个方向整理吗？
```

### Step 4: Refine the Notes

Refined note template:

```markdown
# [主题标题]

> 整理自 X 篇笔记，时间跨度：YYYY-MM-DD 至 YYYY-MM-DD
> 最后整理：YYYY-MM-DD

---

## 概述

[对这个主题的整体概述，2-3 句话]

---

## [分类 1]

### [子主题 1.1]

[整理后的内容]

---

## 待补充

- [ ] [识别出的信息缺口 1]
- [ ] [识别出的信息缺口 2]

---

## 原始来源

- [[原笔记 1]] — YYYY-MM-DD
- [[原笔记 2]] — YYYY-MM-DD

---

> 本笔记由 AI 助手整理，原始笔记已保留。
```

### Step 5: Save the Refined Note

Ask the user's preference:
- **Create new** — Save as a new note (recommended for multi-note consolidation)
- **Update in place** — Replace the original note (for single note refinement)

For new note:

```bash
obsidian-cli create "Notes/[主题标题]" --content "<refined content>"
```

For in-place update:

```bash
obsidian-cli create "Notes/[note-name]" --overwrite --content "<refined content>"
```

### Step 6: Confirm

```markdown
✅ 笔记整理完成！

📄 **[[主题标题]]**
📁 已保存到：Notes/

### 整理成果
- 📥 输入：X 篇原始笔记，约 XXXX 字
- 📤 输出：1 篇结构化笔记，约 XXXX 字
- 🔄 去除重复：X 处
- 🕳️ 标记待补充：X 处
```

## Guidelines

- Always preserve the original notes — refine into a new note by default
- Don't discard information during deduplication; merge and enrich instead
- Maintain the user's voice and terminology — don't over-formalize casual notes
- Flag uncertain interpretations with "【待确认】" markers
- Use `[[wikilink]]` format for internal references
- Default language is Chinese

## Error Handling

| Situation | Action |
|-----------|--------|
| Source notes are too few (<3 items) | Refine what's available; suggest capturing more first |
| Source notes are too many (>10) | Focus on most recent or ask user to narrow the scope |
| Content is already well-structured | Tell user honestly; suggest minor improvements only |
| `create --overwrite` fails | Fall back to creating a new note |
| Mixed languages in notes | Maintain the dominant language; don't force translation |
