#!/usr/bin/env bash
# HITL issue reporter for pstack-skills itself.
# Always targets pedroknigge/pstack-skills — never the consumer working-tree origin.
# Never creates a GitHub issue without explicit human confirmation in the same turn.
set -euo pipefail

REPO="pedroknigge/pstack-skills"
ALLOWED_LABELS="bug enhancement dogfood blindtest"
TITLE_MAX=256
SEARCH_MAX=256
BODY_MAX_BYTES=32768
BODY_MAX_LINES=400

usage() {
  cat <<EOF
Usage:
  scripts/ps-issue.sh --search [QUERY] [--dry-run]
  scripts/ps-issue.sh --title TEXT --label LABEL [--label LABEL] \\
      (--body TEXT | --body-file PATH) [--dry-run] [--confirm]

LABEL is one of: ${ALLOWED_LABELS}
--label may be repeated or comma-separated (e.g. --label dogfood,enhancement).

Always files on ${REPO}. Never consumer origin.
Create requires --confirm after a human yes in this turn, or a TTY y/N.
--dry-run previews argv and is not HITL.
Child/subagent sessions (PS_CHILD / OF_CHILD set) may only --search or --dry-run.
EOF
}

SEARCH=""
HAVE_SEARCH=0
TITLE=""
BODY=""
BODY_FILE=""
LABELS=()
DRY_RUN=0
CONFIRM=0

die() {
  echo "ps-issue: $*" >&2
  exit 1
}

is_allowed_label() {
  local cand="$1" tok
  for tok in $ALLOWED_LABELS; do
    [[ "$cand" == "$tok" ]] && return 0
  done
  return 1
}

add_labels() {
  local raw="$1" part existing
  raw="${raw//,/ }"
  for part in $raw; do
    [[ -n "$part" ]] || continue
    is_allowed_label "$part" || die "--label must be one of: ${ALLOWED_LABELS}"
    for existing in "${LABELS[@]+"${LABELS[@]}"}"; do
      [[ "$existing" == "$part" ]] && continue 2
    done
    LABELS+=("$part")
  done
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --search)
      HAVE_SEARCH=1
      if [[ $# -ge 2 && "$2" != --* ]]; then
        SEARCH="$2"
        shift 2
      else
        SEARCH=""
        shift
      fi
      ;;
    --title) TITLE="${2:-}"; shift 2 ;;
    --body) BODY="${2:-}"; shift 2 ;;
    --body-file) BODY_FILE="${2:-}"; shift 2 ;;
    --label) add_labels "${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --confirm) CONFIRM=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

is_child() {
  [[ -n "${PS_CHILD:-}" || -n "${OF_CHILD:-}" ]]
}

redact() {
  # Strip common secret/token shapes. Do not send leftovers that are only redaction.
  printf '%s' "$1" | sed -E \
    -e 's/ghp_[A-Za-z0-9_]{20,}/<redacted>/g' \
    -e 's/github_pat_[A-Za-z0-9_]{20,}/<redacted>/g' \
    -e 's/gho_[A-Za-z0-9_]{20,}/<redacted>/g' \
    -e 's/sk-[A-Za-z0-9_-]{20,}/<redacted>/g' \
    -e 's/AKIA[0-9A-Z]{16}/<redacted>/g' \
    -e 's/(Bearer[[:space:]]+)[A-Za-z0-9._~+/=-]{12,}/\1<redacted>/g' \
    -e 's/(x-access-token:)[^[:space:]@]+/\1<redacted>/g'
}

single_line() {
  local flag="$1" text="$2" max="$3"
  [[ -n "$text" ]] || die "$flag is empty"
  if [[ "$text" == *$'\n'* ]]; then
    die "$flag must be a single line"
  fi
  if ((${#text} > max)); then
    die "$flag is ${#text} chars; refuse huge dumps (max ${max})"
  fi
  text="$(redact "$text")"
  [[ "$text" != "<redacted>" ]] || die "$flag is secret/PII-shaped; refused"
  [[ -n "$text" ]] || die "$flag is empty after redaction"
  printf '%s' "$text"
}

check_body_size() {
  local flag="$1" text="$2"
  local nbytes nlines
  nbytes="$(printf '%s' "$text" | wc -c | tr -d ' ')"
  nlines="$(printf '%s' "$text" | awk 'END{print NR+0}')"
  if (( nbytes > BODY_MAX_BYTES || nlines > BODY_MAX_LINES )); then
    die "$flag is ${nbytes} bytes / ${nlines} lines; refuse huge dumps"
  fi
  [[ -n "${text//[[:space:]]/}" ]] || die "$flag is empty"
}

preview() {
  printf 'dry-run argv:\n'
  printf '%q ' "$@"
  printf '\n'
}

require_gh() {
  command -v gh >/dev/null 2>&1 || die "gh is not on PATH; install GitHub CLI and run gh auth login"
  GH_PROMPT_DISABLED=1 GH_NO_UPDATE_NOTIFIER=1 gh auth status >/dev/null 2>&1 \
    || die "gh is not authenticated; run gh auth login"
}

if [[ "$HAVE_SEARCH" -eq 1 ]]; then
  if [[ -n "$SEARCH" ]]; then
    SEARCH="$(single_line --search "$SEARCH" "$SEARCH_MAX")"
  fi
  argv=(gh issue list --repo "$REPO" --state open --limit 100)
  if [[ "$DRY_RUN" -eq 1 ]]; then
    preview "${argv[@]}"
    [[ -n "$SEARCH" ]] && echo "filter: ${SEARCH}"
    exit 0
  fi
  require_gh
  out="$(GH_PROMPT_DISABLED=1 GH_NO_UPDATE_NOTIFIER=1 "${argv[@]}")" || die "gh issue list failed"
  if [[ -n "$SEARCH" ]]; then
    filtered="$(printf '%s\n' "$out" | grep -i -- "$SEARCH" || true)"
    if [[ -z "$filtered" ]]; then
      echo "no matching open issues on ${REPO} for ${SEARCH}"
    else
      printf '%s\n' "$filtered"
    fi
  else
    if [[ -z "${out//[[:space:]]/}" ]]; then
      echo "no matching open issues on ${REPO}"
    else
      printf '%s\n' "$out"
    fi
  fi
  exit 0
fi

[[ -n "$TITLE" ]] || die "create needs --title, --body or --body-file, and --label (${ALLOWED_LABELS}) (or --search to list)"
[[ ${#LABELS[@]} -gt 0 ]] || die "create needs at least one --label (${ALLOWED_LABELS})"
if [[ -n "$BODY_FILE" && -n "$BODY" ]]; then
  die "--body and --body-file cannot both be set"
fi
if [[ -z "$BODY_FILE" && -z "$BODY" ]]; then
  die "create needs --body or --body-file"
fi

if [[ "$DRY_RUN" -eq 0 ]] && is_child; then
  die "submit refused while PS_CHILD/OF_CHILD is set (leader-only after HITL; draft with --dry-run or ISSUE.md)"
fi

TITLE="$(single_line --title "$TITLE" "$TITLE_MAX")"

if [[ -n "$BODY_FILE" ]]; then
  [[ -f "$BODY_FILE" ]] || die "--body-file not found"
  [[ ! -L "$BODY_FILE" ]] || die "--body-file cannot be a symlink"
  BODY="$(cat "$BODY_FILE")"
  check_body_size --body-file "$BODY"
else
  check_body_size --body "$BODY"
fi
BODY="$(redact "$BODY")"
check_body_size --body "$BODY"

argv=(gh issue create --repo "$REPO" --title "$TITLE" --body "$BODY")
for label in "${LABELS[@]}"; do
  argv+=(--label "$label")
done

if [[ "$DRY_RUN" -eq 1 ]]; then
  preview "${argv[@]}"
  exit 0
fi

if [[ "$CONFIRM" -eq 0 ]]; then
  if [[ -t 0 && -t 1 ]]; then
    printf 'Create GitHub issue on %s? [y/N] ' "$REPO"
    read -r answer || answer=""
    case "$(printf '%s' "$answer" | tr '[:upper:]' '[:lower:]')" in
      y|yes) ;;
      *) die "create refused without HITL (--confirm after human yes, or answer yes on a TTY; --dry-run is not HITL)" ;;
    esac
  else
    die "create refused without HITL (--confirm after human yes, or answer yes on a TTY; --dry-run is not HITL)"
  fi
fi

require_gh
GH_PROMPT_DISABLED=1 GH_NO_UPDATE_NOTIFIER=1 "${argv[@]}"
