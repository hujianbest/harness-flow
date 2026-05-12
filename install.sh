#!/usr/bin/env bash
# install.sh — Install HarnessFlow into a host repository for Cursor / OpenCode.
#
# Vendors the HF skills tree (and Cursor rule, when applicable) into a host
# repository and writes a manifest so the install can be cleanly reversed via
# uninstall.sh.
#
# Design reference: features/001-install-scripts/design.md
# ADR reference: docs/decisions/ADR-007-install-scripts-topology-and-manifest.md
# Spec reference: features/001-install-scripts/spec.md
#
# Constraints:
#   - bash 3.2+ compatible (no mapfile / no associative arrays / no ${var,,})
#   - POSIX coreutils only (no jq / no python / no node / no npm)
#   - set -Eeuo pipefail (set -E required so ERR trap propagates from functions)

set -Eeuo pipefail
IFS=$'\n\t'

PROG="install.sh"

usage() {
    cat <<EOF
Usage: $PROG --target {cursor|opencode|both}
             [--topology {copy|symlink}]
             [--host <path>]
             [--dry-run]
             [--verbose]
             [--force]

Defaults:
  --topology copy
  --host    .  (current working directory)

Vendors HarnessFlow into a host repository:
  --target opencode → host/.opencode/skills/
  --target cursor   → host/.cursor/harness-flow-skills/ + host/.cursor/rules/harness-flow.mdc
  --target both     → both of the above

Topology:
  copy    → cp -R the skills tree (per-skill manifest entries)
  symlink → ln -s the skills tree (single symlink manifest entry)

Manifest is written to host/.harnessflow-install-manifest.json.
A README is written to host/.harnessflow-install-readme.md.

Use uninstall.sh to reverse based on the manifest.
EOF
}

# Resolve canonical absolute path of script (handle symlinked invocations like ECC's wrapper).
resolve_self_dir() {
    local src="${BASH_SOURCE[0]}"
    while [ -L "$src" ]; do
        local d
        d="$(cd -P "$(dirname "$src")" && pwd)"
        src="$(readlink "$src")"
        case "$src" in
            /*) ;;
            *)  src="$d/$src" ;;
        esac
    done
    cd -P "$(dirname "$src")" && pwd
}

HF_REPO="$(resolve_self_dir)"
TARGET=""
TOPOLOGY="copy"
HOST_RAW="."
DRY_RUN=0
VERBOSE=0
FORCE=0

ENTRIES=()
INSTALLED=()

# log() always prints (FR-007: default banner is non-verbose).
log() {
    printf '[hf-install] %s\n' "$*"
}

# err() always prints to stderr.
err() {
    printf '[hf-install][ERROR] %s\n' "$*" >&2
}

# op() applies a single filesystem operation. In dry-run or verbose mode it
# also prints the planned/applied action.
op() {
    local action="$1"; shift
    if [ "$VERBOSE" = 1 ] || [ "$DRY_RUN" = 1 ]; then
        printf '[%s] %s\n' "$action" "$*"
    fi
    if [ "$DRY_RUN" = 1 ]; then
        return 0
    fi
    case "$action" in
        MKDIR) mkdir -p "$@" ;;
        CP)    cp -R "$1" "$2" ;;
        LN)    ln -s "$1" "$2" ;;
        RM)    rm -rf "$1" ;;
        *)
            err "unknown op: $action"
            return 1
            ;;
    esac
}

# Pre-register an "I am about to create this" intent so rollback can clean it
# up even if the actual op fails partway. Pre-existing dirs are intentionally
# skipped: we won't delete dirs we did not create (so host's own .cursor/
# stays intact at uninstall time).
mark_will_create() {
    local kind="$1" abs="$2" rel="${3:-}"
    if [ "$kind" = "dir" ] && [ -d "$abs" ]; then
        return 0
    fi
    INSTALLED+=("$kind:$abs")
    if [ -n "$rel" ]; then
        ENTRIES+=("$kind:$rel")
    fi
}

rollback() {
    local rc=$?
    err "install failed (exit $rc); rolling back..."
    local i
    for ((i=${#INSTALLED[@]}-1; i>=0; i--)); do
        local entry="${INSTALLED[$i]}"
        local kind="${entry%%:*}"
        local path="${entry#*:}"
        case "$kind" in
            symlink|file) rm -f "$path" 2>/dev/null || true ;;
            dir)          rm -rf "$path" 2>/dev/null || true ;;
        esac
    done
    rm -f "$HOST/.harnessflow-install-manifest.json" 2>/dev/null || true
    rm -f "$HOST/.harnessflow-install-readme.md" 2>/dev/null || true
    exit "$rc"
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
            --target)    require_value "$1" "${2:-}"; TARGET="$2"; shift 2 ;;
            --target=*)  TARGET="${1#*=}"; shift ;;
            --topology)  require_value "$1" "${2:-}"; TOPOLOGY="$2"; shift 2 ;;
            --topology=*) TOPOLOGY="${1#*=}"; shift ;;
            --host)      require_value "$1" "${2:-}"; HOST_RAW="$2"; shift 2 ;;
            --host=*)    HOST_RAW="${1#*=}"; shift ;;
            --dry-run)   DRY_RUN=1; shift ;;
            --verbose)   VERBOSE=1; shift ;;
            --force)     FORCE=1; shift ;;
            -h|--help)   usage; exit 0 ;;
            *)
                err "unknown arg: $1"
                usage >&2
                exit 1
                ;;
        esac
    done
}

validate_args() {
    case "$TARGET" in
        cursor|opencode|both) ;;
        "")
            err "--target is required"
            usage >&2
            exit 1
            ;;
        *)
            err "invalid --target: $TARGET (expected cursor|opencode|both)"
            exit 1
            ;;
    esac
    case "$TOPOLOGY" in
        copy|symlink) ;;
        *)
            err "invalid --topology: $TOPOLOGY (expected copy|symlink)"
            exit 1
            ;;
    esac
    if [ ! -d "$HOST_RAW" ]; then
        err "--host path does not exist or is not a directory: $HOST_RAW"
        exit 1
    fi
    HOST="$(cd "$HOST_RAW" && pwd)"
    if [ "$HOST" = "$HF_REPO" ]; then
        err "--host must not be the HarnessFlow repository itself (would self-vendor)"
        exit 1
    fi
}

detect_existing_manifest() {
    local manifest="$HOST/.harnessflow-install-manifest.json"
    if [ -f "$manifest" ]; then
        if [ "$FORCE" = 1 ]; then
            if [ "$DRY_RUN" = 1 ]; then
                # FR-005 strict reading: dry-run must not actually mutate the host.
                # In --force --dry-run mode we describe what we would do but skip
                # the real uninstall invocation.
                log "[dry-run] would invoke uninstall.sh --host $HOST before re-install (--force)"
                return 0
            fi
            log "existing manifest found; --force given, removing previous install before re-install"
            local uninstall="$HF_REPO/uninstall.sh"
            if [ -x "$uninstall" ]; then
                bash "$uninstall" --host "$HOST" || {
                    err "previous uninstall failed; aborting"
                    exit 1
                }
            else
                err "uninstall.sh not found at $uninstall; cannot --force"
                exit 1
            fi
        else
            err "existing manifest found at $manifest; pass --force to overwrite"
            exit 1
        fi
    fi
}

detect_hf_version() {
    HF_COMMIT="unknown-non-git-checkout"
    if command -v git >/dev/null 2>&1 && [ -d "$HF_REPO/.git" ]; then
        local sha
        sha=$(cd "$HF_REPO" && git rev-parse HEAD 2>/dev/null || true)
        if [ -n "$sha" ]; then
            HF_COMMIT="$sha"
        fi
    fi
    HF_VERSION="unknown"
    if [ -f "$HF_REPO/CHANGELOG.md" ]; then
        local ver
        ver=$(grep -E '^## \[[0-9]+\.[0-9]+\.[0-9]+' "$HF_REPO/CHANGELOG.md" \
              | head -n1 \
              | sed -E 's/^## \[([^]]+)\].*/\1/' || true)
        if [ -n "$ver" ]; then
            HF_VERSION="$ver"
        fi
    fi
}

vendor_skills_opencode() {
    local skills_root_abs="$HOST/.opencode/skills"
    local skills_root_rel=".opencode/skills"
    mark_will_create dir "$HOST/.opencode" ""
    op MKDIR "$HOST/.opencode"
    if [ "$TOPOLOGY" = "symlink" ]; then
        mark_will_create symlink "$skills_root_abs" "$skills_root_rel"
        op LN "$HF_REPO/skills" "$skills_root_abs"
    else
        mark_will_create dir "$skills_root_abs" "$skills_root_rel"
        op MKDIR "$skills_root_abs"
        local skill_path name
        # Use glob (not `for x in $(ls)`) to handle names with spaces/newlines safely.
        for skill_path in "$HF_REPO/skills"/*; do
            [ -d "$skill_path" ] || continue
            name="${skill_path##*/}"
            local skill_abs="$skills_root_abs/$name"
            local skill_rel="$skills_root_rel/$name"
            mark_will_create dir "$skill_abs" "$skill_rel"
            op CP "$skill_path" "$skill_abs"
        done
    fi
}

vendor_cursor() {
    mark_will_create dir "$HOST/.cursor" ""
    op MKDIR "$HOST/.cursor"
    # .cursor/rules is registered as a parent_dir entry in the manifest so
    # uninstall can rmdir-only it (preserving any user-added rules under it).
    mark_will_create dir "$HOST/.cursor/rules" ".cursor/rules"
    op MKDIR "$HOST/.cursor/rules"

    local skills_abs="$HOST/.cursor/harness-flow-skills"
    local skills_rel=".cursor/harness-flow-skills"
    local rule_abs="$HOST/.cursor/rules/harness-flow.mdc"
    local rule_rel=".cursor/rules/harness-flow.mdc"

    if [ "$TOPOLOGY" = "symlink" ]; then
        mark_will_create symlink "$skills_abs" "$skills_rel"
        op LN "$HF_REPO/skills" "$skills_abs"
        mark_will_create symlink "$rule_abs" "$rule_rel"
        op LN "$HF_REPO/.cursor/rules/harness-flow.mdc" "$rule_abs"
    else
        mark_will_create dir "$skills_abs" "$skills_rel"
        op MKDIR "$skills_abs"
        local skill_path name
        for skill_path in "$HF_REPO/skills"/*; do
            [ -d "$skill_path" ] || continue
            name="${skill_path##*/}"
            local skill_abs="$skills_abs/$name"
            local skill_rel="$skills_rel/$name"
            mark_will_create dir "$skill_abs" "$skill_rel"
            op CP "$skill_path" "$skill_abs"
        done
        mark_will_create file "$rule_abs" "$rule_rel"
        op CP "$HF_REPO/.cursor/rules/harness-flow.mdc" "$rule_abs"
    fi
}

write_manifest() {
    local manifest="$HOST/.harnessflow-install-manifest.json"
    local now
    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    if [ "$DRY_RUN" = 1 ]; then
        printf '[WRITE] %s (manifest_version=1, %d entries)\n' "$manifest" "${#ENTRIES[@]}"
        return 0
    fi

    {
        printf '{\n'
        printf '  "manifest_version": 1,\n'
        printf '  "installed_at": "%s",\n' "$now"
        printf '  "hf_commit": "%s",\n' "$HF_COMMIT"
        printf '  "hf_version": "%s",\n' "$HF_VERSION"
        printf '  "target": "%s",\n' "$TARGET"
        printf '  "topology": "%s",\n' "$TOPOLOGY"
        printf '  "entries": [\n'
        local i n="${#ENTRIES[@]}"
        for ((i=0; i<n; i++)); do
            local entry="${ENTRIES[$i]}"
            local kind="${entry%%:*}"
            local path="${entry#*:}"
            local sep=","
            if [ "$i" = "$((n-1))" ]; then sep=""; fi
            printf '    {"kind": "%s", "path": "%s"}%s\n' "$kind" "$path" "$sep"
        done
        printf '  ]\n'
        printf '}\n'
    } > "$manifest"
}

write_readme() {
    local readme="$HOST/.harnessflow-install-readme.md"
    local readme_rel=".harnessflow-install-readme.md"
    local now
    now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    mark_will_create file "$readme" "$readme_rel"

    if [ "$DRY_RUN" = 1 ]; then
        printf '[WRITE] %s (post-install README)\n' "$readme"
        return 0
    fi

    cat > "$readme" <<EOF
# HarnessFlow installed (vendor mode)

- Installed at: $now
- HF version: $HF_VERSION
- HF commit: $HF_COMMIT
- Target: $TARGET
- Topology: $TOPOLOGY

## Quick verify

\`\`\`bash
# 1. count vendored skills (expected ≥ 24)
find .opencode/skills -mindepth 2 -maxdepth 2 -name SKILL.md 2>/dev/null | wc -l

# 2. inspect install manifest
cat .harnessflow-install-manifest.json

# 3. (symlink topology only) check symlink target
readlink .opencode/skills 2>/dev/null || true

# 4. (cursor target only) check rule placement
ls -la .cursor/rules/harness-flow.mdc 2>/dev/null || true
\`\`\`

## Uninstall

\`\`\`bash
bash <hf-repo>/uninstall.sh --host .
\`\`\`

## Cursor rule note (cursor / both target)

\`.cursor/rules/harness-flow.mdc\` references \`skills/using-hf-workflow/SKILL.md\` relatively;
after vendor, the correct path is \`.cursor/harness-flow-skills/using-hf-workflow/SKILL.md\`.
(v0.6+ may rewrite paths automatically at install time — see ADR-007 D4 alternative A3.)
EOF
}

main() {
    parse_args "$@"
    validate_args
    detect_existing_manifest
    detect_hf_version

    log "starting install: target=$TARGET topology=$TOPOLOGY host=$HOST hf_version=$HF_VERSION"

    trap rollback ERR INT TERM

    case "$TARGET" in
        opencode) vendor_skills_opencode ;;
        cursor)   vendor_cursor ;;
        both)
            vendor_skills_opencode
            vendor_cursor
            ;;
    esac

    write_readme
    write_manifest

    trap - ERR INT TERM

    if [ "$DRY_RUN" = 1 ]; then
        log "dry-run complete (no files written)"
    else
        log "install complete: $HOST/.harnessflow-install-manifest.json (${#ENTRIES[@]} entries)"
        log "see $HOST/.harnessflow-install-readme.md for verify + uninstall instructions"
    fi
}

main "$@"
