#!/bin/bash
# 记录工具调用结果和耗时

INPUT=$(cat)

# 提取字段
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
TOOL_USE_ID=$(echo "$INPUT" | jq -r '.tool_use_id')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id')
TOOL_INPUT=$(echo "$INPUT" | jq -c '.tool_input')
TOOL_RESPONSE=$(echo "$INPUT" | jq -c '.tool_response')

# 计算耗时
TEMP_DIR="${HOME}/.claude/tool-timing"
START_TIME_FILE="${TEMP_DIR}/${TOOL_USE_ID}"
END_TIME=$(date +%s%3N)
DURATION_MS="null"

if [ -f "$START_TIME_FILE" ]; then
    START_TIME=$(cat "$START_TIME_FILE")
    DURATION_MS=$((END_TIME - START_TIME))
    rm -f "$START_TIME_FILE"
fi

# 时间戳
TIMESTAMP=$(date -u +'%Y-%m-%dT%H:%M:%SZ')

# 日志文件
LOG_FILE="${HOME}/.claude/tool_calls.log"

# 创建日志条目（限制输出长度）
LOG_ENTRY=$(jq -cn \
  --arg timestamp "$TIMESTAMP" \
  --arg session_id "$SESSION_ID" \
  --arg tool_name "$TOOL_NAME" \
  --arg tool_use_id "$TOOL_USE_ID" \
  --argjson duration_ms "$DURATION_MS" \
  --argjson tool_input "$TOOL_INPUT" \
  --argjson tool_response "$TOOL_RESPONSE" \
  '{
    timestamp: $timestamp,
    session_id: $session_id,
    tool_name: $tool_name,
    tool_use_id: $tool_use_id,
    duration_ms: $duration_ms,
    input: $tool_input,
    response: $tool_response
  }')

# 追加到日志文件
echo "$LOG_ENTRY" >> "$LOG_FILE"

exit 0
