---
name: obsidian-tech-design
description: "Generate technical design documents using a standard template and save them to your Obsidian vault. Use when user says: '帮我写技术方案', 'write a tech design', '技术设计文档', 'RFC', '帮我写个架构设计'."
metadata:
  { "openclaw": { "emoji": "⚙️", "requires": { "bins": ["obsidian-cli"] } } }
---

# Tech Design — Technical Design Document Generator

Help the user write a structured technical design document following a standard template, then save it to the Obsidian vault.

## When to Use

- User wants to write a technical design document or RFC
- User says "帮我写技术方案", "write a tech design", "技术设计文档", "RFC"
- User describes a feature/system and needs it formalized into a design doc

## Required Tools

- `obsidian-cli search-content "<keywords>"` — Search for related existing notes for context
- `obsidian-cli print "note/path"` — Read related notes
- `obsidian-cli create "Tech Design/[title]" --content "..."` — Save the design doc

## Reference

The full template is in [references/template.md](./references/template.md). Load it when generating the document.

## Workflow

### Step 1: Understand the Requirements

Gather from the user:

| Field | Required | Description |
|-------|----------|-------------|
| 项目/功能名称 | Yes | What is being designed |
| 背景与问题 | Yes | Why this is needed, what problem it solves |
| 目标 | Yes | What success looks like |
| 约束条件 | No | Technical constraints, timeline, budget |
| 已有方案 | No | Any existing approaches or prior art |

If the user provides a brief description, ask clarifying questions:
- "这个功能要解决什么问题？"
- "有什么技术约束吗？比如必须用某个框架、要兼容现有系统？"

### Step 2: Search for Context (Optional)

If relevant, search the vault for related existing notes:

```bash
obsidian-cli search-content "<related keywords>"
```

This helps:
- Avoid duplicating existing designs
- Reference prior decisions
- Understand the current architecture

Read relevant results:

```bash
obsidian-cli print "folder/related-note"
```

### Step 3: Generate the Design Document

Load the template from `references/template.md` and fill in each section based on the user's input.

Key sections:

1. **背景 (Background)** — Problem statement, current situation
2. **目标 (Goals)** — What this design achieves, non-goals
3. **方案设计 (Design)** — Core technical approach
   - Architecture description (ASCII diagram if helpful)
   - Core components and responsibilities
   - Data model / API design
   - Key flows
4. **技术选型 (Tech Stack)** — Why specific technologies were chosen
5. **方案对比 (Alternatives)** — Other approaches considered and why rejected
6. **排期 (Timeline)** — Milestones and estimated effort
7. **风险评估 (Risks)** — What could go wrong and mitigation strategies
8. **参考资料 (References)** — Related notes, links, prior art

### Step 4: Review with User

Present the draft to the user before saving:
- "方案内容是否准确？有需要调整的地方吗？"
- "要补充其他技术细节吗？"

### Step 5: Save to Vault

```bash
obsidian-cli create "Tech Design/[技术方案] [项目名称]" --content "<formatted design doc>"
```

### Step 6: Confirm

```markdown
✅ 技术方案已创建（草稿状态）！

📄 **[[[技术方案] 项目名称]]]**
📁 已保存到：Tech Design/

### 文档结构
- 背景与目标
- 方案设计（含 X 个核心模块）
- 技术选型对比
- 排期（预计 X 周）
- 风险评估（X 个风险点）

💡 文档为草稿状态，请评审后确认。
```

## Guidelines

- Write the design doc in Chinese (default) unless the user specifies English
- Be specific in the design section — include data models, API signatures, flow descriptions
- For tech stack comparison, use a table with pros/cons
- Keep the document actionable — someone should be able to implement from this doc
- If the user's requirements are vague, make reasonable assumptions and note them clearly with "【假设】" markers
- Don't over-engineer — match the design complexity to the project scope

## Error Handling

| Situation | Action |
|-----------|--------|
| User provides very vague requirements | Ask 2-3 targeted questions before generating |
| `search-content` finds conflicting existing designs | Mention them and ask user how to reconcile |
| `create` fails | Show error; offer to output the markdown for manual copy |
| User wants to update an existing design doc | Find it with `search-content`, then suggest creating a v2 |
