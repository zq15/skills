---
name: obsidian-meeting-notes
description: "Format meeting content into structured meeting notes and save them to your Obsidian vault. Use when user says: '帮我整理会议纪要', 'save meeting notes', '把会议记录存到 Obsidian', '帮我记录一下这次会议'."
metadata:
  { "openclaw": { "emoji": "📋", "requires": { "bins": ["obsidian-cli"] } } }
---

# Meeting Notes — Format and Archive to Obsidian

Take raw meeting information from the user, format it into a standard meeting notes template, and create a note in the Obsidian vault.

## When to Use

- User shares meeting content and wants it saved to Obsidian
- User says "帮我整理会议纪要", "save meeting notes", "把会议记录存到 Obsidian"
- User pastes unstructured meeting notes and wants them formatted and archived

## Required Tools

- `obsidian-cli create "Meeting Notes/[title]" --content "..."` — Create the meeting notes note

## Workflow

### Step 1: Gather Meeting Information

Extract or ask for the following from the user's input:

| Field | Required | Example |
|-------|----------|---------|
| 会议主题 (Topic) | Yes | "Q1 产品规划评审" |
| 会议日期 (Date) | Yes (default: today) | "2024-01-15" |
| 会议时间 (Time) | No | "14:00-15:30" |
| 参会人员 (Attendees) | Yes | "张三、李四、王五" |
| 主持人 (Host) | No | "张三" |

If the user provides raw/unstructured content, extract these fields from context. If critical fields are missing (topic, attendees), ask the user.

### Step 2: Structure the Content

Organize the meeting content into these sections:

1. **议题 (Agenda Items)** — What was discussed
2. **讨论要点 (Discussion Points)** — Key arguments, opinions, data shared
3. **决议 (Decisions)** — What was decided
4. **待办事项 (Action Items)** — Who does what by when
5. **备注 (Notes)** — Anything else worth recording

For each action item, ensure it has:
- **负责人** (Owner): Who is responsible
- **截止日期** (Deadline): When it's due
- **具体内容** (Description): What needs to be done

### Step 3: Format the Document

Use this template:

```markdown
# 会议纪要：[会议主题]

| 项目 | 内容 |
|------|------|
| 📅 日期 | YYYY-MM-DD |
| ⏰ 时间 | HH:MM - HH:MM |
| 📍 地点 | [线上/会议室名称] |
| 👥 参会人 | [姓名列表] |
| 🎙️ 主持人 | [姓名] |
| ✍️ 记录人 | [姓名/AI 助手] |

---

## 📋 议题

1. [议题 1]
2. [议题 2]

---

## 💬 讨论要点

### 议题 1：[标题]

- [要点 1]
- [要点 2]

---

## ✅ 决议

1. **[决议 1]**
2. **[决议 2]**

---

## 📌 待办事项

| # | 事项 | 负责人 | 截止日期 | 状态 |
|---|------|--------|----------|------|
| 1 | [具体任务] | [姓名] | YYYY-MM-DD | ⬜ 待开始 |
| 2 | [具体任务] | [姓名] | YYYY-MM-DD | ⬜ 待开始 |

---

## 📝 备注

- [其他需要记录的内容]

---

> 本纪要由 AI 助手整理，如有遗漏请补充。
```

### Step 4: Save to Vault

```bash
obsidian-cli create "Meeting Notes/会议纪要：[主题] - YYYY-MM-DD" --content "<formatted markdown>"
```

If "Meeting Notes" folder doesn't exist, obsidian-cli will create it automatically.

### Step 5: Confirm

```markdown
✅ 会议纪要已创建！

📄 **[[会议纪要：主题 - 日期]]**
📁 已归档到：Meeting Notes/

### 摘要
- 共讨论 X 个议题
- 形成 X 项决议
- 产生 X 个待办事项
```

## Guidelines

- Default to Chinese for the document content
- Keep the document well-structured; prefer tables for action items
- If the user provides audio transcription, clean up filler words and organize by topic
- Preserve the user's original wording for decisions and action items — don't paraphrase important commitments
- Auto-generate a short title from the meeting topic if the user doesn't provide one

## Error Handling

| Situation | Action |
|-----------|--------|
| User provides very little info | Ask for at least: topic, attendees, key decisions |
| `create` fails | Show error; offer to output the markdown for manual copy |
| No clear action items | Still create the note, add "本次会议无明确待办事项" |
