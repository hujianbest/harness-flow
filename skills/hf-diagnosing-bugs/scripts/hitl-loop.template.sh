#!/usr/bin/env bash
# 人在回路中的复现循环。
# 复制此文件，编辑下方步骤，然后运行。
# Agent 运行脚本；用户在自己的终端中按照提示操作。
#
# 用法：
#   bash hitl-loop.template.sh
#
# 两个辅助函数：
#   step "<指令>"                 → 显示指令，等待按下 Enter
#   capture VAR "<问题>"          → 显示问题，将回答读入 VAR
#
# 最后，捕获的值会以 KEY=VALUE 格式打印，供 Agent 解析。
#
# `capture` 会将值打印回终端，Agent 将从中读取——因此只捕获观察结果，
# 登录操作则应作为 `step` 留给用户完成。

set -euo pipefail

step() {
  printf '\n>>> %s\n' "$1"
  read -r -p "    [完成后按 Enter] " _
}

capture() {
  local var="$1" question="$2" answer
  printf '\n>>> %s\n' "$question"
  read -r -p "    > " answer
  printf -v "$var" '%s' "$answer"
}

# --- 在下方编辑 ---------------------------------------------------------

step "打开 http://localhost:3000 上的应用并登录。"

capture ERRORED "点击“导出”按钮。是否抛出错误？(y/n)"

capture ERROR_MSG "粘贴错误消息（如果没有，请输入“无”）："

# --- 在上方编辑 ---------------------------------------------------------

printf '\n--- 已捕获 ---\n'
printf 'ERRORED=%s\n' "$ERRORED"
printf 'ERROR_MSG=%s\n' "$ERROR_MSG"
