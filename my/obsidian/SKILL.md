---
name: obsidian
description: Work with Obsidian vaults (plain Markdown notes) and automate via obsidian-cli.
---

# Obsidian

Obsidian vault = a normal folder on disk.

Vault structure (typical)

- Notes: `*.md` (plain text Markdown; edit with any editor)
- Config: `.obsidian/` (workspace + plugin settings; usually don't touch from scripts)
- Canvases: `*.canvas` (JSON)
- Attachments: whatever folder you chose in Obsidian settings (images/PDFs/etc.)

## Find the active vault(s)

Obsidian desktop tracks vaults here (source of truth):

- `~/Library/Application Support/obsidian/obsidian.json`

`obsidian-cli` resolves vaults from that file; vault name is typically the **folder name** (path suffix).

Fast "what vault is active / where are the notes?"

- If you've already set a default: `obsidian-cli print-default --path-only`
- Otherwise, read `~/Library/Application Support/obsidian/obsidian.json` and use the vault entry with `"open": true`.

Notes

- Multiple vaults common (iCloud vs `~/Documents`, work/personal, etc.). Don't guess; read config.
- Avoid writing hardcoded vault paths into scripts; prefer reading the config or using `print-default`.

## Install obsidian-cli on macOS

```bash
brew install yakitrak/yakitrak/obsidian-cli
```

## Install obsidian-cli on Ubuntu/Linux

`obsidian-cli` has been renamed to `notesmd-cli` and must be built from source (Go required):

```bash
# Install Go if needed
sudo apt install golang-go

# Build and install
git clone https://github.com/yakitrak/notesmd-cli.git
cd notesmd-cli
go build -o obsidian-cli .
sudo install -m 755 obsidian-cli /usr/local/bin/
```

On Linux, vault config is at `~/.config/obsidian/obsidian.json` (not `~/Library/...`).

## obsidian-cli quick start

### Set default vault (once per machine)

`set-default` 接受 **vault 的绝对路径**（不是 vault 名）：

```bash
obsidian-cli set-default "/absolute/path/to/vault"
# 例：obsidian-cli set-default "/Users/foo/ai/obsidian_note"
```

验证：
```bash
obsidian-cli print-default
obsidian-cli print-default --path-only
```

### Search

- `obsidian-cli search "query"` — 按笔记名搜索
- `obsidian-cli search-content "query"` — 按笔记内容搜索（返回片段 + 行号）

### Create — ⚠️ 注意

`obsidian-cli create` **依赖 Obsidian URI 协议**，只有 Obsidian 桌面 App 正在运行时才能实际写入文件。

- **Obsidian 运行中**：`obsidian-cli create "Folder/New note" --content "..." --open`
- **Obsidian 未运行 / 无 GUI 环境**：命令退出码为 0 但文件不会写入磁盘，**改用 Write 工具直接写 `.md` 文件**：

```python
# 直接写文件，Obsidian 下次打开时自动识别
Write(file_path="/absolute/vault/path/Folder/note.md", content="...")
```

Avoid creating notes under hidden dot-folders (e.g. `.something/...`); Obsidian may refuse.

### Move / rename (safe refactor)

- `obsidian-cli move "old/path/note" "new/path/note"`
- 自动更新 vault 内所有 `[[wikilinks]]` 和 Markdown 链接（这是相比 `mv` 的核心优势）

### Delete

- `obsidian-cli delete "path/note"`

Prefer direct edits when appropriate: open the `.md` file and change it; Obsidian will pick it up.
