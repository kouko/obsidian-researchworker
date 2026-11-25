# Installation, updates and transition

The `obsidian` 5.0.0 package provides 15 skills. The independently installable
`obsidian-finance` 0.2.0 package provides four skills, including
`tw-equity-research`. The Obsidian release retires File Intel and the generated
OpenCode slash commands. All remaining skill definitions and bundled resources
are available in their respective packages.

The following routes describe installation of the candidate release. See
[Verification status](#verification-status) for actual host evidence. Select
only the packages you need.

## Obtain a local source checkout

For Claude Code, Codex and Antigravity CLI, clone the source and identify its
absolute path. For a candidate release, check out the intended commit in a
separate clone before registering the marketplace or package.

```sh
git clone https://github.com/kouko/obsidian-researchworker.git
cd obsidian-researchworker
researchworker_root="$(pwd -P)"
```

## Claude Code

Register the repository as the `obsidian-researchworker` marketplace and
install either or both plugins at the desired scope. This example uses user
scope.

```sh
claude plugin marketplace add "$researchworker_root"
claude plugin install obsidian@obsidian-researchworker --scope user
claude plugin install obsidian-finance@obsidian-researchworker --scope user
claude plugin list
```

To update, bring the checkout to the desired release revision, refresh its
marketplace metadata, and update installed plugins at their existing scope.

```sh
claude plugin marketplace update obsidian-researchworker
claude plugin update obsidian@obsidian-researchworker --scope user
claude plugin update obsidian-finance@obsidian-researchworker --scope user
```

## Codex

Use the same local checkout as the marketplace source.

```sh
codex plugin marketplace add "$researchworker_root"
codex plugin add obsidian@obsidian-researchworker
codex plugin add obsidian-finance@obsidian-researchworker
codex plugin list --marketplace obsidian-researchworker
```

To update a locally registered marketplace, bring the checkout to the desired
release revision and repeat the install commands for the selected plugins.

```sh
codex plugin add obsidian@obsidian-researchworker
codex plugin add obsidian-finance@obsidian-researchworker
codex plugin list --marketplace obsidian-researchworker
```

For a marketplace registered from a Git URL or repository instead, first run
`codex plugin marketplace upgrade obsidian-researchworker` to refresh its
snapshot. The upgrade command applies only to Git registrations.

Verify the installed versions separately. If the catalog changes but a selected
plugin still has older installed contents, refresh that plugin using the host's
plugin interface. Restart the session before checking available skills.

## Antigravity CLI

The Antigravity CLI (`agy`) uses its Claude-plugin conversion to install from
each local package directory. Check the existing plugin list first so that an
imported or already-installed copy is identified before an installation replaces
it.

```sh
agy plugin list
agy plugin install "$researchworker_root/obsidian"
agy plugin install "$researchworker_root/obsidian-finance"
agy plugin list
```

To update, bring the source checkout to the desired release revision, then
repeat the install commands for the packages you use. Start a fresh session
with your intended workspace attached by absolute path where needed. This guide
targets the CLI. Desktop and IDE behavior are outside the verification scope.

## OpenCode

Use OpenCode v2. Configure either or both package targets in the `plugins`
array of the host's `opencode.json` (for example,
`~/.config/opencode/opencode.json` on macOS). Preserve other existing config
entries.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    "github:kouko/obsidian-researchworker#main::path:obsidian",
    "github:kouko/obsidian-researchworker#main::path:obsidian-finance"
  ]
}
```

For pre-release local testing, replace the selected Git targets in an
isolated OpenCode configuration with the corresponding absolute package
directory paths, for example:

```json
{
  "plugins": [
    "/absolute/path/to/obsidian-researchworker/obsidian",
    "/absolute/path/to/obsidian-researchworker/obsidian-finance"
  ]
}
```

Restart OpenCode's service and inspect the plugin and skill registries in the
intended workspace. For updates to a Git target, update to the desired release
commit by replacing `main` in the target with that commit ID, then restart.
A configured branch target may reuse cached contents, so check the actual source
revision and registered skills after refreshing.

The skills retain their package namespaces. In OpenCode:

- Select `@obsidian:obsidian-research` or `@obsidian-finance:tw-equity-research`
  using the native skill selection interface.
- For automatic selection, describe the actual task. OpenCode advertises
  permitted skills with descriptions to the model, and the model decides when
  to load them using its native skill tool. Permission settings can restrict
  discovery or loading.
- Supporting files remain in each installed package and can be read as the
  skill directs. They are not all loaded automatically.

The old generated slash command `/obsidian:using-obsidian` is retired; use
`@obsidian:using-obsidian`. Other plugins' commands and native OpenCode
commands are independent of this change. See the [official OpenCode skill
documentation](https://opencode.ai/docs/skills/) for selection and permission
details.

## Verification status

Candidate release verification on November 25, 2026 used isolated host configurations. Claude Code 2.1.332 and Codex 0.172.0 installed both local marketplace packages with 15 and 4 skill files. Antigravity CLI 1.5.16 converted both Claude plugins and reported the complete inventories. Local update tests also advanced both packages from the previous release versions using the commands above. OpenCode 2.4.1 loaded both local package directories, registered 19 namespaced skills, and registered no generated package commands; its TUI offered and completed both example @ mentions without submitting a prompt.

Model-backed automatic selection and skill execution, remote Git installation of the candidate, live-vault writes, and global installation refresh were not verified. See the [verification record](verification.md) for earlier host evidence.

After installing or updating, check that the selected package is enabled, its
version matches the source metadata, and the complete corresponding skill
inventory is available in a fresh session. The combined OpenCode inventory
should contain the 15 `obsidian:` skills and the four `obsidian-finance:`
skills, without generated slash commands from these packages. Scope this check
to these packages so unrelated skills and commands are not counted.

## Migration from Monkey Skills or older releases

ResearchWorker was extracted from Monkey Skills. The historical Obsidian 4.0.0
release removed the eight wiki skills and daily-news-digest; 4.2.0 renamed local
search to `obsidian-knowledge`. Existing general daily notes, topic research,
Defuddle extraction and ordinary wikilinks remain. File Intel was subsequently
retired. Obsidian 5.0.0 unifies the release versions across its distribution
metadata.

The retained plugin name is `obsidian`. In OpenCode, update saved references
from the former `obsidian-researchworker:<skill>` or earlier
`monkey-skills-obsidian:*` prefix to the native `@obsidian:<skill>` form.
Finance uses its own `obsidian-finance:<skill>` IDs.

Check existing registrations before replacing an installed copy. Two copies with
the same plugin name can cause duplicate skills, ambiguous routing or cache
collisions. Preserve the current registration and settings, switch the intended
plugin source, and check one active copy in a fresh session. Rollback restores
the previous registration and disables the replacement. Installation,
replacement and rollback do not require deleting or migrating vault data.
Existing notes, prior wiki/news outputs, scripts and settings remain local.
