---
name: obsidian-stale-detector
description: "Detect stale and potentially outdated notes in your Obsidian vault by analyzing file modification timestamps and content freshness signals. Use when user says: '检查一下哪些笔记过期了', 'find stale notes', '我的知识库有哪些需要更新', '帮我做个知识库健康检查'."
metadata:
  { "openclaw": { "emoji": "🔎", "requires": { "bins": ["obsidian-cli"] } } }
---

# Stale Detector — Obsidian Vault Freshness Check

Scan your Obsidian vault to detect notes that haven't been updated for a long time and may contain outdated information.

## When to Use

- User wants to find outdated notes in their vault
- User says "检查一下哪些笔记过期了", "find stale notes"
- User says "我的知识库有哪些需要更新", "帮我做个知识库健康检查"
- User wants to do periodic vault maintenance

## Required Tools

- `obsidian-cli print-default --path-only` — Get vault path
- Bash `find` + `stat` — Check file modification times
- `obsidian-cli list [folder]` — List notes in a folder
- `obsidian-cli print "note/path"` — Read note content for deep scan

## Workflow

### Step 1: Get the Vault Path

```bash
VAULT=$(obsidian-cli print-default --path-only)
echo "Vault: $VAULT"
```

If `print-default` fails (no default set), ask the user for the vault path or folder to scan.

### Step 2: Scan File Modification Times

Get all `.md` files with their last modification time:

```bash
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" \
  -exec stat --format="%Y %n" {} \; | sort -n
```

Or to get human-readable dates:

```bash
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" \
  -printf "%TY-%Tm-%Td %f %p\n" | sort
```

To find files NOT modified in the last 365 days (expired):

```bash
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" \
  -not -newer "$VAULT/.obsidian" -mtime +365
```

Use graduated thresholds:

```bash
# Expired (>365 days)
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" -mtime +365

# Stale (180-365 days)
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" -mtime +180 -not -mtime +365

# Aging (90-180 days)
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" -mtime +90 -not -mtime +180
```

### Step 3: Classify Notes by Freshness

| Category | Age | Emoji |
|----------|-----|-------|
| 🟢 新鲜 (Fresh) | < 90 days | Recently updated, likely current |
| 🟡 老化 (Aging) | 90-180 days | May need review |
| 🟠 陈旧 (Stale) | 180-365 days | Likely needs update |
| 🔴 过期 (Expired) | > 365 days | High risk of outdated content |

### Step 4: Deep Scan Suspicious Notes (Optional)

For 🟠 or 🔴 notes, optionally read content to check for staleness signals:

```bash
obsidian-cli print "folder/note-name"
```

Look for:
- **Version references** — Mentions of specific software versions that may be outdated
- **Date references** — Hardcoded dates like "2023年计划", "Q1 目标"
- **Temporal language** — "目前", "最近", "即将" that imply time-sensitive content

Limit deep scanning to 5-10 notes.

### Step 5: Generate Report

```markdown
## 🔍 Vault 健康检查报告

### 📂 扫描范围
- **Vault 路径**：[路径]
- **笔记总数**：X 篇
- **扫描时间**：YYYY-MM-DD

---

### 📊 整体健康度

| 状态 | 数量 | 占比 |
|------|------|------|
| 🟢 新鲜（<90天） | X 篇 | XX% |
| 🟡 老化（90-180天） | X 篇 | XX% |
| 🟠 陈旧（180-365天） | X 篇 | XX% |
| 🔴 过期（>365天） | X 篇 | XX% |

**健康评分：X/10**

---

### 🔴 需要立即关注（过期笔记）

| # | 笔记路径 | 最后更新 | 已过天数 | 风险说明 |
|---|---------|----------|----------|----------|
| 1 | [[笔记名]] | YYYY-MM-DD | X 天 | [如：包含版本号引用] |

### 🟠 建议检查（陈旧笔记）

| # | 笔记路径 | 最后更新 | 已过天数 |
|---|---------|----------|----------|
| 1 | [[笔记名]] | YYYY-MM-DD | X 天 |

---

### 💡 维护建议

1. **优先处理**：[具体建议]
2. **批量更新**：[如"XX 文件夹的 X 篇笔记都超过半年未更新，建议集中审查"]
3. **考虑归档**：[如"XX 笔记可能已不再适用，建议归档"]
4. **定期检查**：建议每 [月/季度] 运行一次过期检测
```

## Guidelines

- Be helpful, not alarming — old notes aren't necessarily bad (some content is evergreen)
- Distinguish between time-sensitive content (process guides, tech docs) and evergreen content (principles, tutorials)
- Provide actionable suggestions — don't just list stale notes, suggest what to do about them
- When deep scanning, highlight specific outdated references

## Error Handling

| Situation | Action |
|-----------|--------|
| `print-default` fails | Ask user for vault path; fall back to asking for folder |
| `find` returns no results | Check if vault path is correct |
| All notes are fresh | Congratulate the user on maintaining a healthy vault! |
| Vault has >100 notes | Use metadata-only analysis (skip deep scan), offer to deep scan specific folders |
