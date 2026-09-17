#!/usr/bin/env bash
# Sensor-only sibling detector for the pstack-skills parent router.
# Prints announce lines. Does not install, invoke, or vendor siblings.
#
# Usage:
#   scripts/ps-detect-siblings.sh           # cwd + parents + $HOME skill dirs
#   scripts/ps-detect-siblings.sh PATH      # that tree only (no $HOME leak)
set -euo pipefail

explicit=0
if [[ $# -ge 1 ]]; then
  root="$1"
  explicit=1
else
  root="."
fi
root="$(cd "$root" && pwd)"

skill_parents=()
add_parent() {
  local d="$1"
  [[ -d "$d" ]] || return 0
  skill_parents+=("$d")
}

add_parent "${root}/.agents/skills"
add_parent "${root}/.claude/skills"
add_parent "${root}/.cursor/skills"
add_parent "${root}/.grok/skills"
if [[ "$explicit" -eq 0 ]]; then
  add_parent "${HOME}/.agents/skills"
  add_parent "${HOME}/.claude/skills"
  add_parent "${HOME}/.cursor/skills"
  add_parent "${HOME}/.grok/skills"
fi

have_skill() {
  local name="$1"
  local p
  for p in "${skill_parents[@]+"${skill_parents[@]}"}"; do
    if [[ -f "${p}/${name}/SKILL.md" ]]; then
      return 0
    fi
  done
  return 1
}

walk_has() {
  local rel="$1"
  if [[ "$explicit" -eq 1 ]]; then
    [[ -e "${root}/${rel}" ]]
    return $?
  fi
  local here="$root"
  local i
  for i in 0 1 2 3 4; do
    [[ -e "${here}/${rel}" ]] && return 0
    [[ "$here" == "/" ]] && return 1
    here="$(dirname "$here")"
  done
  return 1
}

on_path() {
  [[ "$explicit" -eq 0 ]] && command -v "$1" >/dev/null 2>&1
}

ark="none"
if walk_has "ark.config.json" || walk_has ".ark" || on_path ark-check \
  || have_skill ark-check || have_skill ark-adopt || have_skill ark-loop; then
  ark="detected"
fi

of="none"
if walk_has ".orderfield" || walk_has "ORDER.json" || on_path of \
  || have_skill of || have_skill orderfield; then
  of="detected"
fi

docs="none"
if have_skill documentation-manager; then
  docs="detected"
fi

vp="none"
if have_skill vibe-proof-auditor || walk_has "vibe-proof-audit-report.md"; then
  vp="detected"
fi

printf 'ArkGate: %s\n' "$ark"
printf 'Orderfield: %s\n' "$of"
printf 'Docs: %s\n' "$docs"
printf 'Vibe-proof: %s\n' "$vp"
