# Obsidian interface acceptance

On 2026-11-22, launched Obsidian Desktop with a disposable Electron
profile and a copy of the Q3 replay vault from b66a90f. The CLI reported
its active target as /private/tmp/industry-obsidian-ui.5L40g8/vault.
Existing personal vaults and their settings were not part of the test.

- Obsidian indexed both markets and their four localized notes per quarter.
- Opening the smartphone Q3 overview and asking Obsidian for its outbound
  links resolved the project overview and the three quarterly substudies.
- The property search `[market:smartphones] [quarter:2024Q3] [status:partial]`
  returned exactly the four smartphone Q3 notes.
- The active-note DOM title was `2024Q3 全球智慧型手機市場-規模與市佔率`.
  The Properties widget returned type, market, quarter, status, as_of,
  and updated. The overview reported partial status, as_of 2024-11-02,
  and updated 2026-11-21.
- After the staged two-revision replay, opening the original size/share
  path in Obsidian showed the updated text and its 重要修訂 heading.
  The first revision's IDC figures and source remained in the history.
  Source wording limitations are documented in the runtime replay.

These checks exercised the desktop app's own renderer, link resolution,
and search index via its CLI. No global plugin was installed.
