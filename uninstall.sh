#!/usr/bin/env bash
# uninstall.sh — Reverse a HarnessFlow vendor install based on the manifest
# written by install.sh.
#
# Reads host/.harnessflow-install-manifest.json and removes each entry.
# Parent directories (`PARENT_DIRS`) use rmdir-only so user-added skills
# survive (FR-004 acceptance #1 / HYP-002 Blocking validation).
#
# Design reference: features/001-install-scripts/design.md §10 (apply_removal
# parent vs leaf), §13 (manifest schema)
# ADR reference: docs/decisions/ADR-007-install-scripts-topology-and-manifest.md D2

set -Eeuo pipefail
IFS=$'\n\t'

PROG="uninstall.sh"

# Parent dirs that should be removed only when empty (so host's user-added
# content survives). Other dir entries get rm -rf.
PARENT_DIRS=(
    ".opencode/skills"
    ".cursor/harness-flow-skills"
    ".cursor/rules"
)

usage() {
    cat <<EOF
Usage: $PROG [--host <path>] [--dry-run] [-h|--help]

Defaults:
  --host .  (current working directory)

Reads <host>/.harnessflow-install-manifest.json and removes each entry. Parent
directories under .opencode/ or .cursor/ are removed only when empty (so host
content other than HF vendor stays intact). Manifest and post-install README
are removed last.

Exit codes:
  0  success
  1  invalid args / no manifest found / partial removal failure

Windows:
  This is a bash 3.2+ script. On Windows run it via Git Bash (bundled with
  Git for Windows: https://git-scm.com/download/win), WSL, or MSYS2 — not
  PowerShell or cmd. A PowerShell wrapper (uninstall.ps1) is also provided
  that locates bash and forwards arguments.
EOF
}

HOST_RAW="."
DRY_RUN=0

log() { printf '[hf-uninstall] %s\n' "$*"; }
err() { printf '[hf-uninstall][ERROR] %s\n' "$*" >&2; }

is_parent_dir() {
    local rel="$1"
    local p
    for p in "${PARENT_DIRS[@]}"; do
        if [ "$rel" = "$p" ]; then
            return 0
        fi
    done
    return 1
}

require_value() {
    if [ $# -lt 2 ] || [ -z "${2:-}" ] || [[ "${2:-}" == --* ]]; then
        err "$1 requires a value"
        usage >&2
        exit 1
    fi
}

parse_args() {
    while [ $# -gt 0 ]; do
        case "$1" in
            --host)     require_value "$1" "${2:-}"; HOST_RAW="$2"; shift 2 ;;
            --host=*)   HOST_RAW="${1#*=}"; shift ;;
            --dry-run)  DRY_RUN=1; shift ;;
            -h|--help)  usage; exit 0 ;;
            *)
                err "unknown arg: $1"
                usage >&2
                exit 1
                ;;
        esac
    done
}

main() {
    parse_args "$@"

    if [ ! -d "$HOST_RAW" ]; then
        err "--host path does not exist or is not a directory: $HOST_RAW"
        exit 1
    fi
    HOST="$(cd "$HOST_RAW" && pwd)"
    local manifest="$HOST/.harnessflow-install-manifest.json"

    if [ ! -f "$manifest" ]; then
        err "no manifest found at $manifest; nothing to uninstall"
        exit 1
    fi

    log "reading manifest: $manifest"

    # Extract entries[] without jq. Entries look like:
    #   {"kind": "dir", "path": ".opencode/skills/hf-finalize"}
    # We pull out kind/path pairs in order.
    local entries=()
    local line kind path
    while IFS= read -r line; do
        kind=$(printf '%s' "$line" | sed -nE 's/.*"kind"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/p')
        path=$(printf '%s' "$line" | sed -nE 's/.*"path"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/p')
        if [ -n "$kind" ] && [ -n "$path" ]; then
            entries+=("$kind:$path")
        fi
    done < <(grep -E '"kind"[[:space:]]*:' "$manifest")

    if [ "${#entries[@]}" = 0 ]; then
        err "manifest contains no entries; nothing to remove (manifest format error?)"
        exit 1
    fi

    log "removing ${#entries[@]} entries (target host: $HOST)"

    # Reverse-iterate so leaf entries go first (they were added last).
    local i e e_kind e_rel abs
    local rc=0
    for ((i=${#entries[@]}-1; i>=0; i--)); do
        e="${entries[$i]}"
        e_kind="${e%%:*}"
        e_rel="${e#*:}"
        abs="$HOST/$e_rel"
        case "$e_kind" in
            symlink|file)
                if [ "$DRY_RUN" = 1 ]; then
                    printf '[RM] %s\n' "$abs"
                else
                    rm -f "$abs" 2>/dev/null || rc=2
                fi
                ;;
            dir)
                if is_parent_dir "$e_rel"; then
                    if [ "$DRY_RUN" = 1 ]; then
                        printf '[RMDIR] %s (only-if-empty)\n' "$abs"
                    else
                        rmdir "$abs" 2>/dev/null || true
                    fi
                else
                    if [ "$DRY_RUN" = 1 ]; then
                        printf '[RM -rf] %s\n' "$abs"
                    else
                        rm -rf "$abs" 2>/dev/null || rc=2
                    fi
                fi
                ;;
            *)
                err "unknown manifest entry kind: $e_kind (path=$e_rel); skipping"
                ;;
        esac
    done

    # Manifest itself + readme are not in entries[] (manifest avoids self-reference;
    # readme is in entries[] so it was already handled above). Manifest is removed
    # explicitly at the end so its own deletion isn't required to be self-listed.
    if [ "$DRY_RUN" = 1 ]; then
        printf '[RM] %s\n' "$manifest"
    else
        rm -f "$manifest" 2>/dev/null || rc=2
    fi

    # Best-effort: remove parent .opencode / .cursor if empty.
    for d in "$HOST/.opencode" "$HOST/.cursor"; do
        if [ -d "$d" ]; then
            if [ "$DRY_RUN" = 1 ]; then
                printf '[RMDIR] %s (only-if-empty)\n' "$d"
            else
                rmdir "$d" 2>/dev/null || true
            fi
        fi
    done

    if [ "$DRY_RUN" = 1 ]; then
        log "dry-run complete (no files removed)"
    elif [ "$rc" -ne 0 ]; then
        err "uninstall completed with partial failure (exit $rc); some files may remain"
        exit "$rc"
    else
        log "uninstall complete"
    fi
}

main "$@"
