# pstack-skills

pstack-skills is an installable Agent Skills pack. The parent router is `pstack`. Each leaf folder is `ps-*`.
Upstream origin is the **Cursor pstack plugin** (poteto / Lauren Tan).
That plugin is not an official public GitHub repo yet.
Skill text, playbooks, and principles in this pack are a port of those Desktop leaves — names rewritten to `ps-*`, meaning preserved.
This repository (`pedroknigge/pstack-skills`) is the **public port** by Pedro Knigge.
Do not treat it as a poteto or Cursor release.
Packaging for this repo is MIT, Copyright (c) 2026 Pedro Knigge.
See [LICENSE](LICENSE).
Do not strip license or attribution from skill text.
[MIT](LICENSE)

## Install

Install for every detected agent, in all projects:

```bash
npx skills add pedroknigge/pstack-skills -g -y
```

`-g` installs globally. Omit `-g` to install into the current repo only. `-y` skips prompts.

`./install.sh` copies every folder under `skills/` into each agent skill directory that exists on this machine. The default scope is your home directory.

```bash
./install.sh
./install.sh --project
./install.sh --uninstall
```

Antigravity needs the agent names on the command:

```bash
npx skills add pedroknigge/pstack-skills -g -y -a antigravity -a antigravity-cli
```

Update a global install with `npx skills update pstack-skills -g -y`. After a release, follow [docs/release-checklist.md](docs/release-checklist.md).

## Invoke

Use `/pstack` or `/ps` when you have not named a leaf. Use `/ps-<slug>` when you have. Routing for every leaf is [skills/pstack/SKILL.md](skills/pstack/SKILL.md).

## Feature map

Runtime proofs are [docs/feature-map.md](docs/feature-map.md). Run them with `bash scripts/verify-pack.sh`.

## Version

The pack version is the `VERSION` file (`0.0.5`). History is [CHANGELOG.md](CHANGELOG.md).

## Report an issue

Search open issues, then file on [pedroknigge/pstack-skills](https://github.com/pedroknigge/pstack-skills) only after you confirm in the same turn.

```bash
scripts/ps-issue.sh --search "short query"
scripts/ps-issue.sh --title "short title" --label bug --body "what broke" --dry-run
```

The procedure is [skills/pstack/references/issue.md](skills/pstack/references/issue.md).
