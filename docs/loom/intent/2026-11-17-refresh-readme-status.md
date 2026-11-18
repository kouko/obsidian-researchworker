# Align README release and compatibility information
originator: kouko
kind: engineering
needs-design: no — documentation wording only; no software behaviour change
status: confirmed 2026-11-17 — user approved the two documentation corrections
publication: automatic — authorized 2026-11-17 by kouko

## Problem
The root README describes 14 skills and version 4.1.0, while shipped metadata and inventory contain 15 skills at 4.2.0. English, Japanese and Traditional Chinese compatibility tables present inherited claims as working despite independent verification limits.

## Outcome and acceptance
The root overview matches the shipped inventory and version. All three compatibility tables distinguish inherited limitations, unverified behaviour and skill-specific evidence. No runtime files or user data change.

## Scope and authorization
Four README files plus this publication identification record. The user requested a branch and merge on 2026-11-17. Preserve the untracked ROADMAP-DRAFT.md. No new host verification, installation or global configuration changes.

## Verification
The package suite passed 75 tests before these README edits. The documentation diff passed git diff --check. No new functional tests, independent review or attestation were produced for this wording-only correction.
