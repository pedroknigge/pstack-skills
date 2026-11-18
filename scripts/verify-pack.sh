#!/usr/bin/env bash
# Runtime proofs for docs/feature-map.md.
# Bash and Python stdlib only. Structure checks are scripts/check-pack.py.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

EVIDENCE="$ROOT/verify-evidence.md"
EXPECTED_SKILLS=59
VERSION="$(tr -d '[:space:]' < "$ROOT/VERSION")"
MAP="$ROOT/docs/feature-map.md"
SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/verify-pack.XXXXXX")"

LINES=()
fail_count=0

pass() {
  LINES+=("PASS $1")
  printf 'PASS %s\n' "$1"
}

fail() {
  LINES+=("FAIL $1")
  printf 'FAIL %s\n' "$1"
  fail_count=$((fail_count + 1))
}

join_causes() {
  local joined="" line
  for line in "$@"; do
    [[ -n "$line" ]] || continue
    if [[ -n "$joined" ]]; then
      joined+=" | "
    fi
    joined+="$line"
  done
  printf '%s' "$joined"
}

on_exit() {
  local rc=$?
  {
    echo "# verify-evidence"
    echo
    if ((${#LINES[@]})); then
      printf '%s\n' "${LINES[@]}"
    fi
  } >"$EVIDENCE" || true
  rm -rf "$SCRATCH" || true
  exit "$rc"
}
trap on_exit EXIT

prove_install() {
  local home="$SCRATCH/home" log="$SCRATCH/install.log" name extra found
  local -a parents=() causes=()
  local audit audit_rc=0 install_rc=0
  mkdir -p "$home/.agents" "$home/.claude" "$home/.grok" "$home/.cursor" "$home/.gemini"
  if ! HOME="$home" "$ROOT/install.sh" --global >"$log" 2>&1; then
    install_rc=$?
  fi
  if [[ "$install_rc" -ne 0 ]]; then
    fail "global install: install.sh exited ${install_rc}: $(tr '\n' ' ' <"$log") -> fix: ./install.sh --global must succeed when HOME contains .agents .claude .grok .cursor .gemini"
    return
  fi
  for name in .agents .claude .grok .cursor .gemini; do
    parents+=("$home/$name/skills")
  done
  while IFS= read -r extra; do
    [[ -n "$extra" ]] || continue
    found=0
    for name in "${parents[@]}"; do
      [[ "$name" == "$extra" ]] && found=1
    done
    [[ "$found" -eq 1 ]] || parents+=("$extra")
  done < <(find "$home" -type d -name skills | sort)
  audit="$(python3 - "$VERSION" "$EXPECTED_SKILLS" "$ROOT/skills" "${parents[@]}" 2>&1 <<'PY'
import importlib.util
import sys
from pathlib import Path

version, expected_n, skills_dir, *parents = sys.argv[1:]
expected_n = int(expected_n)
skills = Path(skills_dir)
root = skills.parent
checker = root / "scripts" / "check-pack.py"
spec = importlib.util.spec_from_file_location("check_pack", checker)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

prefix = "v" + version
source = sorted(
    p.name for p in skills.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()
)
problems = []
if len(source) != expected_n:
    problems.append(
        f"skills/ has {len(source)} SKILL.md dirs, expected {expected_n} "
        f"-> fix: keep parent pstack plus every ps-* leaf, or change EXPECTED_SKILLS "
        f"in scripts/verify-pack.sh and the {expected_n} in docs/feature-map.md together"
    )
source_set = set(source)
for raw in parents:
    parent = Path(raw)
    label = f"{parent.parent.name}/skills"
    if not parent.is_dir():
        problems.append(
            f"{label} was not created -> fix: install.sh skill_parents must install "
            f"there when ~/{parent.parent.name} exists"
        )
        continue
    got = sorted(
        p.name for p in parent.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()
    )
    if got != source:
        missing = [name for name in source if name not in got]
        extra = [name for name in got if name not in source_set]
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if extra:
            detail.append("unexpected " + ", ".join(extra))
        problems.append(
            f"{label} does not match skills/ ({'; '.join(detail) or 'count mismatch'}) "
            "-> fix: install.sh must copy every skills/<name>/ directory that contains SKILL.md"
        )
    bare = sorted(
        p.name for p in parent.iterdir() if p.is_dir() and not (p / "SKILL.md").is_file()
    )
    if bare:
        problems.append(
            f"{label} has non-skill dirs {', '.join(bare)} -> fix: install.sh must copy only skill folders"
        )
    worker = parent / "ps-poteto-mode" / "worker.md"
    if not worker.is_file():
        problems.append(
            f"{label}/ps-poteto-mode/worker.md is missing -> fix: keep skills/ps-poteto-mode/worker.md and let install.sh copy it"
        )
    for hit in parent.rglob("*"):
        if hit.is_dir() and hit.name in {"test", "tests"}:
            problems.append(
                f"{label} installed {hit.relative_to(parent)} -> fix: move that suite to tests/upstream-<skill>/ and do not ship it under skills/"
            )
    for skill_dir in parent.iterdir():
        md = skill_dir / "SKILL.md"
        if not skill_dir.is_dir() or not md.is_file():
            continue
        rel = f"{label}/{skill_dir.name}/SKILL.md"
        try:
            data, err = mod.parse_frontmatter(md.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            problems.append(
                f"{rel} is unreadable ({exc}) -> fix: write a description that starts with {prefix}"
            )
            continue
        if data is None:
            problems.append(
                f"{rel} {err} -> fix: repair that skill's frontmatter so description starts with {prefix}"
            )
            continue
        desc = data.get("description")
        if not isinstance(desc, str) or not desc.startswith(prefix):
            shown = desc if isinstance(desc, str) else "missing"
            problems.append(
                f"{rel} description does not start with {prefix} (got {shown[:80]!r}) "
                f"-> fix: prefix the source description with {prefix} and reinstall"
            )
for item in problems:
    print(item)
sys.exit(1 if problems else 0)
PY
)" || audit_rc=$?
  if [[ "$audit_rc" -ne 0 ]]; then
    while IFS= read -r line; do
      [[ -n "$line" ]] && causes+=("$line")
    done <<<"$audit"
    [[ ${#causes[@]} -gt 0 ]] || causes+=("install audit exited ${audit_rc} with no detail -> fix: rerun scripts/verify-pack.sh and read the python traceback")
    fail "global install: $(join_causes "${causes[@]}")"
    return
  fi
  pass "global install"
}

prove_npx() {
  if [[ ! -f "$MAP" ]] || ! grep -F -q 'npx skills add pedroknigge/pstack-skills -g -y' "$MAP" || ! grep -F -q 'not run offline' "$MAP"; then
    fail "npx skills add: docs/feature-map.md does not list \`npx skills add pedroknigge/pstack-skills -g -y\` as not run offline -> fix: add that registry-install row and do not invoke npx from scripts/verify-pack.sh"
    return
  fi
  pass "npx skills add (not run offline)"
}

prove_router() {
  local out rc=0
  out="$(python3 "$ROOT/scripts/check-pack.py" 2>&1)" || rc=$?
  if [[ "$rc" -eq 0 && -z "$out" ]]; then
    pass "pstack router"
    return
  fi
  out="$(printf '%s' "$out" | tr '\n' ' ' | sed 's/  */ /g')"
  if [[ -z "$out" ]]; then
    fail "pstack router: check-pack exited ${rc} with no findings -> fix: make python3 scripts/check-pack.py exit 0 on this tree"
    return
  fi
  fail "pstack router: ${out}"
}

prove_issue() {
  local out rc=0 other
  local -a causes=()
  out="$(env -u PS_CHILD -u OF_CHILD bash "$ROOT/scripts/ps-issue.sh" \
    --title "verify pack" --label enhancement --body "offline dry-run" --dry-run 2>&1)" || rc=$?
  if [[ "$rc" -ne 0 ]]; then
    causes+=("dry-run exited ${rc}: ${out} -> fix: scripts/ps-issue.sh --dry-run must print the gh argv and exit 0")
  fi
  if [[ "$out" != *"pedroknigge/pstack-skills"* ]]; then
    causes+=("dry-run output does not name pedroknigge/pstack-skills -> fix: set REPO=pedroknigge/pstack-skills in scripts/ps-issue.sh")
  fi
  if [[ "$out" != *"gh issue create"* ]]; then
    causes+=("dry-run output is not a create preview -> fix: --dry-run must print the gh issue create argv for pedroknigge/pstack-skills")
  fi
  other="$(printf '%s\n' "$out" | grep -oE '[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+' | grep -v '^pedroknigge/pstack-skills$' || true)"
  if [[ -n "$other" ]]; then
    causes+=("dry-run names another repo (${other//$'\n'/, }) -> fix: never target consumer origin; REPO stays pedroknigge/pstack-skills")
  fi
  check_child() {
    local var="$1" child_out child_rc=0
    if [[ "$var" == "PS_CHILD" ]]; then
      child_out="$(env -u OF_CHILD PS_CHILD=1 bash "$ROOT/scripts/ps-issue.sh" \
        --title "should not post" --label bug --body "draft only" </dev/null 2>&1)" || child_rc=$?
    else
      child_out="$(env -u PS_CHILD OF_CHILD=1 bash "$ROOT/scripts/ps-issue.sh" \
        --title "should not post" --label bug --body "draft only" </dev/null 2>&1)" || child_rc=$?
    fi
    if [[ "$child_rc" -eq 0 ]]; then
      causes+=("${var} submit exited 0 -> fix: refuse create in scripts/ps-issue.sh when ${var} is set, before gh issue create")
    elif [[ "$child_out" != *"submit refused"* || "$child_out" != *"PS_CHILD/OF_CHILD"* ]]; then
      causes+=("${var} submit did not refuse as a child (${child_out}) -> fix: die with submit refused while PS_CHILD/OF_CHILD is set and do not call gh")
    fi
  }
  check_child PS_CHILD
  check_child OF_CHILD
  if [[ ${#causes[@]} -gt 0 ]]; then
    fail "ps-issue: $(join_causes "${causes[@]}")"
    return
  fi
  pass "ps-issue"
}

prove_report() {
  local dir="$SCRATCH/report" md html rc=0
  mkdir -p "$dir"
  md="$dir/report.md"
  printf '# Pack verify\n\nruntime proof\n' >"$md"
  html="$(python3 "$ROOT/scripts/render-report.py" "$md" 2>&1)" || rc=$?
  if [[ "$rc" -ne 0 || ! -s "$dir/report.html" ]] || ! grep -q '<html' "$dir/report.html"; then
    fail "render-report: exit ${rc}: ${html} -> fix: python3 scripts/render-report.py must write a non-empty HTML twin beside the markdown"
    return
  fi
  pass "render-report"
}

prove_siblings() {
  local out rc=0 expected
  out="$(bash "$ROOT/scripts/ps-detect-siblings.sh" "$ROOT" 2>&1)" || rc=$?
  expected="$(printf '%s\n' "ArkGate: none" "Orderfield: none" "Docs: none" "Vibe-proof: none")"
  if [[ "$rc" -ne 0 || "$out" != "$expected" ]]; then
    fail "ps-detect-siblings: exit ${rc}, output \`${out//$'\n'/ }\` -> fix: on this repo scripts/ps-detect-siblings.sh must print ArkGate, Orderfield, Docs, and Vibe-proof as none and exit 0"
    return
  fi
  pass "ps-detect-siblings"
}

prove_upstream() {
  local out rc=0
  out="$(python3 - "$ROOT" <<'PY'
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
script = root / "scripts" / "port-upstream.py"
version = (root / "VERSION").read_text(encoding="utf-8").strip()
real_run = subprocess.run
seen = []


def one_line(text: str) -> str:
    text = " ".join(text.split())
    if len(text) > 1500:
        return text[:1500] + " ..."
    return text


def die(msg: str) -> None:
    print(msg)
    sys.exit(1)


def spy(args, *_unused, **_kwargs):
    cmd = [str(part) for part in (args if isinstance(args, (list, tuple)) else [args])]
    existed = (dst / "ps-demo" / "SKILL.md").is_file()
    completed = real_run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    seen.append((cmd, existed, completed.returncode, completed.stdout or ""))
    return completed


subprocess.run = spy
with tempfile.TemporaryDirectory() as tmp:
    src = Path(tmp) / "upstream"
    dst = Path(tmp) / "out"
    skill = src / "demo"
    skill.mkdir(parents=True)
    dst.mkdir()
    (skill / "SKILL.md").write_text(
        "---\nname: demo\ndescription: \"demo skill\"\n---\n\n# demo\n",
        encoding="utf-8",
    )
    sys.argv = [str(script), str(src), str(dst), version]
    scope = {"__name__": "__main__", "__file__": str(script)}
    code = 0
    try:
        exec(compile(script.read_text(encoding="utf-8"), str(script), "exec"), scope)
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    except Exception as exc:
        die(
            f"port-upstream.py raised {type(exc).__name__}: {exc} -> fix: "
            "scripts/port-upstream.py must port the temp tree and then run scripts/check-pack.py"
        )
    if not seen:
        die(
            "port-upstream.py never called check-pack.py -> fix: "
            "subprocess-run scripts/check-pack.py after the leaf rewrite and sys.exit with its status"
        )
    cmd, existed, rc, output = seen[-1]
    if not cmd or not str(cmd[-1]).endswith("check-pack.py"):
        die(
            f"last subprocess was {cmd!r}, not check-pack.py -> fix: "
            "call scripts/check-pack.py as the last step of scripts/port-upstream.py"
        )
    if not existed:
        die(
            "check-pack.py ran before the ported skill existed -> fix: "
            "run scripts/check-pack.py after the leaf rewrite in scripts/port-upstream.py"
        )
    if rc != 0 or code != 0:
        detail = one_line(output) or "no output"
        die(
            f"check-pack.py exited {rc} (porter status {code}): {detail} -> fix: "
            "apply the check-pack fix and keep port-upstream.py exiting with that status"
        )
PY
)" || rc=$?
  if [[ "$rc" -ne 0 ]]; then
    out="$(printf '%s' "$out" | tr '\n' ' ' | sed 's/  */ /g')"
    fail "port-upstream: ${out:-porter check exited ${rc} -> fix: run scripts/check-pack.py at the end of scripts/port-upstream.py}"
    return
  fi
  pass "port-upstream"
}

prove_install
prove_npx
prove_router
prove_issue
prove_report
prove_siblings
prove_upstream

if ((fail_count > 0)); then
  exit 1
fi
exit 0
