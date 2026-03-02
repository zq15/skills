---
name: obsidian-knowledge-connect
description: "Discover connections between Obsidian notes, build knowledge networks, and establish bidirectional wikilinks. Use when user says: '有哪些相关笔记', 'find related notes', '帮我建立知识关联', '这个主题还有哪些相关的', '构建知识图谱'."
metadata:
  { "openclaw": { "emoji": "🗺️", "requires": { "bins": ["obsidian-cli"] } } }
---

# Knowledge Connect — Discover Note Relationships & Build Knowledge Networks

Help the user discover hidden connections between their Obsidian notes, find related content, and build a knowledge network with bidirectional wikilinks.

## When to Use

- User wants to find notes related to a specific topic
- User says "有哪些相关笔记", "find related notes", "帮我建立知识关联"
- User wants to build a knowledge map for a topic
- User says "这个主题还有哪些相关的", "帮我串联一下知识", "构建知识图谱"

## Required Tools

- `obsidian-cli search-content "<keyword>"` — Search for related notes by content
- `obsidian-cli search "<keyword>"` — Search by title
- `obsidian-cli print "note/path"` — Read note content to analyze connections
- `obsidian-cli list [folder]` — Browse notes for broader discovery
- `obsidian-cli create "note/path" --append --content "..."` — Add cross-references to notes
- `obsidian-cli create "Maps/[topic]" --content "..."` — Save knowledge map

## Workflow

### Step 1: Identify the Starting Point

The user may provide:
- A specific note to find connections for
- A topic or keyword to explore

If starting from a note:

```bash
obsidian-cli print "folder/note-name"
```

Extract key concepts, terms, and themes from the note.

### Step 2: Discover Related Notes

Search with multiple keywords to cast a wide net:

```bash
obsidian-cli search-content "<keyword 1>"
obsidian-cli search-content "<keyword 2>"
obsidian-cli search "<related term>"
```

Use:
- Direct topic keywords
- Synonyms and related terms
- Key concepts mentioned in the source note
- Technical terms

### Step 3: Read and Analyze Connections

For each potentially related note (top 5-10):

```bash
obsidian-cli print "folder/related-note"
```

Analyze the relationship type:

| Relationship | Description |
|-------------|-------------|
| 🔗 直接相关 | Same topic, different angle |
| 🧩 互补 | Fills gaps in each other |
| 📚 前置/后续 | Sequential knowledge |
| 🔀 交叉引用 | Shared concepts across topics |
| ⚡ 矛盾/对比 | Conflicting viewpoints |

### Step 4: Build the Knowledge Map

Present the discovered connections:

```markdown
# 🗺️ 知识关联图：[主题/笔记标题]

> 基于「[[起始笔记]]」发现的知识网络
> 扫描时间：YYYY-MM-DD

---

## 🎯 中心节点

**[[起始笔记标题]]**
- 核心概念：[概念1]、[概念2]、[概念3]

---

## 🔗 关联笔记

### 直接相关

| 笔记 | 关联类型 | 关联说明 |
|------|----------|----------|
| [[笔记标题]] | 🔗 直接相关 | [为什么相关] |
| [[笔记标题]] | 🧩 互补 | [互补点说明] |

### 延伸阅读

| 笔记 | 关联类型 | 关联说明 |
|------|----------|----------|
| [[笔记标题]] | 📚 前置知识 | [说明] |
| [[笔记标题]] | 🔀 交叉引用 | [共同概念] |

---

## 🧠 知识网络

```
[[中心笔记]]
├── 🔗 [[直接相关笔记 1]]
├── 🧩 [[互补笔记 2]]
└── 📚 [[前置笔记 3]]
```

---

## 💡 发现与建议

- **知识聚类**：[发现的知识聚类模式]
- **知识缺口**：[发现缺少的关联笔记或主题]
- **建议行动**：
  1. [建议创建的笔记或补充的内容]
  2. [建议建立的新关联]
```

### Step 5: Add Cross-References (Optional)

Ask before modifying any existing note:
- "要在这些笔记中添加相互引用（`[[wikilink]]`）吗？"

If the user agrees, append a "相关笔记" section:

```bash
obsidian-cli create "folder/note-name" --append --content "

---

## 🔗 相关笔记

- [[相关笔记 1]] — [关联说明]
- [[相关笔记 2]] — [关联说明]"
```

### Step 6: Save Knowledge Map (Optional)

```bash
obsidian-cli create "Maps/🗺️ 知识图谱：[主题]" --content "<knowledge map content>"
```

### Step 7: Confirm

```markdown
✅ 知识关联分析完成！

🗺️ **发现 X 篇相关笔记，建立了 X 个关联**

- 🔗 直接相关：X 篇
- 🧩 互补笔记：X 篇
- 📚 前置/后续：X 篇

💡 建议：[最重要的一条建议]
```

## Guidelines

- Start broad, then narrow — search with multiple keywords to find unexpected connections
- Quality over quantity — 5 strong connections are better than 20 weak ones
- Explain why notes are related, not just that they are
- Always ask before modifying existing notes (adding cross-references)
- Use `[[wikilink]]` format — this is native to Obsidian and enables graph view
- Default language is Chinese

## Error Handling

| Situation | Action |
|-----------|--------|
| `search-content` returns few results | Broaden keywords; try synonyms |
| Starting note has no clear connections | Suggest the note may be on a new topic |
| Too many connections found (>15) | Prioritize by relevance strength; group into clusters |
| `create --append` fails | Skip that note; note it in the report |
| Vault is very small | Acknowledge limited scope; suggest topics to write about |
