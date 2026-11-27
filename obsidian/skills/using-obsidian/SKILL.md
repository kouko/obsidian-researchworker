---
name: using-obsidian
description: Manage Obsidian vault workflows. Use when managing daily notes, setting up vaults, saving conversation summaries, starting or resuming research, creating diagrams, or cleaning up vaults. 筆記・日記・整理。ノート・日記・整理。
---

# Using Obsidian

This plugin provides daily workflow skills and vault management for Obsidian.

## When to Use

- Starting your day (daily notes, priorities)
- Setting up a new Obsidian vault
- Saving conversation summaries to vault
- Saving standalone research or starting or updating a saved research project
- Creating diagrams (Mermaid, Excalidraw, Canvas)
- Vault cleanup and organization

## Available Skills

### Daily workflow

| Skill | Purpose |
|-------|---------|
| `obsidian-daily` | Start the day — read/create daily note, surface priorities |
| `obsidian-vault-setup` | Interactive vault configurator |
| `obsidian-tldr` | Save conversation summary to vault |
| `obsidian-research` | Research a standalone topic on the web (EN + JA + the topic's own language) and write a research note to `research/` |
| `obsidian-research-project` | Start a research project or update its saved state across rounds after user confirmation |
| `obsidian-knowledge` | Search the local vault from any project (read-only); works without Grep/Glob |

### Authoring & visualization

| Skill | Purpose |
|-------|---------|
| `obsidian-markdown` | Create and edit Obsidian Flavored Markdown (wikilinks, embeds, callouts, properties) |
| `obsidian-bases` | Create and edit Bases (.base files) with views, filters, formulas |
| `obsidian-cli` | Interact with Obsidian vaults via CLI (read, create, search, plugin dev) |
| `obsidian-canvas` | Create Canvas files (MindMap/freeform layouts) |
| `obsidian-mermaid-visualizer` | Create Mermaid diagrams in vault notes |
| `obsidian-excalidraw-diagram` | Generate Excalidraw diagrams (Obsidian/Standard/Animated) |
| `dashboard-design` | Design dashboards from requirements to prototyping |
| `defuddle` | Extract web pages and YouTube transcripts using Defuddle CLI |
| `obsidian-headless` | Sync and publish vaults without the desktop app (Obsidian Headless) |
| `knap` | Render Markdown templates from JSON or CSV data |

## Available Agents

| Agent | Role | Model |
|-------|------|-------|
| `obsidian-vault-organizer` | Vault file organization, broken links, metadata cleanup | haiku |

## Quick Start

- Morning routine: invoke `obsidian-daily`
- End of session: invoke `obsidian-tldr`
- New vault: invoke `obsidian-vault-setup`
- Start or update a saved research project: invoke `obsidian-research-project`
  by itself, without opening any evidence. Use the user's wording to propose
  the round and wait for a separate confirmation before reading evidence or
  doing project work
- One-off research, including a detailed report based on supplied local
  sources: invoke `obsidian-research` and verify the requested vault before
  saving. Use `obsidian-knowledge` when the user asks to look up existing notes.
