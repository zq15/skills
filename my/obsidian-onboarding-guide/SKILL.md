---
name: obsidian-onboarding-guide
description: "Automatically compile Obsidian vault folders into a structured onboarding reading guide for new project or team members. Use when user says: '帮新人整理入职文档', 'create onboarding guide', '新人入职知识包', '帮我整理一个新人阅读清单'."
metadata:
  { "openclaw": { "emoji": "🎯", "requires": { "bins": ["obsidian-cli"] } } }
---

# Onboarding Guide — New Member Reading Guide Generator

Scan an Obsidian vault, identify core notes, and generate a structured onboarding reading guide organized by week and priority.

## When to Use

- A new member is joining and needs a reading list
- User says "帮新人整理入职文档", "create onboarding guide", "新人入职知识包"
- User wants to create a standard onboarding reading plan from vault content
- User says "帮我整理一个新人阅读清单"

## Required Tools

- `obsidian-cli list [folder]` — List all notes in vault or folders
- `obsidian-cli print "note/path"` — Read specific notes for summary
- `obsidian-cli create "Onboarding Guide" --content "..."` — Save the guide

## Workflow

### Step 1: Identify the Context

Gather from the user:

| Field | Required | Description |
|-------|----------|-------------|
| 新人角色 (Role) | No | e.g., 前端开发、后端开发、产品经理 |
| 特殊关注 (Focus areas) | No | Any specific topics to prioritize |
| Vault 或文件夹 | No | If user wants to focus on a specific area |

If the user doesn't specify a role, generate a general-purpose guide.

### Step 2: Scan the Vault

#### 2a. List All Top-Level Folders

```bash
obsidian-cli list
```

This shows the overall vault structure.

#### 2b. List Notes in Each Major Folder

For each relevant folder:

```bash
obsidian-cli list "FolderName"
```

Collect all note titles and their hierarchy.

### Step 3: Categorize and Prioritize Notes

Classify notes into priority tiers based on title and folder:

**Tier 1 — 第一周必读 (Week 1: Must Read)**

Keywords to look for in titles/paths:
- 入职、新人、指南、规范、流程
- README, Getting Started, Overview, 入门
- 介绍、架构、团队、文化
- 环境搭建、Quick Start, 开发规范
- 提交规范、Review 流程

**Tier 2 — 第二周推荐 (Week 2: Recommended)**

Keywords:
- 架构、设计、技术方案
- 产品、需求
- 部署、发布、运维
- API、接口

**Tier 3 — 第三周扩展 (Week 3: Extended)**

Keywords:
- 历史、决策、技术选型
- 复盘、总结、经验
- 进阶、深入、原理

If the user specified a role, boost documents relevant to that role.

### Step 4: Read Key Notes for Summaries (Optional)

For Tier 1 notes (up to 5), read them to provide brief summaries:

```bash
obsidian-cli print "folder/key-note"
```

Generate a 1-2 sentence summary for each.

### Step 5: Generate the Onboarding Guide

```markdown
# 🎯 新人阅读指南

> **适用角色**：[角色，如"通用" / "前端开发"]
> **生成日期**：YYYY-MM-DD
> **预计阅读周期**：3 周

---

## 📖 使用说明

欢迎！这份阅读指南是根据知识库自动整理的，帮助你快速了解项目/团队的技术栈、工作流程和核心知识。

建议按周计划阅读，遇到问题随时找相关同学。

---

## 📅 第一周：快速上手

> 目标：了解基本情况，搭建环境，熟悉工作流程

### 必读笔记

| # | 笔记 | 文件夹 | 简介 | 预计时间 |
|---|------|--------|------|----------|
| 1 | [[笔记标题]] | [文件夹] | [一句话简介] | ~X 分钟 |
| 2 | [[笔记标题]] | [文件夹] | [一句话简介] | ~X 分钟 |

### ✅ 第一周 Checklist

- [ ] 阅读团队/项目介绍
- [ ] 完成开发环境搭建
- [ ] 了解代码/文档规范

---

## 📅 第二周：深入了解

> 目标：理解系统架构，熟悉核心业务逻辑

### 推荐笔记

| # | 笔记 | 文件夹 | 简介 | 预计时间 |
|---|------|--------|------|----------|
| 1 | [[笔记标题]] | [文件夹] | [一句话简介] | ~X 分钟 |

### ✅ 第二周 Checklist

- [ ] 理解系统整体架构
- [ ] 熟悉核心业务流程

---

## 📅 第三周：扩展阅读

> 目标：了解技术决策背景，建立全局视野

### 扩展笔记

| # | 笔记 | 文件夹 | 简介 |
|---|------|--------|------|
| 1 | [[笔记标题]] | [文件夹] | [一句话简介] |

---

## 🗺️ 知识库导航

| 文件夹 | 描述 | 笔记数 | 重要度 |
|--------|------|--------|--------|
| [[文件夹名]] | [描述] | X 篇 | ⭐⭐⭐ |
| [[文件夹名]] | [描述] | X 篇 | ⭐⭐ |

---

## 💡 Tips

- 🔍 善用 Obsidian 搜索功能，遇到问题先搜一搜
- 📝 阅读过程中发现笔记过时，欢迎直接更新
- 🔗 注意笔记中的 `[[wikilink]]`，顺着链接探索相关内容
- 📚 这份指南是自动生成的，如有遗漏请反馈

---

> 📌 本指南基于 Obsidian vault 自动生成，生成时间：YYYY-MM-DD
```

### Step 6: Save to Vault

```bash
obsidian-cli create "Onboarding Guide" --content "<formatted guide>"
# or with role:
obsidian-cli create "Onboarding/新人阅读指南 - [角色] - YYYY-MM-DD" --content "<formatted guide>"
```

### Step 7: Confirm

```markdown
✅ 入职阅读指南已生成！

📄 **[[新人阅读指南]]**
📁 已保存到：Onboarding/

### 概览
- 扫描了 X 个文件夹，共 X 篇笔记
- 筛选出 X 篇核心笔记
- 按 3 周计划组织阅读路径
```

## Guidelines

- Prioritize breadth over depth — the guide should cover all important folders, not just one
- Estimate reading time: ~5 min for short notes, ~15 min for long ones, ~30 min for complex technical docs
- If a folder has no clear "getting started" note, note it as a gap
- Tailor the checklist items to the specified role
- Use `[[wikilink]]` format — Obsidian users can navigate these natively

## Error Handling

| Situation | Action |
|-----------|--------|
| `list` returns empty vault | Ask user to verify vault path |
| Very few notes (<10) | Create a simpler guide; suggest building more docs |
| Many notes (>100) | Be more selective; focus on top 20-30 most important |
| No notes match the specified role | Fall back to general guide; note role-specific notes are missing |
