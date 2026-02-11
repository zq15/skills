#!/bin/bash
# 记录工具调用开始时间

INPUT=$(cat)
TOOL_USE_ID=$(echo "$INPUT" | jq -r '.tool_use_id')
START_TIME=$(date +%s%3N)  # 毫秒时间戳

# 保存开始时间到临时文件
TEMP_DIR="${HOME}/.claude/tool-timing"
mkdir -p "$TEMP_DIR"
echo "$START_TIME" > "${TEMP_DIR}/${TOOL_USE_ID}"

exit 0
