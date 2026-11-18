# SEC contact setup — acceptance test evidence

Tried on 2026-11-18 at `f9b8deedfa95a2d3c5405d236dab00cd396daced` in fresh local clones made with `git clone --no-local` and `git checkout --detach f9b8dee`. The README's Python entry point loaded in the clone without a separate application install. Each run used an isolated HOME, synthetic contact, and either preflight without network or an injected fixture transport. No live SEC request or host conversation took place.

## 1. 缺少聯絡資料時，助理在當前對話詢問操作者或組織名稱與聯絡 email，並先說明本機保存及 SEC 用途。提供有效資料後，同一次工作可接著擷取。

- How I tried it: Ran the README command `python obsidian-finance/skills/sec-data/scripts/acquire.py --ticker AAPL --fiscal-quarter 2024Q3 --output-dir "$HOME/output"` with a missing profile. A separate offline probe invoked the same script with `--setup-contact`, using `subprocess.run(input=json.dumps(payload), ...)`, then invoked the quarter operation in a separate Python process with the committed fixtures `test_acquire.payloads`, `test_fiscal_quarter.evidence("Q3")` and `test_fiscal_quarter.declaration("Q3")` supplying all four responses.
- What came back: `SEC_CONTACT_REQUIRED` / exit 64 without creating output. The valid setup gave `setup=configured exit=0`, profile mode `0600`, and immediate replay gave `{"status": "complete", "exit": 0, "calls": 4}`.
- Evidence: Both `test_setup_cli_and_later_acquisition` and `test_quarter_package` passed. The explanation and prompt are specified in `obsidian-finance/skills/sec-data/SKILL.md` under “Configure contact on first use”; this is source evidence only.

## 2. 後續工作階段可讀取本機設定，無須重問、另裝指令或手動設定環境變數。

- How I tried it: Spawned a new acquisition process using the same isolated HOME and identical user arguments, with no second setup payload; the fixture transport asserted that all four requests used the saved contact.
- What came back: `later-process {"status": "complete", "exit": 0, "calls": 4}`.
- Evidence: `test_setup_cli_and_later_acquisition` passed. The probe creates distinct run directories; it verifies process-to-process persistence and does not establish behavior in a new host conversation.

## 3. 無效輸入會明確回報。實際聯絡資料不進入擷取輸出、研究筆記或 Git。

- How I tried it: Exercised invalid setup first and captured its output, then scanned both completed runs, captured output, and tracked files for both synthetic values. Simulated denied replacement, configuration-directory redirection and reflected response bodies with the targeted pytest cases.
- What came back: `setup=SEC_CONTACT_INVALID exit=64` with neither value echoed or saved. The independent probe reported `contact absent from 18 generated files and tracked files; clean checkout`. The save-denial test observed `SEC_CONTACT_SAVE_FAILED`, original profile bytes preserved, and no temporary file left. Tests confirmed responses matching tested synthetic values were withheld and the configuration path could not be redirected into a test vault. No host-generated research note was produced.
- Evidence: `test_invalid_setup_preserves_private_profile`, `test_denied_replace_preserves_previous_contact`, `test_reflected_contact_not_retained`, `test_config_directory_symlink_does_not_store_contact_in_vault`, and `test_single_token_contact_reflection_is_withheld` passed.

## 4. 本機設定是唯一的聯絡資料來源。只有舊環境變數時，助理會走首次設定。

- How I tried it: Reused the README command with synthetic `SEC_USER_AGENT` and no saved profile, then left that different legacy value set during both fixture-backed acquisitions.
- What came back: With only the variable, `{"status":"failed","exit_code":64,"error":"SEC_CONTACT_REQUIRED: set up a local SEC contact","run_path":null}` (whitespace normalized) and output was absent. With the profile present, the fixture verified the locally saved header on every call.
- Evidence: `test_contact_preflight_ignores_old_environment` independently asserted no requests and no output for missing, corrupt or unsafe profiles despite the legacy variable.

## 5. First-time prompt and continue flow

- How I tried it: Walked the preflight → setup → same-work replay sequence in row 1.
- What came back: The three observed codes were 64, 0, and 0. Host wording and same-conversation continuation were unobserved.
- Evidence: Row 1 commands and output.

## 6. Later-request flow

- How I tried it: Invoked the same request in a new process with the saved settings as in row 2.
- What came back: Successful offline acquisition with no further setup. Host prompting was unobserved.
- Evidence: Row 2 captured replay.

## 7. Invalid input or refused save flow

- How I tried it: Followed row 3 and checked the denial and unsafe-path tests.
- What came back: Invalid and failed-save paths were reported separately. A failed save preserved existing contact. The unsafe path prevented both storage in the target research folder and starting acquisition. Host explanation was unobserved.
- Evidence: Row 3 targeted cases and `test_symlinked_profile_directory_is_unusable_and_cannot_store_contact`.

## 8. Legacy-only first-time flow

- How I tried it: Ran row 4 with only the legacy variable.
- What came back: The entry point requested first-time setup. The following host prompt was unobserved.
- Evidence: Row 4 captured preflight and targeted tests.

## Targeted and package checks

- Targeted command: `python -m pytest obsidian-finance/tests/test_acquire.py obsidian-finance/tests/test_sec_client.py obsidian-finance/tests/test_contact_vault_symlink.py obsidian-finance/tests/test_single_token_contact_reflection.py -q -p no:cacheprovider -k 'contact or invalid_setup or traceable_package or utf8_user_agent or quarter_package'`.
- Captured result: `22 passed, 62 deselected in 4.44s`.
- README package command: `python3 -m pytest obsidian/tests obsidian-finance/tests -q -p no:cacheprovider`. The full suite is for the automated pre-acceptance check that blocks on failure. It was not run by this acceptance tester, and formal finalization is pending.
