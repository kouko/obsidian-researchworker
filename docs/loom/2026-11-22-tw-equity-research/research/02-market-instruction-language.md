---
title: "Should market-specific equity research instructions use local languages?"
type: loom-research
status: concluded
created: 2026-11-22
updated: 2026-11-22
change: 2026-11-22-tw-equity-research
tags: [loom/research]
---

# Should market-specific equity research instructions use local languages?

## Question and scope

Choose the authoring language of common and market-specific instructions. Treat invocation examples, original evidence and saved note language as separate choices.

## Findings

- The [existing equity skill](../../../../obsidian-finance/skills/equity-research/SKILL.md) already combines English instructions with a multilingual description. The [industry note contract](../../../../obsidian-finance/skills/industry-research/references/record.md) provides a precedent for localized note text and stable metadata.
- English throughout keeps instruction review uniform, but Taiwan-specific terms and their source labels still need original Traditional Chinese to prevent mismatches.
- Writing Taiwan-specific analytical guidance in Traditional Chinese places rules and original terminology together. English remains suitable for common storage and verification contracts and for the existing US guidance. This requires maintaining one authoritative text per market and reviewing changes in the language of that text.
- Translating all instructions into multiple languages adds parallel versions without an identified need for such duplication.

## Decision impact

Recommend English for the shared entry and common contracts, English for the US workflow, and Taiwan Traditional Chinese for Taiwan market analysis instructions and examples. Retain source labels and terms in their original language, especially when they affect accounting scope or timing. Keep machine keys and schemas stable. Choose the report language from user preference and the existing note context. This language choice applies to both independent market workflows under one entry and independent public skills.

## Limitations

This is an authoring and maintenance recommendation. No matched runs have established an accuracy or routing advantage from changing the language of the instructions.
