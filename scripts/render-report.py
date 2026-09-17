#!/usr/bin/env python3
"""Turn a structured markdown (or TSV) report into self-contained HTML.

Stdlib only. Offline (system fonts). Styles what the file already contains.
Does not invent scores, gates, verdicts, or dashboard metrics.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

CSS = """
:root {
  --bg: #10110f;
  --paper: #181914;
  --ink: #efe8d6;
  --muted: #b7ad96;
  --faint: #8a8373;
  --line: #2a281f;
  --line-strong: #3d3a2e;
  --accent: #c6f135;
  --font-sans: ui-sans-serif, system-ui, "Segoe UI", sans-serif;
  --font-mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-sans);
  font-size: 17px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
.sheet { max-width: 960px; margin: 0 auto; padding: 28px 22px 80px; }
.masthead {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  border-bottom: 1px solid var(--line-strong);
  padding-bottom: 14px;
  margin-bottom: 28px;
}
.wordmark { font-weight: 700; letter-spacing: -0.02em; font-size: 13px; line-height: 1.2; }
.wordmark b { display: block; font-size: 22px; }
.wordmark span {
  color: var(--muted);
  font-family: var(--font-mono);
  font-weight: 400;
  font-size: 11px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.mast-meta {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--muted);
  text-align: right;
}
.article h1 {
  font-size: 28px;
  letter-spacing: -0.02em;
  margin: 0 0 16px;
  line-height: 1.2;
}
.article h2 {
  font-family: var(--font-mono);
  font-weight: 500;
  font-size: 13px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin: 32px 0 12px;
  color: var(--muted);
}
.article h3 { font-size: 20px; font-weight: 600; margin: 24px 0 10px; }
.article h4 { font-size: 16px; margin: 20px 0 8px; }
.article p { margin: 0 0 12px; max-width: 72ch; }
.article ul, .article ol { margin: 0 0 16px; padding-left: 1.2em; max-width: 72ch; }
.article li { margin: 0 0 8px; }
.article blockquote {
  margin: 0 0 16px;
  padding: 4px 0 4px 14px;
  border-left: 3px solid var(--accent);
  color: var(--muted);
}
hr { border: 0; border-top: 1px solid var(--line); margin: 28px 0; }
code {
  font-family: var(--font-mono);
  font-size: 0.9em;
  background: #1c1c16;
  border: 1px solid var(--line);
  padding: 0.05em 0.35em;
}
pre {
  background: #0a0a08;
  border: 1px solid var(--line-strong);
  padding: 16px 18px;
  overflow-x: auto;
  margin: 0 0 20px;
}
pre code { background: none; border: 0; padding: 0; font-size: 13.5px; line-height: 1.55; }
.table-wrap { overflow-x: auto; margin: 0 0 20px; border: 1px solid var(--line); }
table { width: 100%; border-collapse: collapse; font-size: 14px; line-height: 1.45; }
th, td {
  text-align: left;
  padding: 8px 10px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}
th {
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
  background: var(--paper);
}
.foot {
  margin-top: 48px;
  padding-top: 14px;
  border-top: 1px solid var(--line);
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--faint);
  display: flex;
  justify-content: space-between;
  gap: 12px;
}
@media (max-width: 720px) {
  .masthead { flex-direction: column; align-items: flex-start; }
  .mast-meta { text-align: left; }
}
@media print {
  body { background: #fff; color: #111; }
  .sheet { padding: 0; }
  pre, code, th { background: #fff; }
  a { color: inherit; }
}
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def inline(text: str) -> str:
    text = esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        r'<a href="\2" rel="noopener noreferrer">\1</a>',
        text,
    )
    return text


def split_cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_sep_row(cells: list[str]) -> bool:
    return bool(cells) and all(
        re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells
    )


def tsv_to_markdown(text: str) -> str:
    rows = [ln.split("\t") for ln in text.splitlines() if ln.strip()]
    if not rows:
        return "# Decision log\n\n_(empty)_\n"
    widths = max(len(r) for r in rows)
    norm = [r + [""] * (widths - len(r)) for r in rows]
    header = norm[0]
    body = norm[1:]
    lines = [
        "# Decision log",
        "",
        "| " + " | ".join(header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    return "\n".join(lines)


def first_heading(md: str) -> str:
    for line in md.splitlines():
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            return m.group(1).strip()
    return ""


def md_body_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    para: list[str] = []

    def flush_para() -> None:
        nonlocal para
        if not para:
            return
        out.append(f"<p>{inline(' '.join(para))}</p>")
        para = []

    while i < len(lines):
        line = lines[i]
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush_para()
            level = min(len(heading.group(1)), 4)
            title = heading.group(2).strip()
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            out.append(f'<h{level} id="{esc(slug)}">{inline(title)}</h{level}>')
            i += 1
            continue

        if line.startswith("```"):
            flush_para()
            fence = line[3:].strip()
            i += 1
            buf: list[str] = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            lang = f' class="lang-{esc(fence)}"' if fence else ""
            out.append(f"<pre{lang}><code>{esc(chr(10).join(buf))}</code></pre>")
            continue

        if line.lstrip().startswith("|"):
            flush_para()
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = split_cells(lines[i])
                if not is_sep_row(cells):
                    rows.append(cells)
                i += 1
            if rows:
                thead = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
                body = []
                for row in rows[1:]:
                    body.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
                out.append(
                    "<div class='table-wrap'><table><thead><tr>"
                    + thead
                    + "</tr></thead><tbody>"
                    + "".join(body)
                    + "</tbody></table></div>"
                )
            continue

        ul = re.match(r"^[-*]\s+(.+)$", line)
        ol = re.match(r"^\d+\.\s+(.+)$", line)
        if ul or ol:
            flush_para()
            ordered = bool(ol)
            tag = "ol" if ordered else "ul"
            items: list[str] = []
            while i < len(lines):
                um = re.match(r"^[-*]\s+(.+)$", lines[i])
                om = re.match(r"^\d+\.\s+(.+)$", lines[i])
                if ordered and om:
                    items.append(f"<li>{inline(om.group(1))}</li>")
                elif not ordered and um:
                    items.append(f"<li>{inline(um.group(1))}</li>")
                else:
                    break
                i += 1
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue

        if line.startswith(">"):
            flush_para()
            quote: list[str] = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i][1:].strip())
                i += 1
            out.append(f"<blockquote><p>{inline(' '.join(quote))}</p></blockquote>")
            continue

        if re.fullmatch(r"-{3,}|_{3,}|\*{3,}", line.strip()):
            flush_para()
            out.append("<hr>")
            i += 1
            continue

        if not line.strip():
            flush_para()
            i += 1
            continue

        para.append(line.strip())
        i += 1

    flush_para()
    return "\n".join(out)


def load_markdown(src: Path) -> str:
    raw = src.read_text(encoding="utf-8")
    if src.suffix.lower() == ".tsv":
        return tsv_to_markdown(raw)
    return raw


def render_html(md: str, source_name: str) -> str:
    title = first_heading(md) or source_name
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="sheet">
    <header class="masthead">
      <div class="wordmark"><b>pstack</b><span>skills report</span></div>
      <div class="mast-meta">{esc(source_name)}</div>
    </header>
    <div class="article">
      {md_body_html(md)}
    </div>
    <footer class="foot">
      <span>pstack-skills</span>
      <span>markdown + html · no invented scores</span>
    </footer>
  </main>
</body>
</html>
"""


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print("usage: render-report.py INPUT.md|INPUT.tsv [OUTPUT.html]", file=sys.stderr)
        return 2
    src = Path(argv[1])
    if not src.is_file():
        print(f"error: report not found: {src}", file=sys.stderr)
        return 1
    dest = Path(argv[2]) if len(argv) > 2 else src.with_suffix(".html")
    try:
        md = load_markdown(src)
        dest.write_text(render_html(md, src.name), encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(str(dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
