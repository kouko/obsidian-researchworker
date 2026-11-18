---
title: "Separate non-echoing contact input in Codex CLI"
type: loom-research
status: concluded
created: 2026-11-18
updated: 2026-11-18
change: 2026-11-18-sec-contact-setup
tags:
  - loom/research
---

# Separate non-echoing contact input in Codex CLI

## Question and scope

Can Codex CLI 0.169.0 on macOS transfer contact data separately from the command without terminal echo, then resume acquisition in the same conversation?

## Method and rationale

Run a narrow local prototype with synthetic data and an isolated home. Use the actual setup entry point and replace only the HTTP responses in acquisition. Observe terminal output and verify that the fixture checks the complete saved request identity.

## Findings

The initial nonterminal launch received EOF before receiving data. In a terminal session, the prototype disabled and checked echo before emitting its readiness marker, received a newline-terminated JSON object through a separate tool call, and piped it to the unchanged setup entry point. The command contained no contact values. Captured terminal output contained only the readiness marker and the configured status. The isolated profile had mode 0600. The same Codex conversation continued to a complete offline AAPL acquisition.

## Evidence

Codex thread `01a1ef42-eb9a-7072-bee8-963c8f24aa04` ran `python3 pty_setup.py` through a terminal and sent the payload separately. The command returned `READY_FOR_SEPARATE_INPUT`, then `{"status":"configured","exit_code":0}` (whitespace normalized). It then ran `python3 offline_acquire.py --ticker AAPL --period-start 2024-01-01 --period-end 2024-12-31 --as-of 2024-12-31 --output-dir native-pty-output` and returned complete, one eligible fact, one filing, and no errors. The prototype ran against the implementation at `b582c16`. The [plan](../plan.md) tracks the production adaptation.

The integrated script at `a0c9101` passed 286 package tests. In Codex thread `01a1ef46-9991-7670-8d31-3ad6e33964d2`, a clarified first-use prompt produced `SEC_CONTACT_REQUIRED` with no output directory entries. The response asked for contact details and explained local and host retention, but omitted the exact save path and what the header would contain in a live acquisition. After receiving the synthetic values, Codex invoked `python3 -B sec-data/scripts/acquire.py --setup-contact --terminal`, received the readiness marker and a successful status without echo, and continued the original offline operation. The acquisition returned complete, one eligible fact, one filing and no errors. All eight output files were scanned for both synthetic values, with no matches. Profile permissions were 0600.

## Decision impact

The independent test found that an invalid oversized frame could re-enable echo while its final transport chunk was still being delivered. The fix discards overflow through the terminating newline within the existing deadline. The [regression](../../../../obsidian-finance/tests/test_oversized_terminal_contact_echo.py) passed after the fix and verified that the prior profile was preserved.

Retain piped stdin for hosts that can provide it. Adapt the existing setup entry point to handle the terminal path in Codex without requiring a separate install or asking the user to configure anything.

## Limitations and open questions

The integrated verification covers the macOS Codex CLI with the skill supplied by path. It does not verify automatic skill loading or the hosted production conversation. The independent acceptance report predates the terminal change. Tool input can be retained by the host. No real contact or live SEC request was used.
