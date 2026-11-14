# Attribution

This document summarizes third-party components bundled or adapted in
`obsidian-researchworker`, extracted from `monkey-skills`. All components are MIT-licensed; their copyright notices
and license texts are preserved in the per-component `LICENSE` files
listed below.

See [`LICENSE`](LICENSE) for the overall project license (MIT,
Copyright (c) 2026 kouko).

## Third-Party Imports

### Obsidian skills from Steph Ango (kepano)

Upstream: [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills)
License: MIT, Copyright (c) 2026 Steph Ango

| Component | License file |
|-----------|-------------|
| `obsidian/skills/defuddle/` | [LICENSE](obsidian/skills/defuddle/LICENSE) |
| `obsidian/skills/obsidian-markdown/` | [LICENSE](obsidian/skills/obsidian-markdown/LICENSE) |
| `obsidian/skills/obsidian-bases/` | [LICENSE](obsidian/skills/obsidian-bases/LICENSE) |
| `obsidian/skills/obsidian-cli/` | [LICENSE](obsidian/skills/obsidian-cli/LICENSE) |

### Obsidian visual skills from Axton Liu (axtonliu)

Upstream: [`axtonliu/axton-obsidian-visual-skills`](https://github.com/axtonliu/axton-obsidian-visual-skills)
License: MIT, Copyright (c) 2025 Axton Liu

| Component | License file | Notes |
|-----------|-------------|-------|
| `obsidian/skills/obsidian-canvas/` | [LICENSE](obsidian/skills/obsidian-canvas/LICENSE) | Combines Axton Liu's canvas creator with kepano's json-canvas integration |
| `obsidian/skills/obsidian-excalidraw-diagram/` | [LICENSE](obsidian/skills/obsidian-excalidraw-diagram/LICENSE) | |
| `obsidian/skills/obsidian-mermaid-visualizer/` | [LICENSE](obsidian/skills/obsidian-mermaid-visualizer/LICENSE) | |

## Upstream historical context (not shipped here)

The following inventory describes the upstream `monkey-skills` project, not
components or runtime dependencies bundled in `obsidian-researchworker`.
Upstream paths and attribution context are retained for reference.

### skill-creator-advance and skill-judge

In upstream Monkey Skills, these adapted components are maintained under
`skill-dev-toolkit/` after the Loom plugins moved to an independent repository.
Their upstream licenses and notices are retained there at the component paths.

| Component |
|-----------|
| `skill-dev-toolkit/skills/skill-creator-advance/` |
| `skill-dev-toolkit/skills/skill-judge/` |

### repo-wiki plugin (conceptual derivation, no code imported)

Upstream `repo-wiki/` adapts the conceptual pattern from these prior works.
Its implementation is original to Monkey Skills; that plugin is not shipped
here. Credited here for transparency on upstream intellectual lineage:

- [Andrej Karpathy — LLM Wiki Pattern (2024)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — conceptual root: synthesize at ingest time, not query time; AI-owned wiki layer separate from immutable raw layer
- [`SamurAIGPT/llm-wiki-agent`](https://github.com/SamurAIGPT/llm-wiki-agent) — `raw/ → wiki/` directory pattern, ingest/query SKILL.md split, page-type taxonomy reference
- [`llmrix/llm-wiki-skill`](https://github.com/llmrix/llm-wiki-skill) — SKILL.md frontmatter and step-numbered workflow style reference

`repo-wiki`'s additions over these prior works: git-aware seed (init), polymorphic ingest (git/context/doc-import), verification triggers T1-T7 with segmented output, entity name normalization rule, hidden `.repo-wiki/` directory convention, CLAUDE.md drop-in for AI-owned enforcement.

### Other original upstream components

The following absent components are original to Monkey Skills, under its
overall MIT license:

- `domain-teams/` — entire plugin (planning / code / docs / qa / devops / design / research / copywriting / skill team skills)
- `philosophers-toolkit/` — entire plugin
- `repo-wiki/` — entire plugin (init / ingest / query skills + templates; conceptual lineage credited above)

### Upstream external runtime dependency (not shipped here)

- `feature-dev:code-architect` — Anthropic official plugin, dependency of upstream `domain-teams:code-team` (not embedded; upstream users install the `feature-dev` plugin separately)

## Original Obsidian Work (transferred from Monkey Skills)

The following transferred components were authored under Monkey Skills'
overall MIT license, whose notice is retained in this repository:

- `obsidian/skills/using-obsidian/` — router
- `obsidian/skills/obsidian-daily/` — daily workflow
- `obsidian/skills/obsidian-vault-setup/` — vault configurator
- `obsidian/skills/obsidian-tldr/` — conversation summary saver
- `obsidian/skills/obsidian-file-intel/` — file content extractor
- `obsidian/skills/dashboard-design/` — dashboard design workflow

## Reporting License Issues

If you believe a component is incorrectly attributed or a license notice
is missing, please open an issue at
https://github.com/kouko/obsidian-researchworker/issues.
