#!/usr/bin/env bash
# tests/test_install_scripts.sh — End-to-end tests for install.sh / uninstall.sh.
#
# Covers the 12 scenarios from features/001-install-scripts/design.md §16:
#   #1 opencode copy            #7 user-skill preserved (HYP-002 Blocking)
#   #2 opencode symlink         #8 dry-run no side effects
#   #3 cursor copy              #9 force re-install
#   #4 cursor symlink          #10 NFR-004 grep audit (no jq/python/node/npm)
#   #5 both copy               #11 ASM-001 non-git checkout fallback
#   #6 both symlink            #12 NFR-002 mid-failure rollback
#
# Usage:
#   bash tests/test_install_scripts.sh                 # run all 12
#   bash tests/test_install_scripts.sh --only=1,7,12   # run subset

set -uo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HF_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
INSTALL="$HF_REPO/install.sh"
UNINSTALL="$HF_REPO/uninstall.sh"

ONLY=""
PASS_COUNT=0
FAIL_COUNT=0
FAILED_SCENARIOS=()

while [ $# -gt 0 ]; do
    case "$1" in
        --only)   ONLY="${2:-}"; shift 2 ;;
        --only=*) ONLY="${1#*=}"; shift ;;
        *) printf '[test] unknown arg: %s\n' "$1" >&2; exit 1 ;;
    esac
done

should_run() {
    local n="$1"
    if [ -z "$ONLY" ]; then return 0; fi
    case ",$ONLY," in
        *,"$n",*) return 0 ;;
        *) return 1 ;;
    esac
}

mk_host() {
    mktemp -d -t hf-install-test.XXXXXX
}

assert_eq() {
    local actual="$1" expected="$2" msg="$3"
    if [ "$actual" = "$expected" ]; then
        return 0
    fi
    printf '  ❌ %s: expected=%s actual=%s\n' "$msg" "$expected" "$actual" >&2
    return 1
}

assert_ge() {
    local actual="$1" min="$2" msg="$3"
    if [ "$actual" -ge "$min" ] 2>/dev/null; then
        return 0
    fi
    printf '  ❌ %s: actual=%s not ≥ %s\n' "$msg" "$actual" "$min" >&2
    return 1
}

assert_file() {
    local p="$1" msg="$2"
    if [ -f "$p" ] || [ -L "$p" ]; then
        return 0
    fi
    printf '  ❌ %s: file not present at %s\n' "$msg" "$p" >&2
    return 1
}

assert_symlink_to() {
    local link="$1" want_target="$2" msg="$3"
    if [ ! -L "$link" ]; then
        printf '  ❌ %s: %s is not a symlink\n' "$msg" "$link" >&2
        return 1
    fi
    local got
    got="$(readlink "$link")"
    if [ "$got" = "$want_target" ]; then
        return 0
    fi
    printf '  ❌ %s: symlink target want=%s got=%s\n' "$msg" "$want_target" "$got" >&2
    return 1
}

count_skill_md_in() {
    local root="$1"
    if [ ! -d "$root" ] && [ ! -L "$root" ]; then
        printf '0'
        return
    fi
    find "$root" -mindepth 2 -maxdepth 2 -name SKILL.md 2>/dev/null | wc -l | tr -d ' '
}

manifest_has_path() {
    local manifest="$1" want_path="$2"
    grep -q "\"path\"[[:space:]]*:[[:space:]]*\"$want_path\"" "$manifest"
}

run_scenario() {
    local n="$1" desc="$2" fn="$3"
    if ! should_run "$n"; then return 0; fi
    printf '== scenario #%s: %s ==\n' "$n" "$desc"
    local host
    host="$(mk_host)"
    local rc=0
    if "$fn" "$host"; then
        printf '  ✅ PASS\n'
        PASS_COUNT=$((PASS_COUNT+1))
    else
        printf '  ❌ FAIL (host=%s, kept for inspection)\n' "$host" >&2
        FAIL_COUNT=$((FAIL_COUNT+1))
        FAILED_SCENARIOS+=("$n")
        rc=1
    fi
    if [ "$rc" = 0 ]; then
        rm -rf "$host" 2>/dev/null || true
    fi
    return 0
}

# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------

scenario_1() { # opencode copy
    local host="$1"
    bash "$INSTALL" --target opencode --host "$host" >/dev/null || return 1
    local n
    n=$(count_skill_md_in "$host/.opencode/skills")
    assert_ge "$n" 24 "skills count" || return 1
    assert_file "$host/.harnessflow-install-manifest.json" "manifest exists" || return 1
    assert_file "$host/.harnessflow-install-readme.md" "readme exists" || return 1
    manifest_has_path "$host/.harnessflow-install-manifest.json" ".opencode/skills/hf-finalize" \
        || { printf '  ❌ manifest lacks per-skill entry\n' >&2; return 1; }
}

scenario_2() { # opencode symlink
    local host="$1"
    bash "$INSTALL" --target opencode --topology symlink --host "$host" >/dev/null || return 1
    assert_symlink_to "$host/.opencode/skills" "$HF_REPO/skills" "opencode symlink" || return 1
    manifest_has_path "$host/.harnessflow-install-manifest.json" ".opencode/skills" || return 1
}

scenario_3() { # cursor copy
    local host="$1"
    bash "$INSTALL" --target cursor --host "$host" >/dev/null || return 1
    local n
    n=$(count_skill_md_in "$host/.cursor/harness-flow-skills")
    assert_ge "$n" 24 "cursor skills count" || return 1
    assert_file "$host/.cursor/rules/harness-flow.mdc" "cursor rule" || return 1
    manifest_has_path "$host/.harnessflow-install-manifest.json" ".cursor/rules/harness-flow.mdc" || return 1
}

scenario_4() { # cursor symlink
    local host="$1"
    bash "$INSTALL" --target cursor --topology symlink --host "$host" >/dev/null || return 1
    assert_symlink_to "$host/.cursor/harness-flow-skills" "$HF_REPO/skills" "cursor skills symlink" || return 1
    assert_symlink_to "$host/.cursor/rules/harness-flow.mdc" "$HF_REPO/.cursor/rules/harness-flow.mdc" "cursor rule symlink" || return 1
}

scenario_5() { # both copy
    local host="$1"
    bash "$INSTALL" --target both --host "$host" >/dev/null || return 1
    assert_ge "$(count_skill_md_in "$host/.opencode/skills")" 24 "opencode skills" || return 1
    assert_ge "$(count_skill_md_in "$host/.cursor/harness-flow-skills")" 24 "cursor skills" || return 1
    assert_file "$host/.cursor/rules/harness-flow.mdc" "cursor rule" || return 1
}

scenario_6() { # both symlink
    local host="$1"
    bash "$INSTALL" --target both --topology symlink --host "$host" >/dev/null || return 1
    assert_symlink_to "$host/.opencode/skills" "$HF_REPO/skills" "opencode symlink" || return 1
    assert_symlink_to "$host/.cursor/harness-flow-skills" "$HF_REPO/skills" "cursor skills symlink" || return 1
    assert_symlink_to "$host/.cursor/rules/harness-flow.mdc" "$HF_REPO/.cursor/rules/harness-flow.mdc" "cursor rule symlink" || return 1
}

scenario_7() { # HYP-002 Blocking: user-skill survives uninstall
    local host="$1"
    bash "$INSTALL" --target opencode --host "$host" >/dev/null || return 1
    mkdir -p "$host/.opencode/skills/my-own-skill"
    printf 'user content\n' > "$host/.opencode/skills/my-own-skill/SKILL.md"
    bash "$UNINSTALL" --host "$host" >/dev/null || return 1
    assert_file "$host/.opencode/skills/my-own-skill/SKILL.md" "user-skill preserved" || return 1
    if [ -d "$host/.opencode/skills/hf-finalize" ]; then
        printf '  ❌ HF skill still present after uninstall\n' >&2
        return 1
    fi
    if [ -f "$host/.harnessflow-install-manifest.json" ]; then
        printf '  ❌ manifest still present after uninstall\n' >&2
        return 1
    fi
}

scenario_8() { # dry-run no side effects
    local host="$1"
    local before
    before=$(find "$host" 2>/dev/null | wc -l | tr -d ' ')
    bash "$INSTALL" --target both --dry-run --host "$host" >/dev/null || return 1
    local after
    after=$(find "$host" 2>/dev/null | wc -l | tr -d ' ')
    assert_eq "$after" "$before" "no files written in dry-run" || return 1
    if [ -e "$host/.opencode" ] || [ -e "$host/.cursor" ] || [ -e "$host/.harnessflow-install-manifest.json" ]; then
        printf '  ❌ dry-run created artifacts\n' >&2
        return 1
    fi
    # Verbose vs default line counts (FR-007 acceptance):
    local default_lines verbose_lines
    default_lines=$(bash "$INSTALL" --target opencode --dry-run --host "$host" 2>&1 | wc -l | tr -d ' ')
    verbose_lines=$(bash "$INSTALL" --target opencode --dry-run --verbose --host "$host" 2>&1 | wc -l | tr -d ' ')
    if [ "$default_lines" -ge 10 ]; then
        # In dry-run mode op() prints; tighten check by comparing verbose vs non-verbose,
        # since dry-run forces verbose-like output. Use non-dry default mode for default check.
        :
    fi
    if [ "$verbose_lines" -le 24 ]; then
        printf '  ❌ verbose output too short: %s lines (expected > 24)\n' "$verbose_lines" >&2
        return 1
    fi
    # Default banner-only mode (no dry-run, no verbose) on a fresh host:
    local fresh
    fresh="$(mk_host)"
    local plain_lines
    plain_lines=$(bash "$INSTALL" --target opencode --host "$fresh" 2>&1 | wc -l | tr -d ' ')
    rm -rf "$fresh"
    if [ "$plain_lines" -ge 10 ]; then
        printf '  ❌ default output too verbose: %s lines (expected < 10)\n' "$plain_lines" >&2
        return 1
    fi
}

scenario_9() { # force re-install
    local host="$1"
    bash "$INSTALL" --target opencode --host "$host" >/dev/null || return 1
    if bash "$INSTALL" --target opencode --host "$host" >/dev/null 2>&1; then
        printf '  ❌ second install without --force should have failed\n' >&2
        return 1
    fi
    bash "$INSTALL" --target opencode --host "$host" --force >/dev/null || return 1
    assert_file "$host/.harnessflow-install-manifest.json" "manifest after --force" || return 1
    # uninstall.sh dry-run leaves files (FR-005 acceptance for uninstall branch):
    local files_before
    files_before=$(find "$host" 2>/dev/null | wc -l | tr -d ' ')
    bash "$UNINSTALL" --host "$host" --dry-run >/dev/null || return 1
    local files_after
    files_after=$(find "$host" 2>/dev/null | wc -l | tr -d ' ')
    assert_eq "$files_after" "$files_before" "uninstall dry-run is no-op" || return 1
}

scenario_10() { # NFR-004 grep audit
    local _host="$1"
    local hits
    hits=$( (awk '!/^[[:space:]]*#/' "$INSTALL" "$UNINSTALL") \
            | grep -E '\b(jq|python|node|npm)\b' || true)
    if [ -n "$hits" ]; then
        printf '  ❌ NFR-004 grep audit found forbidden tokens:\n%s\n' "$hits" >&2
        return 1
    fi
}

scenario_11() { # ASM-001 non-git checkout fallback
    local host="$1"
    local fake_repo
    fake_repo="$(mktemp -d -t hf-fakezip.XXXXXX)"
    cp -R "$HF_REPO/skills" "$fake_repo/skills"
    cp -R "$HF_REPO/.cursor" "$fake_repo/.cursor"
    cp "$HF_REPO/install.sh" "$fake_repo/install.sh"
    cp "$HF_REPO/uninstall.sh" "$fake_repo/uninstall.sh"
    cp "$HF_REPO/CHANGELOG.md" "$fake_repo/CHANGELOG.md"
    chmod +x "$fake_repo/install.sh" "$fake_repo/uninstall.sh"
    bash "$fake_repo/install.sh" --target opencode --host "$host" >/dev/null || {
        rm -rf "$fake_repo"
        return 1
    }
    local mf="$host/.harnessflow-install-manifest.json"
    if ! grep -q '"hf_commit"[[:space:]]*:[[:space:]]*"unknown-non-git-checkout"' "$mf"; then
        printf '  ❌ hf_commit not downgraded to unknown-non-git-checkout\n' >&2
        rm -rf "$fake_repo"
        return 1
    fi
    if ! grep -qE '"hf_version"[[:space:]]*:[[:space:]]*"[0-9]+\.[0-9]+\.[0-9]+"' "$mf"; then
        printf '  ❌ hf_version not parsed from CHANGELOG\n' >&2
        rm -rf "$fake_repo"
        return 1
    fi
    rm -rf "$fake_repo"
}

scenario_12() { # NFR-002 mid-failure rollback
    local host="$1"
    # Make the host directory read-only so install.sh's first mkdir fails.
    chmod -w "$host"
    local before_count
    before_count=$(find "$host" 2>/dev/null | wc -l | tr -d ' ')
    if bash "$INSTALL" --target opencode --host "$host" >/dev/null 2>&1; then
        chmod +w "$host"
        printf '  ❌ install should have failed when host is read-only\n' >&2
        return 1
    fi
    chmod +w "$host"
    local after_count
    after_count=$(find "$host" 2>/dev/null | wc -l | tr -d ' ')
    assert_eq "$after_count" "$before_count" "host returns to pre-install state" || return 1
    if [ -f "$host/.harnessflow-install-manifest.json" ]; then
        printf '  ❌ manifest leaked after rollback\n' >&2
        return 1
    fi
}

# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

run_scenario 1  "opencode copy"                      scenario_1
run_scenario 2  "opencode symlink"                   scenario_2
run_scenario 3  "cursor copy"                        scenario_3
run_scenario 4  "cursor symlink"                     scenario_4
run_scenario 5  "both copy"                          scenario_5
run_scenario 6  "both symlink"                       scenario_6
run_scenario 7  "HYP-002 user-skill preserved"       scenario_7
run_scenario 8  "dry-run no side effects + FR-007"   scenario_8
run_scenario 9  "force re-install + uninstall dry-run" scenario_9
run_scenario 10 "NFR-004 grep audit"                 scenario_10
run_scenario 11 "ASM-001 non-git checkout fallback"  scenario_11
run_scenario 12 "NFR-002 mid-failure rollback"       scenario_12

printf '\nResult: %s passed, %s failed\n' "$PASS_COUNT" "$FAIL_COUNT"
if [ "$FAIL_COUNT" -gt 0 ]; then
    printf 'Failed scenarios: %s\n' "${FAILED_SCENARIOS[*]}"
    exit 1
fi
