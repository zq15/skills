---
name: obsidian-smart-search
description: "Search your Obsidian vault with natural language queries and provide summarized answers with key points and source note references. Use when user says: '搜一下我的笔记', 'search my vault', '我的知识库里有没有...', 'find notes about'."
metadata:
  { "openclaw": { "emoji": "🔍", "requires": { "bins": ["obsidian-cli"] } } }
---

# Smart Search — Obsidian Vault Search & Q&A

Search across your Obsidian vault using natural language, read relevant notes, and synthesize a clear answer with references.

## When to Use

- User asks a question that might be answered by their Obsidian notes
- User wants to find specific information in their vault
- User says "搜一下我的笔记", "search my vault", "我的知识库里有没有..."
- User says "find notes about", "查一下我记过的..."

## Required Tools

- `obsidian-cli search "query"` — Search note titles/names
- `obsidian-cli search-content "query"` — Search inside notes (shows snippets)
- `obsidian-cli print "note/path"` — Read full note content

## Workflow

### Step 1: Extract Search Keywords

From the user's natural language query, extract 1-3 concise keywords.

Examples:
- "我的部署流程文档在哪？" → keywords: `部署流程`
- "How do I handle error logging?" → keywords: `error logging`
- "我之前写的技术评审笔记" → keywords: `技术评审`

### Step 2: Search the Vault

First search note content (more thorough):

```bash
obsidian-cli search-content "<keywords>"
```

If results are sparse, also search by title:

```bash
obsidian-cli search "<keywords>"
```

If no results:
1. Try alternative keywords (synonyms, broader terms)
2. Try splitting compound terms
3. If still no results, tell the user honestly: "在你的 Obsidian vault 中未找到相关笔记，建议尝试其他关键词或确认笔记是否存在。"

### Step 3: Filter and Rank Results

From the search results, select the top 3-5 most relevant notes based on:
- Title relevance to the query
- Snippet relevance (content match quality)
- Recency (prefer recently modified files)

### Step 4: Read Note Content

For each selected note, read its full content:

```bash
obsidian-cli print "folder/note-name"
```

Read up to 3 notes. If the first note fully answers the question, you may skip the rest.

### Step 5: Synthesize and Respond

Compose the answer in the following format:

```markdown
## 回答

[直接回答用户的问题，2-4 句话，简洁明了]

## 关键要点

- **要点 1**：[从笔记中提取的关键信息]
- **要点 2**：[从笔记中提取的关键信息]
- **要点 3**：[从笔记中提取的关键信息]

## 参考笔记

1. [[笔记名称]] — [所在文件夹]，更新于 YYYY-MM-DD
2. [[笔记名称]] — [所在文件夹]，更新于 YYYY-MM-DD
```

## Guidelines

- Answer in the same language the user used (Chinese or English)
- Quote specific content from notes when relevant — use `>` blockquotes
- If notes contain conflicting information, note the discrepancy and mention which is more recent
- If the answer is only partially found, say what you found and what's missing
- Never fabricate information not present in the notes
- Use `[[wikilink]]` format for note references

## Error Handling

| Situation | Action |
|-----------|--------|
| `search-content` returns empty | Try `search` by title, then try alternative keywords |
| `print` fails (note not found) | Skip this note, try the next result |
| Too many results | Focus on top 3 by relevance |
| Query is very broad | Ask user to narrow down the topic |
