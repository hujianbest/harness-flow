#!/usr/bin/env bash
#
# 向导——逐步引导人工完成手动流程。
# 由 /wizard 技能生成。
#
# “STAGES”标记上方的所有内容都是向导库：不要手动编辑。
# 请在标记下方编写每个步骤的阶段。

set -euo pipefail

# ──────────────────────────────────────────────────────────────────────────
# 向导库——令人愉悦且一致的用户体验。所有向导中均完全相同。
# ──────────────────────────────────────────────────────────────────────────

if [[ -t 1 ]] && command -v tput >/dev/null 2>&1 && [[ "$(tput colors 2>/dev/null || echo 0)" -ge 8 ]]; then
  BOLD=$(tput bold); DIM=$(tput dim); RESET=$(tput sgr0)
  BLUE=$(tput setaf 4); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); RED=$(tput setaf 1)
else
  BOLD=""; DIM=""; RESET=""; BLUE=""; GREEN=""; YELLOW=""; RED=""
fi

# 作者在阶段部分顶部设置此值。
TOTAL_STAGES=0

_STAGE_INDEX=0
ENV_FILE="${ENV_FILE:-.env}"
WRITTEN_ENV=()    # 本次运行写入 ENV_FILE 的 KEY
WRITTEN_SECRET=() # 本次运行设置的密钥 NAME
SKIPPED=()        # 无法完成的事项（例如缺少 gh）

# _clear——清空终端，使屏幕上只显示当前步骤。输出不是终端时不执行任何操作，
# 从而保持管道日志可读。
_clear() {
  [[ -t 1 ]] || return 0
  if command -v tput >/dev/null 2>&1; then tput clear; else printf '\033[2J\033[3J\033[H'; fi
}

# banner "标题"——开场画面：此向导的用途。
banner() {
  _clear
  printf '\n%s%s  %s%s\n' "$BOLD" "$BLUE" "$1" "$RESET"
  printf '%s  共 %s 个阶段%s\n\n' "$DIM" "$TOTAL_STAGES" "$RESET"
  printf '%s  你操作浏览器；此向导会准确告诉你该做什么，\n' "$DIM"
  printf '  并捕获你复制回来的值。可随时按 Ctrl-C 停止并在以后重新运行——\n'
  printf '  它会记住已保存的值。%s\n' "$RESET"
  pause "准备开始了吗？"
}

# stage "名称"——清屏，然后宣布阶段并显示进度。
# 清屏后屏幕上只保留当前步骤。
stage() {
  _clear
  _STAGE_INDEX=$((_STAGE_INDEX + 1))
  printf '\n%s%s▸ 阶段 %s/%s · %s%s\n' \
    "$BOLD" "$BLUE" "$_STAGE_INDEX" "$TOTAL_STAGES" "$1" "$RESET"
}

# say "..."——普通说明行。
say()  { printf '  %s\n' "$1"; }
# step "..."——人工在浏览器中执行的、具有步骤感的操作。
step() { printf '  %s•%s %s\n' "$BLUE" "$RESET" "$1"; }
note() { printf '  %s%s%s\n' "$DIM" "$1" "$RESET"; }
warn() { printf '  %s⚠ %s%s\n' "$YELLOW" "$1" "$RESET"; }

# open_url URL——在人工的浏览器中打开，跨平台支持（包括 WSL）。
open_url() {
  local url="$1"
  printf '  %s↗ 正在打开%s %s\n' "$GREEN" "$RESET" "$url"
  { if   command -v wslview     >/dev/null 2>&1; then wslview "$url"
    elif command -v explorer.exe >/dev/null 2>&1; then explorer.exe "$url"
    elif command -v xdg-open    >/dev/null 2>&1; then xdg-open "$url"
    elif command -v open        >/dev/null 2>&1; then open "$url"
    else warn "无法打开浏览器——请手动访问：$url"; fi
  } >/dev/null 2>&1 || warn "无法打开浏览器——请手动访问：$url"
}

# pause "消息"——等待人工确认已完成手动部分。
pause() {
  printf '  %s%s%s ' "$DIM" "${1:-按 Enter 继续}" "$RESET"
  read -r _ || true
}

# confirm "问题"——y/N 门禁；回答 yes 时返回成功。
confirm() {
  local reply=""
  printf '  %s? %s [y/N] ' "$YELLOW" "$1"
  read -r reply || true
  [[ "$reply" =~ ^[Yy] ]]
}

# _existing KEY——ENV_FILE 中 KEY 的当前值（如果有）。
_existing() {
  [[ -f "$ENV_FILE" ]] || return 1
  local line; line=$(grep -E "^${1}=" "$ENV_FILE" | tail -n1) || return 1
  printf '%s' "${line#*=}"
}

# ask KEY "提示"——将值读入 $KEY。重新运行时，将现有 .env 值作为
# 默认值（按 Enter 保留）。输入可见（非密钥）。
ask() {
  local key="$1" prompt="$2" current input
  current=$(_existing "$key" || true)
  if [[ -n "$current" ]]; then
    printf '  %s%s%s %s[按 Enter 保留当前值]%s ' "$BOLD" "$prompt" "$RESET" "$DIM" "$RESET"
  else
    printf '  %s%s%s ' "$BOLD" "$prompt" "$RESET"
  fi
  read -r input || true
  [[ -z "$input" && -n "$current" ]] && input="$current"
  printf -v "$key" '%s' "$input"
}

# ask_secret KEY "提示"——与 ask 类似，但隐藏输入。
ask_secret() {
  local key="$1" prompt="$2" current input
  current=$(_existing "$key" || true)
  if [[ -n "$current" ]]; then
    printf '  %s%s%s %s[按 Enter 保留当前值]%s ' "$BOLD" "$prompt" "$RESET" "$DIM" "$RESET"
  else
    printf '  %s%s%s ' "$BOLD" "$prompt" "$RESET"
  fi
  read -rs input || true
  printf '\n'
  [[ -z "$input" && -n "$current" ]] && input="$current"
  printf -v "$key" '%s' "$input"
}

# write_env KEY VALUE——将 KEY=VALUE 更新插入 ENV_FILE（创建文件；
# 替换任何现有行）。幂等。
write_env() {
  local key="$1" value="$2" tmp
  touch "$ENV_FILE"
  tmp=$(mktemp)
  grep -vE "^${key}=" "$ENV_FILE" > "$tmp" || true
  printf '%s=%s\n' "$key" "$value" >> "$tmp"
  mv "$tmp" "$ENV_FILE"
  WRITTEN_ENV+=("$key")
  printf '  %s✓ 已写入%s %s → %s\n' "$GREEN" "$RESET" "$key" "$ENV_FILE"
}

# set_secret NAME VALUE——通过 gh 设置 GitHub Actions 仓库密钥。如果 gh
# 不可用或未认证，则回退为警告（并记录）。
set_secret() {
  local name="$1" value="$2"
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if printf '%s' "$value" | gh secret set "$name" >/dev/null 2>&1; then
      WRITTEN_SECRET+=("$name")
      printf '  %s✓ 已设置%s GitHub 密钥 %s\n' "$GREEN" "$RESET" "$name"
      return
    fi
  fi
  SKIPPED+=("GitHub 密钥 $name（请手动设置：gh secret set $name）")
  warn "已跳过 GitHub 密钥 $name——gh 尚未就绪；请稍后设置"
}

# set_var NAME VALUE——设置 GitHub Actions 仓库变量（非密钥）。
set_var() {
  local name="$1" value="$2"
  if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    if gh variable set "$name" --body "$value" >/dev/null 2>&1; then
      printf '  %s✓ 已设置%s GitHub 变量 %s\n' "$GREEN" "$RESET" "$name"
      return
    fi
  fi
  SKIPPED+=("GitHub 变量 $name")
  warn "已跳过 GitHub 变量 $name——gh 尚未就绪；请稍后设置"
}

# finish——清屏，然后显示所有已配置内容的结束摘要。
finish() {
  _clear
  printf '\n%s%s  ✓ 设置完成%s\n' "$BOLD" "$GREEN" "$RESET"
  (( ${#WRITTEN_ENV[@]} ))    && note "已向 $ENV_FILE 写入 ${#WRITTEN_ENV[@]} 个值：${WRITTEN_ENV[*]}"
  (( ${#WRITTEN_SECRET[@]} )) && note "已设置 ${#WRITTEN_SECRET[@]} 个 GitHub 密钥：${WRITTEN_SECRET[*]}"
  if (( ${#SKIPPED[@]} )); then
    printf '\n'; warn "仍需手动完成："
    for s in "${SKIPPED[@]}"; do note "  - $s"; done
  fi
  printf '\n'
}

# ──────────────────────────────────────────────────────────────────────────
# STAGES——编写此部分。人工执行的每个步骤对应一个 stage()。
# 替换下方示例。设置 TOTAL_STAGES，使其与所编写的阶段数一致。
# ──────────────────────────────────────────────────────────────────────────

TOTAL_STAGES=1

banner "Stripe 设置"

# ── 示例阶段：请替换为实际步骤 ────────────────────────────────────────────
stage "Stripe——API 密钥"
say "我们将获取你的 Stripe 测试密钥，并保存供本地开发和 CI 使用。"
open_url "https://dashboard.stripe.com/test/apikeys"
step "在 API 密钥页面，复制可发布密钥（以 pk_test_ 开头）。"
ask STRIPE_PUBLISHABLE_KEY "粘贴可发布密钥："
step "在密钥行点击“显示测试密钥”，然后复制。"
ask_secret STRIPE_SECRET_KEY "粘贴密钥："
write_env STRIPE_PUBLISHABLE_KEY "$STRIPE_PUBLISHABLE_KEY"
write_env STRIPE_SECRET_KEY "$STRIPE_SECRET_KEY"
set_secret STRIPE_SECRET_KEY "$STRIPE_SECRET_KEY"   # CI 需要此项
# ──────────────────────────────────────────────────────────────────────────

finish
