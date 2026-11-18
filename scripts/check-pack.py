#!/usr/bin/env python3
"""Deterministic structure check for the pstack-skills pack.

Exit 0 when the tree is clean, 1 when there is a finding. One stdout line per
finding: `<path>: <what is wrong> -> fix: <exact fix>`.
Allowlist: scripts/check-pack.allow (path, tab, exact span) skips intentional upstream-name quotes and foreign filenames.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
MAX_FILE = 512 * 1024
MAX_TREE = 2 * 1024 * 1024
UPSTREAM_DOCS = "https://github.com/cursor/plugins/tree/main/pstack/"
PATH_EXT = (
    "md",
    "markdown",
    "py",
    "sh",
    "ts",
    "tsx",
    "js",
    "mjs",
    "cjs",
    "tsv",
    "json",
    "html",
    "txt",
    "yml",
    "yaml",
    "toml",
)
FINDINGS: list[str] = []


def add(path: str, what: str, fix: str) -> None:
    FINDINGS.append(f"{path}: {what} -> fix: {fix}")


def load_allow() -> set[tuple[str, str]]:
    path = ROOT / "scripts" / "check-pack.allow"
    rules: set[tuple[str, str]] = set()
    if not path.is_file():
        return rules
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        rel, _, span = line.partition("\t")
        if span:
            rules.add((rel.strip(), span))
    return rules


def allowed(rel: str, span: str, rules: set[tuple[str, str]]) -> bool:
    return (rel, span) in rules


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        if value[0] == '"':
            return json.loads(value)
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, object] | None, str]:
    if not text.startswith("---\n"):
        return None, "frontmatter is missing the opening ---"
    end = text.find("\n---\n", 3)
    if end < 0:
        return None, "frontmatter is missing the closing ---"
    data: dict[str, object] = {}
    meta: dict[str, str] = {}
    in_meta = False
    lines = text[4:end].split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if in_meta and line.startswith("  ") and not line.startswith("   "):
            key, sep, raw = line.strip().partition(":")
            if not sep:
                return None, f"metadata line `{line.strip()}` is not `key: value`"
            try:
                meta[key.strip()] = unquote(raw.strip())
            except json.JSONDecodeError:
                return None, f"metadata `{key.strip()}` value is not parseable"
            i += 1
            continue
        in_meta = False
        if line.startswith(" ") or line.startswith("\t"):
            return None, (
                f"indented line `{line.strip()}` sits outside a key "
                "(a folded description was left outside the description scalar)"
            )
        key, sep, raw = line.partition(":")
        if not sep or not key.strip():
            return None, f"`{line.strip()}` is not `key: value`"
        key = key.strip()
        raw = raw.strip()
        if key == "metadata" and raw == "":
            in_meta = True
            data["metadata"] = meta
            i += 1
            continue
        if raw in {">", ">-", "|", "|-"}:
            i += 1
            parts: list[str] = []
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].strip() == ""):
                if lines[i].strip():
                    parts.append(lines[i].strip())
                i += 1
            data[key] = " ".join(parts)
            continue
        try:
            data[key] = unquote(raw)
        except json.JSONDecodeError:
            return None, f"`{key}` value is not parseable"
        i += 1
    data["metadata"] = meta
    return data, ""


def check_frontmatter(version: str) -> None:
    for folder in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        rel_dir = f"skills/{folder.name}"
        skill = folder / "SKILL.md"
        if not skill.is_file():
            add(rel_dir, "folder has no SKILL.md", f"add {rel_dir}/SKILL.md")
            continue
        rel = f"{rel_dir}/SKILL.md"
        text = skill.read_text(encoding="utf-8")
        data, err = parse_frontmatter(text)
        if data is None:
            fix = "make the leading --- block `key: value` lines, with metadata.version indented under metadata"
            if "folded description" in err:
                fix = f'join the continuation into `description: "v{version}. …"`'
            add(rel, err, fix)
            continue
        name = data.get("name")
        if not isinstance(name, str) or not name:
            add(rel, "name is missing", f"set `name: {folder.name}`")
        elif name != folder.name:
            add(rel, f"name is `{name}`", f"set `name: {folder.name}`")
        if folder.name == "pstack":
            if name != "pstack":
                add(rel, "router name is not `pstack`", "set `name: pstack`")
        elif not folder.name.startswith("ps-"):
            add(
                rel,
                f"folder `{folder.name}` is not the `pstack` router and does not start with `ps-`",
                f"rename the folder to `ps-{folder.name}` and set name to match",
            )
        elif isinstance(name, str) and name != folder.name:
            pass
        desc = data.get("description")
        prefix = f"v{version}."
        if not isinstance(desc, str) or not desc:
            add(rel, "description is missing", f"set description to a string starting with `{prefix}`")
        elif not desc.startswith(prefix):
            add(rel, f"description does not start with `{prefix}`", f"prefix the description with `{prefix}`")
        meta = data.get("metadata")
        got = meta.get("version") if isinstance(meta, dict) else None
        if got != version:
            shown = got if isinstance(got, str) and got else "missing"
            add(rel, f"metadata.version is `{shown}`", f'set `metadata.version: "{version}"`')
        license_value = data.get("license")
        if not isinstance(license_value, str) or not license_value.strip():
            add(rel, "license is missing", "add `license: MIT`")


def skill_folder_names() -> list[str]:
    return sorted(p.name for p in SKILLS.iterdir() if p.is_dir() and p.name.startswith("ps-"))


def check_router(folders: list[str]) -> None:
    rel = "skills/pstack/SKILL.md"
    path = SKILLS / "pstack" / "SKILL.md"
    if not path.is_file():
        add(rel, "router SKILL.md is missing", "add skills/pstack/SKILL.md")
        return
    text = path.read_text(encoding="utf-8")
    known = set(folders)
    named: set[str] = set()
    for match in re.finditer(r"ps-[a-z0-9]+(?:-[a-z0-9]+)*", text):
        token = match.group(0)
        nxt = text[match.end() : match.end() + 2]
        if nxt[:1] == ".":
            continue
        if nxt == "-*" or nxt[:1] == "*":
            glob = token + ("-*" if nxt == "-*" else "*")
            prefix = token + ("-" if nxt == "-*" else "")
            hits = [name for name in folders if name.startswith(prefix)]
            if not hits:
                add(rel, f"glob `{glob}` matches no skill folder", f"name a real folder instead of `{glob}`")
            named.update(hits)
            continue
        if token not in known:
            add(rel, f"names `{token}` but skills/{token}/ does not exist", f"remove `{token}` or add skills/{token}/SKILL.md")
        else:
            named.add(token)
    for name in folders:
        if name not in named:
            add(rel, f"does not name `{name}`", f"add `{name}` to the router catalog")


def inside_repo(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT)
    except ValueError:
        return False
    return True


def link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    if " " in target:
        target = target.split()[0]
    return target.split("#", 1)[0].split("?", 1)[0].strip()


def resolves(md: Path, rel: str) -> bool:
    if not rel or rel.startswith(("#", "mailto:")):
        return True
    if re.match(r"^[a-z][a-z0-9+.-]*://", rel, re.I):
        return True
    candidates = [md.parent / rel, ROOT / rel.lstrip("./")]
    for candidate in candidates:
        resolved = candidate.resolve()
        if inside_repo(resolved) and resolved.exists():
            return True
    return False


def intended_repo_path(md: Path, rel: str) -> str:
    resolved = (md.parent / rel).resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def path_fix(md: Path, rel: str) -> str:
    intended = intended_repo_path(md, rel)
    for marker in ("docs/guide/", "docs/harness/"):
        index = intended.find(marker)
        if index >= 0:
            return UPSTREAM_DOCS + intended[index:]
    return "point it at a file that exists in this repo (relative to this file, or from the repo root)"


PACK_PREFIXES = {"references", "scripts", "playbooks", "docs", "skills", "tests", "evals"}


def is_relative_path(span: str) -> bool:
    if any(ch in span for ch in " \t\n<>*|${}[]()"):
        return False
    if span.startswith(("http://", "https://", "~", "/", "#")):
        return False
    if span.startswith(("./", "../")):
        return True
    if "/" not in span or not re.fullmatch(r"[\w.+-]+(?:/[\w.+-]+)+/?", span):
        return False
    return span.split("/", 1)[0] in PACK_PREFIXES


def index_filenames() -> dict[str, list[Path]]:
    found: dict[str, list[Path]] = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [name for name in dirnames if name != ".git"]
        for name in filenames:
            found.setdefault(name, []).append(Path(dirpath) / name)
    return found


def bare_unique(span: str, index: dict[str, list[Path]]) -> Path | None:
    ext = "|".join(PATH_EXT)
    if not re.fullmatch(rf"[\w.+-]+\.(?:{ext})", span):
        return None
    hits = index.get(span) or []
    if len(hits) == 1:
        return hits[0]
    return None


def mask_fences(text: str) -> str:
    return re.sub(r"```.*?```", lambda match: " " * len(match.group(0)), text, flags=re.S)


def markdown_files_for_paths() -> list[Path]:
    files = list(SKILLS.glob("*/SKILL.md"))
    files.extend(SKILLS.glob("*/references/*.md"))
    return sorted(files)


def check_paths(rules: set[tuple[str, str]], index: dict[str, list[Path]]) -> None:
    link_re = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    code_re = re.compile(r"`([^`\n]+)`")
    for path in markdown_files_for_paths():
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for match in link_re.finditer(text):
            target = link_target(match.group(1))
            if not target or target.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*://", target, re.I):
                continue
            if target.startswith("mailto:"):
                continue
            if allowed(rel, target, rules) or resolves(path, target):
                continue
            add(rel, f"link `{target}` does not resolve to a file", path_fix(path, target))
        masked = mask_fences(text)
        for match in code_re.finditer(masked):
            span = match.group(1)
            if allowed(rel, span, rules) or resolves(path, span):
                continue
            unique = bare_unique(span, index)
            if is_relative_path(span):
                add(rel, f"path `{span}` does not resolve to a file", path_fix(path, span))
            elif unique is not None:
                dest = unique.relative_to(ROOT).as_posix()
                add(rel, f"path `{span}` does not resolve to a file", f"point it at `{dest}`")


def ids_and_shorts(folders: list[str]) -> tuple[list[str], dict[str, str]]:
    ids = [name[3:] for name in folders]
    id_set = set(ids)
    shorts: dict[str, str] = {}
    for skill_id in ids:
        if not skill_id.startswith("principle-"):
            continue
        short = skill_id[len("principle-") :]
        if short and short not in id_set:
            shorts[short] = skill_id
    ids.sort(key=len, reverse=True)
    return ids, shorts


def check_unprefixed(folders: list[str], rules: set[tuple[str, str]]) -> None:
    ids, shorts = ids_and_shorts(folders)
    if not ids:
        return
    ident = "(?:" + "|".join(re.escape(skill_id) for skill_id in ids) + ")"
    wrapped = rf"(?:\*\*{ident}\*\*|`{ident}`|{ident})"
    patterns: list[tuple[re.Pattern[str], str]] = [
        (re.compile(rf"(?<![\w-])the ({wrapped}) skill"), "ps"),
        (re.compile(rf"(?<![\w:/])/({ident})(?![\w-])"), "slash"),
        (re.compile(rf"(?i)(?<![A-Za-z0-9_-])(?:run|use) ({wrapped})(?![\w-])"), "ps"),
        (re.compile(rf"(?<![\w/.-])`({ident})`(?![\w-])"), "tick"),
        (re.compile(rf"\*\*({ident})\*\*"), "bold"),
        (re.compile(rf"(?<![\w-])\+ ({ident})(?![\w-])"), "plus"),
    ]
    if shorts:
        short_alt = "(?:" + "|".join(re.escape(name) for name in sorted(shorts, key=len, reverse=True)) + ")"
        patterns.append((re.compile(rf"\*\*({short_alt})\*\*"), "short"))
    for path in sorted(SKILLS.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        hits: list[tuple[int, int, str, str]] = []
        for pattern, kind in patterns:
            for match in pattern.finditer(text):
                window = text[max(0, match.start() - 12) : match.start()]
                if "://" in window:
                    continue
                span = match.group(0)
                if allowed(rel, span, rules):
                    continue
                hits.append((match.start(), match.end(), span, kind + ":" + match.group(1)))
        hits.sort(key=lambda item: (item[0], -(item[1] - item[0])))
        cursor = -1
        for start, end, span, payload in hits:
            if start < cursor:
                continue
            cursor = end
            kind, captured = payload.split(":", 1)
            captured = captured.strip("`").replace("**", "")
            if kind == "short":
                full = "ps-" + shorts[captured]
            elif kind == "slash":
                full = "/ps-" + captured
            else:
                full = "ps-" + captured
            add(rel, f"unprefixed skill ref `{span}`", f"rename to `{full}`")


def check_install_lean(folders: list[str]) -> None:
    total = 0
    known = set(folders)
    for path in sorted(SKILLS.rglob("*")):
        if path.is_dir() and path.name in {"test", "tests"}:
            skill = next((part for part in path.relative_to(SKILLS).parts if part in known or part == "pstack"), path.parts[-2])
            rel = path.relative_to(ROOT).as_posix()
            add(rel, f"`{path.name}/` directory under skills/", f"move to tests/upstream-{skill}/")
        if not path.is_file():
            continue
        size = path.stat().st_size
        total += size
        if size > MAX_FILE:
            skill = path.relative_to(SKILLS).parts[0]
            rel = path.relative_to(ROOT).as_posix()
            add(rel, f"file is {size} bytes (>512KB)", f"move to tests/upstream-{skill}/")
    if total >= MAX_TREE:
        add("skills", f"total size {total} bytes is not under 2MB", "move bulky files to tests/upstream-<id>/")


def check_roles() -> None:
    agents = ROOT / "AGENTS.md"
    setup = SKILLS / "ps-setup-pstack" / "SKILL.md"
    if not agents.is_file():
        add("AGENTS.md", "AGENTS.md is missing", "restore AGENTS.md")
        return
    if not setup.is_file():
        add("skills/ps-setup-pstack/SKILL.md", "setup skill is missing", "add skills/ps-setup-pstack/SKILL.md")
        return
    setup_text = setup.read_text(encoding="utf-8")
    labels: list[str] = []
    for line in agents.read_text(encoding="utf-8").splitlines():
        if "role label" not in line.lower():
            continue
        for match in re.finditer(r"`([^`]+)`", line):
            label = match.group(1)
            if label == "ps-setup-pstack" or label.startswith(("ps-", "/")):
                continue
            labels.append(label)
    # A short AGENTS.md may name no roles.
    if not labels:
        return
    for label in labels:
        if label not in setup_text:
            add(
                "AGENTS.md",
                f"role label `{label}` is not in skills/ps-setup-pstack/SKILL.md",
                "use a role label from that skill's step 5 rule, or add the role there",
            )


def main() -> int:
    version_path = ROOT / "VERSION"
    if not version_path.is_file():
        add("VERSION", "VERSION file is missing", "add VERSION containing the pack version")
        version = ""
    else:
        version = version_path.read_text(encoding="utf-8").strip()
        if not version:
            add("VERSION", "VERSION file is empty", "write the pack version on one line")
    rules = load_allow()
    folders = skill_folder_names()
    if version:
        check_frontmatter(version)
    check_router(folders)
    check_paths(rules, index_filenames())
    check_unprefixed(folders, rules)
    check_install_lean(folders)
    check_roles()
    for line in sorted(set(FINDINGS)):
        print(line)
    return 1 if FINDINGS else 0


if __name__ == "__main__":
    sys.exit(main())
