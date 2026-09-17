#!/usr/bin/env bash
# Install the pstack-skills pack (parent pstack + every ps-* leaf)
# into detected agent skill dirs.
# `npx skills add pedroknigge/pstack-skills -g -y` is the primary path;
# this script covers ~/.agents/skills plus Claude, Grok, and Gemini/AGY trees.
set -euo pipefail

REPO_URL="${PSTACK_SKILLS_REPO:-https://github.com/pedroknigge/pstack-skills.git}"
PACK_NAME="pstack-skills"

SRC="$(cd "$(dirname "$0")" 2>/dev/null && pwd || true)"
cleanup_src=""
MODE="global"
UNINSTALL=0
copied=0
removed=0

usage() {
  cat <<EOF
Usage: ./install.sh [--global|--project] [--uninstall] [--help]

  --global     Install under \$HOME (default)
  --project    Install under the current workspace
  --uninstall  Remove installed copies from the chosen scope

Copies every folder in skills/ (pstack parent + ps-* leaves) into each
detected agent skill directory. Idempotent: destination folders are replaced.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --global) MODE="global"; shift ;;
    --project) MODE="project"; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

have_local() {
  [[ -n "${SRC}" && -f "${SRC}/skills/pstack/SKILL.md" && -d "${SRC}/skills" ]]
}

if ! have_local; then
  SRC="$(mktemp -d "${TMPDIR:-/tmp}/pstack-skills-install.XXXXXX")"
  cleanup_src="$SRC"
  git clone --depth 1 "$REPO_URL" "$SRC" >/dev/null
fi

trap '[[ -n "$cleanup_src" ]] && rm -rf "$cleanup_src"' EXIT

if [[ "$MODE" == "global" ]]; then
  base="${HOME}"
else
  base="$(pwd)"
fi

skill_names() {
  local d
  for d in "${SRC}/skills"/*; do
    [[ -d "$d" && -f "$d/SKILL.md" ]] || continue
    basename "$d"
  done
}

copy_skill() {
  local name="$1" dest_parent="$2"
  local dest="${dest_parent}/${name}"
  mkdir -p "$dest_parent"
  rm -rf "$dest"
  mkdir -p "$dest"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --exclude .git "${SRC}/skills/${name}/" "$dest/"
  else
    cp -R "${SRC}/skills/${name}/." "$dest/"
    rm -rf "$dest/.git"
  fi
}

remove_skill() {
  local name="$1" dest_parent="$2"
  local dest="${dest_parent}/${name}"
  if [[ -e "$dest" || -L "$dest" ]]; then
    rm -rf "$dest"
    return 0
  fi
  return 1
}

# Print skill-parent dirs that should receive the pack.
skill_parents() {
  if [[ "$MODE" == "global" ]]; then
    printf '%s\n' "${base}/.agents/skills"
    if command -v claude >/dev/null 2>&1 || [[ -d "${base}/.claude" ]]; then
      printf '%s\n' "${base}/.claude/skills"
    fi
    if command -v grok >/dev/null 2>&1 || [[ -d "${base}/.grok" ]]; then
      printf '%s\n' "${base}/.grok/skills"
    fi
    if command -v gemini >/dev/null 2>&1 || [[ -d "${base}/.gemini" ]]; then
      printf '%s\n' "${base}/.gemini/skills"
    fi
    if command -v agy >/dev/null 2>&1 || [[ -d "${base}/.gemini/config/skills" ]]; then
      printf '%s\n' "${base}/.gemini/config/skills"
    fi
    if command -v agy >/dev/null 2>&1 || [[ -d "${base}/.gemini/antigravity-cli/skills" ]]; then
      printf '%s\n' "${base}/.gemini/antigravity-cli/skills"
    fi
    if command -v agy >/dev/null 2>&1 || [[ -d "${base}/.gemini/antigravity/skills" ]]; then
      printf '%s\n' "${base}/.gemini/antigravity/skills"
    fi
    if [[ -d "${base}/.cursor/skills" ]]; then
      printf '%s\n' "${base}/.cursor/skills"
    fi
  else
    printf '%s\n' "${base}/.agents/skills"
    [[ -d "${base}/.claude" ]] && printf '%s\n' "${base}/.claude/skills"
    [[ -d "${base}/.grok" || -f "${base}/.grok/config.toml" ]] && printf '%s\n' "${base}/.grok/skills"
    [[ -d "${base}/.gemini" ]] && printf '%s\n' "${base}/.gemini/skills"
    [[ -d "${base}/.cursor/skills" ]] && printf '%s\n' "${base}/.cursor/skills"
  fi
}

unique_parents() {
  skill_parents | awk 'NF && !seen[$0]++'
}

names="$(skill_names)"
if [[ -z "$names" ]]; then
  echo "no skills found under ${SRC}/skills" >&2
  exit 1
fi
skill_count=$(printf '%s\n' "$names" | grep -c . || true)

if [[ "$UNINSTALL" -eq 1 ]]; then
  while IFS= read -r parent; do
    [[ -n "$parent" ]] || continue
    while IFS= read -r name; do
      [[ -n "$name" ]] || continue
      if remove_skill "$name" "$parent"; then
        echo "removed ${parent}/${name}"
        removed=$((removed + 1))
      fi
    done <<< "$names"
  done < <(unique_parents)
  echo "removed ${removed} skill dir(s) (${skill_count} skills in pack)"
  exit 0
fi

while IFS= read -r parent; do
  [[ -n "$parent" ]] || continue
  mkdir -p "$parent"
  while IFS= read -r name; do
    [[ -n "$name" ]] || continue
    copy_skill "$name" "$parent"
    copied=$((copied + 1))
  done <<< "$names"
  echo "installed ${skill_count} skills → ${parent}"
done < <(unique_parents)

echo "copied ${copied} skill dir(s) (${skill_count} skills × destinations)"
echo "generic: ${base}/.agents/skills/{pstack,ps-*}"
echo "or: npx skills add pedroknigge/${PACK_NAME} -g -y"
