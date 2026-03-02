---
name: obsidian-daily-capture
description: "Quickly capture ideas, thoughts, and fleeting notes to your Obsidian vault. Use when user says: '记一下', '帮我记录', 'capture this', '写个笔记', '这个想法先记下来', '随手记'."
metadata:
  { "openclaw": { "emoji": "📥", "requires": { "bins": ["obsidian-cli"] } } }
---

# Daily Capture — Quick Idea & Note Capture to Obsidian

Help the user quickly capture ideas, thoughts, meeting insights, reading annotations, and any fleeting information into their Obsidian vault with minimal friction.

## When to Use

- User wants to quickly jot down an idea or thought
- User says "记一下", "帮我记录", "capture this", "写个笔记"
- User shares a fleeting thought, inspiration, or meeting insight
- User says "这个想法先记下来", "随手记", "快速记录"

## Required Tools

- `obsidian-cli search "每日捕获 YYYY-MM-DD"` — Check if today's daily note exists
- `obsidian-cli print "Daily/YYYY-MM-DD"` — Read existing daily note
- `obsidian-cli create "Daily/YYYY-MM-DD" --content "..."` — Create daily note
- `obsidian-cli create "Daily/YYYY-MM-DD" --append --content "..."` — Append to daily note
- `obsidian-cli create "Notes/[title]" --content "..."` — Create standalone note

## Workflow

### Step 1: Receive the Capture

Classify the capture type:

| Type | Icon | Example |
|------|------|---------|
| 💡 想法/灵感 | 💡 | "突然想到可以用 Redis 做缓存" |
| 📝 笔记 | 📝 | "今天学到 Go 的 context 用法..." |
| 📖 阅读批注 | 📖 | "这篇文章提到的观点很有意思..." |
| 🎯 待办/行动 | 🎯 | "记得下周跟进 API 设计评审" |
| 💬 会议灵感 | 💬 | "会上讨论到的架构方案值得深入..." |
| 🔗 链接/资源 | 🔗 | "这个工具不错：https://..." |

### Step 2: Determine Capture Strategy

- **Strategy A (Default)**: Append to today's daily note. If it doesn't exist, create one.
- **Strategy B**: Create a standalone note (for longer or topic-specific captures).

If input is short (<100 words), default to Strategy A. If longer or clearly a standalone topic, use Strategy B.

### Step 3A: Daily Note — Append Mode

Check if today's daily note exists:

```bash
obsidian-cli search "每日捕获 $(date +%Y-%m-%d)"
# or
obsidian-cli print "Daily/$(date +%Y-%m-%d)"
```

If it exists, append to it:

```bash
obsidian-cli create "Daily/$(date +%Y-%m-%d)" --append --content "
---

### $(date +%H:%M) [类型图标] [简短标题]

[捕获内容]

[标签：#tag1 #tag2]"
```

If it doesn't exist, create today's daily note with the first capture:

```bash
obsidian-cli create "Daily/$(date +%Y-%m-%d)" --content "# 📥 每日捕获 $(date +%Y-%m-%d)

> 今日碎片化记录，定期整理归档。

---

### $(date +%H:%M) [类型图标] [简短标题]

[捕获内容]

[标签：#tag1 #tag2]"
```

### Step 3B: Standalone Note

```bash
obsidian-cli create "Inbox/[类型图标] [标题]" --content "[格式化笔记内容]"
```

### Step 4: Confirm

For daily note append:

```markdown
✅ 已捕获！

[类型图标] **[简短标题]** → 已追加到「📥 每日捕获 YYYY-MM-DD」
```

For standalone note:

```markdown
✅ 笔记已创建！

📄 **[[类型图标] 标题]**
📁 已保存到：Inbox/
```

## Guidelines

- Speed is everything — minimize questions, maximize capture
- If the user just throws a sentence at you, capture it immediately; don't ask for clarification
- Auto-generate a short title from the content if the user doesn't provide one
- Add relevant tags based on content analysis (e.g., #技术, #产品, #灵感)
- Keep the formatting lightweight — this is a quick capture, not a polished document
- Default to daily note append mode for short captures
- Use `Daily/YYYY-MM-DD` as the default path for daily notes (adjust if user has a different structure)
- Default language is Chinese

## Error Handling

| Situation | Action |
|-----------|--------|
| `print` fails (note not found) | Create new daily note |
| `create --append` fails | Try creating a new standalone note instead |
| User input is ambiguous | Capture as-is with 📝 type; don't over-classify |
| Very long input (>500 words) | Switch to standalone note strategy automatically |
