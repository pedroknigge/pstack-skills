#!/usr/bin/env python3
"""Pack conventions for pstack-skills 0.0.1 — no invented skill verbs."""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SCRIPTS = ROOT / "scripts"
PARENT_SCRIPTS = SKILLS / "pstack" / "scripts"
PARENT_REFS = SKILLS / "pstack" / "references"


def run(argv: list[str], env: dict[str, str] | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        argv,
        cwd=cwd or ROOT,
        env=merged,
        text=True,
        capture_output=True,
    )


class VersionLock(unittest.TestCase):
    def test_version_file(self) -> None:
        self.assertEqual((ROOT / "VERSION").read_text(encoding="utf-8").strip(), "0.0.1")

    def test_every_description_starts_with_v001(self) -> None:
        skills = sorted(SKILLS.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(skills), 48)
        bad = []
        for path in skills:
            text = path.read_text(encoding="utf-8")
            m = re.search(r'^description:\s*"([^"]+)"', text, re.M)
            if m:
                desc = m.group(1)
            else:
                folded = re.search(
                    r"^description:\s*>\s*\n\s+(\S[^\n]*)",
                    text,
                    re.M,
                )
                desc = folded.group(1) if folded else ""
            if not desc.startswith("v0.0.1"):
                bad.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(bad, [])

    def test_parent_description_keeps_issue_and_html_triggers(self) -> None:
        text = (SKILLS / "pstack" / "SKILL.md").read_text(encoding="utf-8")
        desc = re.search(r'^description:\s*"([^"]+)"', text, re.M)
        self.assertIsNotNone(desc)
        self.assertTrue(desc.group(1).startswith("v0.0.1"))
        self.assertIn("report this to pstack", desc.group(1))
        self.assertIn("sugerí mejora al skill", desc.group(1))
        self.assertIn("dogfood", desc.group(1))
        self.assertIn("blindtest", desc.group(1))
        self.assertIn("probar pstack en un repo random", desc.group(1))
        self.assertIn("HTML", desc.group(1))


class IssueModule(unittest.TestCase):
    def test_scripts_ship_with_parent(self) -> None:
        for name in ("ps-issue.sh", "render-report.py", "ps-detect-siblings.sh"):
            self.assertTrue((SCRIPTS / name).is_file(), name)
            self.assertTrue((PARENT_SCRIPTS / name).is_file(), f"parent {name}")

    def test_dry_run_create_targets_skill_repo(self) -> None:
        r = run(
            [
                str(SCRIPTS / "ps-issue.sh"),
                "--title",
                "sample enhancement",
                "--label",
                "enhancement",
                "--body",
                "A short public draft.",
                "--dry-run",
            ]
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("pedroknigge/pstack-skills", r.stdout)
        self.assertIn("gh issue create", r.stdout)
        self.assertNotIn("origin", r.stdout.lower())

    def test_search_dry_run(self) -> None:
        r = run([str(SCRIPTS / "ps-issue.sh"), "--search", "router", "--dry-run"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("gh issue list", r.stdout)
        self.assertIn("pedroknigge/pstack-skills", r.stdout)

    def test_child_cannot_submit(self) -> None:
        r = run(
            [
                str(SCRIPTS / "ps-issue.sh"),
                "--title",
                "should not post",
                "--label",
                "bug",
                "--body",
                "draft only",
                "--confirm",
            ],
            env={"PS_CHILD": "1"},
        )
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("PS_CHILD", r.stderr)

    def test_label_must_be_allowlisted(self) -> None:
        r = run(
            [
                str(SCRIPTS / "ps-issue.sh"),
                "--title",
                "x",
                "--label",
                "question",
                "--body",
                "nope",
                "--dry-run",
            ]
        )
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("dogfood", r.stderr)

    def test_dogfood_labels_dry_run(self) -> None:
        r = run(
            [
                str(SCRIPTS / "ps-issue.sh"),
                "--title",
                "router missed a leaf",
                "--label",
                "dogfood,blindtest,enhancement",
                "--body",
                "Public friction only.",
                "--dry-run",
            ]
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("--label dogfood", r.stdout)
        self.assertIn("--label blindtest", r.stdout)
        self.assertIn("--label enhancement", r.stdout)


class Bridges(unittest.TestCase):
    def test_bridge_notes_exist(self) -> None:
        for name in (
            "issue.md",
            "arkgate-bridge.md",
            "orderfield-bridge.md",
            "documentation-manager-bridge.md",
            "vibe-proof-bridge.md",
        ):
            path = PARENT_REFS / name
            self.assertTrue(path.is_file(), name)
            text = path.read_text(encoding="utf-8")
            self.assertIn("human captain", text.lower())
            if name != "issue.md":
                self.assertIn("sensor, not fusion", text.lower())
                self.assertIn("no silent auto-run", text.lower())

    def test_docs_bridge_uses_ps_names(self) -> None:
        text = (PARENT_REFS / "documentation-manager-bridge.md").read_text(encoding="utf-8")
        self.assertIn("ps-architect", text)
        self.assertIn("ps-figure-it-out", text)
        self.assertIn("parent", text.lower())
        self.assertIn("documentation-manager", text)

    def test_detect_empty_tree_is_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            r = run([str(SCRIPTS / "ps-detect-siblings.sh"), tmp])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(
            r.stdout.strip().splitlines(),
            [
                "ArkGate: none",
                "Orderfield: none",
                "Docs: none",
                "Vibe-proof: none",
            ],
        )

    def test_detect_ark_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "ark.config.json").write_text("{}\n", encoding="utf-8")
            r = run([str(SCRIPTS / "ps-detect-siblings.sh"), tmp])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("ArkGate: detected", r.stdout)


class DogfoodCycle(unittest.TestCase):
    def test_docs_and_eval_stub(self) -> None:
        cycle = (ROOT / "docs" / "dogfood-cycle.md").read_text(encoding="utf-8")
        self.assertIn("pedroknigge/pstack-skills", cycle)
        self.assertIn("blindtest", cycle)
        parent = (PARENT_REFS / "dogfood.md").read_text(encoding="utf-8")
        self.assertIn("probar pstack en un repo random", parent)
        self.assertIn("HITL", parent)
        evals = (ROOT / "evals" / "README.md").read_text(encoding="utf-8")
        self.assertIn("Planted", evals)
        self.assertIn("Live dogfood", evals)
        stub = (ROOT / "evals" / "fixtures" / "live-dogfood.stub.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("public third-party", stub)
        self.assertIn("private", stub)

    def test_parent_routes_dogfood(self) -> None:
        text = (SKILLS / "pstack" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/dogfood.md", text)
        self.assertIn("dogfood", text.lower())
        self.assertIn("blindtest", text.lower())


class HtmlRenderer(unittest.TestCase):
    def test_markdown_twin(self) -> None:
        md = "# Session summary\n\n**Status:** open\n\n- one\n- two\n\n| col | val |\n| --- | --- |\n| a | b |\n"
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "session.md"
            src.write_text(md, encoding="utf-8")
            r = run(["python3", str(SCRIPTS / "render-report.py"), str(src)])
            dest = src.with_suffix(".html")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(dest.is_file())
            html = dest.read_text(encoding="utf-8")
            self.assertIn("Session summary", html)
            self.assertIn("<table>", html)
            self.assertIn("no invented scores", html)
            self.assertNotIn("Overall score", html)

    def test_tsv_twin(self) -> None:
        tsv = "ts\tphase\tdecision\twhy\tevidence\tresult\n2026-09-17T00:00:00Z\tframe\tdid the thing\tbecause\tcommit abc\topen\n"
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "decisions.tsv"
            src.write_text(tsv, encoding="utf-8")
            r = run(["python3", str(SCRIPTS / "render-report.py"), str(src)])
            dest = src.with_suffix(".html")
            self.assertEqual(r.returncode, 0, r.stderr)
            html = dest.read_text(encoding="utf-8")
            self.assertIn("did the thing", html)
            self.assertIn("<table>", html)


if __name__ == "__main__":
    unittest.main()
