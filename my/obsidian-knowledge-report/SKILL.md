---
name: obsidian-knowledge-report
description: "Generate comprehensive monthly knowledge management reports by analyzing Obsidian vault content health, note counts, and activity metrics using the file system. Use when user says: '生成知识月报', 'knowledge report', '知识管理月报', '帮我分析一下我的知识库健康度'."
metadata:
  { "openclaw": { "emoji": "📈", "requires": { "bins": ["obsidian-cli"] } } }
---

# Knowledge Report — Obsidian Vault Monthly Knowledge Management Report

Collect vault metrics from the file system (note counts, modification times, folder structure, word counts) and generate a detailed monthly knowledge management report.

## When to Use

- User wants a monthly knowledge management report
- User says "生成知识月报", "knowledge report", "知识管理月报"
- Monthly review of vault documentation health and activity
- User says "帮我分析一下我的知识库健康度"

## Required Tools

- `obsidian-cli print-default --path-only` — Get vault path
- Bash `find` — Count files, find recently modified notes
- Bash `wc -l` / `wc -w` — Estimate word counts
- `obsidian-cli list [folder]` — List notes by folder
- `obsidian-cli print "note/path"` — Read notes for content analysis
- `obsidian-cli create "Reports/[title]" --content "..."` — Save the report

## Workflow

### Step 1: Get Vault Path and Report Period

```bash
VAULT=$(obsidian-cli print-default --path-only)
MONTH=$(date +%Y年%m月)
MONTH_START=$(date -d "$(date +%Y-%m)-01" +%Y-%m-%d 2>/dev/null || date -v1d +%Y-%m-%d)
```

### Step 2: Collect Vault Metrics

#### 2a. Total Note Count

```bash
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" | wc -l
```

#### 2b. Notes Created/Modified This Month

```bash
# Modified this month
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" \
  -newer "$VAULT/.obsidian" -mtime -30 | wc -l

# More precise: use find with date comparison
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" \
  -newermt "$(date +%Y-%m)-01" | wc -l
```

#### 2c. Folder Structure and Note Distribution

```bash
# Count notes per top-level folder
for dir in "$VAULT"/*/; do
  count=$(find "$dir" -name "*.md" 2>/dev/null | wc -l)
  echo "$count $(basename "$dir")"
done | sort -rn
```

#### 2d. Estimate Total Word Count

```bash
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" \
  -exec wc -w {} \; | awk '{sum += $1} END {print sum}'
```

#### 2e. Stale Notes (Not Modified in 90+ Days)

```bash
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" -mtime +90 | wc -l
```

### Step 3: Sample and Analyze Content

Read a few recently modified notes (up to 5) to provide content context:

```bash
find "$VAULT" -name "*.md" -not -path "*/.obsidian/*" -mtime -30 \
  -printf "%TY-%Tm-%Td %p\n" | sort -r | head -5
```

Then read each:

```bash
obsidian-cli print "folder/note-name"
```

### Step 4: Generate the Report

```markdown
# 📊 知识管理月报

> **报告周期**：YYYY 年 MM 月
> **生成时间**：YYYY-MM-DD

---

## 📈 月度概览

| 指标 | 数值 |
|------|------|
| Vault 总笔记数 | XXX 篇 |
| 本月新建/修改 | XX 篇 |
| 估计总字数 | ~X 万字 |
| 文件夹数量 | XX 个 |
| 陈旧笔记（>90天未更新） | XX 篇 |

---

## 📚 内容分布

### 各文件夹笔记数量

| 文件夹 | 笔记数 | 占比 |
|--------|--------|------|
| [文件夹 1] | X 篇 | XX% |
| [文件夹 2] | X 篇 | XX% |
| [文件夹 3] | X 篇 | XX% |

---

## 📊 内容健康度

| 指标 | 状态 | 说明 |
|------|------|------|
| 📝 内容产出 | [高/中/低] | 本月 X 篇新内容 |
| 🔄 更新频率 | [活跃/一般/较少] | X% 的笔记近期有更新 |
| 🕳️ 陈旧内容 | [少/中/多] | X% 超过 90 天未更新 |
| 📐 结构清晰度 | [清晰/一般] | 文件夹层级合理程度 |

**健康评分：X/10**

---

## 🗂️ 本月活跃领域

基于本月修改的笔记分布：

- **[领域 1]**：[简要描述本月记录的主要内容]
- **[领域 2]**：[简要描述]

---

## 📌 需要关注

### 陈旧内容（>90天未更新）

| 文件夹 | 陈旧笔记数 | 建议 |
|--------|-----------|------|
| [文件夹] | X 篇 | [如：集中审查更新] |

---

## 💡 建议

### 短期建议（本月可执行）

1. **[建议标题]**：[具体建议，基于实际数据]
2. **[建议标题]**：[具体建议]

### 长期建议（持续改进）

1. **[建议]**：[描述]

---

## 📎 附录

### 数据说明

- 数据来源：本地文件系统（`find` + `stat`）
- 统计周期：YYYY-MM-DD 至 YYYY-MM-DD
- 字数为估算值（基于 `wc -w`）

---

> 📌 本报告基于 Obsidian vault 文件系统数据自动生成。
```

### Step 5: Save to Vault

```bash
obsidian-cli create "Reports/知识管理月报 - $(date +%Y年%m月)" --content "<formatted report>"
```

### Step 6: Confirm

```markdown
✅ 知识月报已生成！

📄 **[[知识管理月报 - YYYY年MM月]]**
📁 已归档到：Reports/

### 本月亮点
- 共 X 篇笔记，本月新建/修改 X 篇
- 最活跃文件夹：[文件夹名]
- 健康评分：X/10
```

## Guidelines

- Be honest about data limitations: word counts are estimates, not precise
- Focus on content health, not individual contributions (no team members in personal vault)
- Suggestions should be specific and actionable based on actual data found
- Default language is Chinese

## Error Handling

| Situation | Action |
|-----------|--------|
| `print-default` fails | Ask user for vault path |
| `find` returns no results | Check vault path; inform user |
| Vault has very few notes (<10) | Generate a brief report; suggest building more content |
| Very large vault (>500 notes) | Sample and extrapolate; note the sampling |
