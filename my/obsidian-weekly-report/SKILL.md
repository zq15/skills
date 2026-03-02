---
name: obsidian-weekly-report
description: "Generate weekly reports by analyzing recently modified Obsidian notes and git activity. Use when user says: '生成周报', 'weekly report', '本周工作总结', '帮我写个周报'."
metadata:
  { "openclaw": { "emoji": "📊", "requires": { "bins": ["obsidian-cli"] } } }
---

# Weekly Report — Vault Activity Weekly Report

Collect recent vault activity (recently modified notes, git commits if available) and generate a structured weekly report saved to Obsidian.

## When to Use

- User wants a weekly report based on recent vault activity
- User says "生成周报", "weekly report", "本周工作总结", "帮我写个周报"
- End-of-week knowledge activity review

## Required Tools

- `obsidian-cli print-default --path-only` — Get vault path
- Bash `find` — Get recently modified files
- Bash `git log` — Get git activity (if vault is in a git repo)
- `obsidian-cli print "note/path"` — Read recently modified notes for context
- `obsidian-cli create "Reports/[title]" --content "..."` — Save the weekly report

## Workflow

### Step 1: Get the Vault Path and Report Period

```bash
VAULT=$(obsidian-cli print-default --path-only)
```

Default report period: current week (Monday to Sunday).
Calculate the week boundaries:

```bash
# Start of current week (Monday)
WEEK_START=$(date -d "last Monday" +%Y-%m-%d 2>/dev/null || date -v-Mon +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)
```

### Step 2: Find Recently Modified Notes

Get all `.md` files modified in the past 7 days:

```bash
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" \
  -newer "$(date -d '7 days ago' +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d)" \
  -printf "%TY-%Tm-%Td %f %p\n" | sort -r
```

Or using `-mtime`:

```bash
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" -mtime -7 \
  -exec ls -la {} \; | sort -k6,7
```

Categorize by folder to understand what areas were active this week.

### Step 3: Check Git Activity (Optional)

If the vault is in a git repository:

```bash
git -C "$VAULT" log --since="7 days ago" --oneline --no-merges 2>/dev/null
```

This shows commit activity alongside file changes.

### Step 4: Read Key Notes for Context

Read a sample of recently modified notes (up to 5) to understand their content:

```bash
obsidian-cli print "folder/recently-modified-note"
```

This helps generate meaningful summaries rather than just listing file names.

### Step 5: Generate the Report

```markdown
# 📊 本周知识周报

> **周期**：YYYY-MM-DD（周一）至 YYYY-MM-DD（本周日）
> **生成时间**：YYYY-MM-DD

---

## 📈 本周概览

| 指标 | 数量 |
|------|------|
| 新建/修改笔记 | XX 篇 |
| 涉及文件夹 | XX 个 |
| Git 提交 | XX 次（如适用） |

---

## 📝 笔记动态

### 新建/修改的笔记

| 文件夹 | 笔记 | 修改日期 |
|--------|------|----------|
| [文件夹] | [[笔记名]] | MM-DD |
| [文件夹] | [[笔记名]] | MM-DD |

---

## 🗂️ 活跃领域

本周主要在以下领域有记录：

- **[领域/文件夹 1]**：[简要描述本周记录的内容]
- **[领域/文件夹 2]**：[简要描述本周记录的内容]

---

## 💡 本周亮点

[从笔记内容中提炼 2-3 个有价值的要点或进展]

1. [亮点 1]
2. [亮点 2]

---

## 📌 待跟进

[从笔记中发现的未完成事项或待补充内容]

- [ ] [待办 1]
- [ ] [待办 2]

---

> 📌 本报告基于 Obsidian vault 文件活动自动生成。
```

### Step 6: Save to Vault

```bash
obsidian-cli create "Reports/周报 $(date +%Y-W%V)" --content "<formatted report>"
# or with date range:
obsidian-cli create "Reports/周报 $WEEK_START ~ $TODAY" --content "<formatted report>"
```

### Step 7: Confirm

```markdown
✅ 周报已生成并保存！

📄 **[[周报 YYYY-MM-DD ~ YYYY-MM-DD]]**
📁 已归档到：Reports/

### 本周亮点
- 共新建/修改 X 篇笔记
- 主要活跃领域：[领域列表]
```

## Guidelines

- If the vault is not in git, skip the git section gracefully
- Keep suggestions constructive and specific
- Focus on knowledge activity, not just file counts
- Default report language is Chinese

## Error Handling

| Situation | Action |
|-----------|--------|
| `print-default` fails | Ask user for the vault path |
| `find` returns no results | Inform user no notes were modified this week |
| `git log` fails (not a git repo) | Skip git section, generate report from file activity only |
| No notes modified this week | Create a brief report noting low activity |
