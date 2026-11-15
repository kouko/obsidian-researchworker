# obsidian

[English](README.md) | **日本語** | [繁體中文](README.zh-TW.md)

> Obsidian vault workflow — daily note、markdown、Bases、図、Canvas、file intel、vault 管理、ダッシュボード設計を Claude Code plugin としてパッケージ化。

## ⚠️ Cowork 互換性

本 plugin の skill のほとんどは Cowork 互換だが、`defuddle` skill のみ例外。
[Defuddle CLI](https://github.com/kepano/defuddle) を subprocess で呼び出して
外部 URL を取得・整形するため、Cowork の sandbox URL allowlist に block される。
`defuddle` は Claude Code CLI で利用すること。これらは upstream の互換性情報であり、
独立版の Claude/Cowork 互換性は未検証。[検証記録](../docs/verification.md)には
過去の Codex ローカルソース導入成功のみを記録し、実利用は未達。

| Skill | Cowork | Claude Code CLI |
|---|---|---|
| `defuddle` | block（URL fetch） | 動作 |
| その他すべての obsidian skill | 動作 | 動作 |

## Version

4.2.0 — [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) を参照。

Vault 初期設定は、個人に合わせた命名・ノート品質・現行 skill の規則を
`AGENTS.md` にまとめ、`CLAUDE.md` は `@AGENTS.md` と末尾の改行だけにする。
既存の両ファイルを読み、復元可能な非公開バックアップを取ってから統合する。
既存の memory とローカル skill は変更せず、不足ファイルの作成は preview の
明示的な承認が必要。個人の規則とバックアップはローカルに保持する。
Codex の探索と Claude の import は互換性の方針であり、新規 session での
読み込みは未検証。global 設定や cache は自動変更しない。
別管理の OpenCode package は 0.2.0。

## 独立配布

[Monkey Skills](https://github.com/kouko/monkey-skills) から抽出し、
[Obsidian ResearchWorker](../README.md) で独立管理する。
plugin 名 `obsidian` は保持する。4.0.0 は 14 skill を提供し、8 つの wiki skill と
daily-news-digest を削除する。通常の daily note、単一テーマの研究、Defuddle 抽出、
wikilink は保持し、既存 vault の出力や設定は変更しない。切り替え前に
[移行ガイド](../docs/migration.md)を確認すること。[検証記録](../docs/verification.md)の
記録リビジョンでは隔離した Codex ローカルソース導入に成功したが、skill 実行と
ノート作成は未達。他 host とリモート導入は未検証。
4.2.0 で `obsidian-knowledge` に改名し、同梱の読み取り専用シェルスクリプトで検索する（編集の Grep/Glob は不要。skill 数は 15 のまま）。

## 背景

Obsidian は local-first な markdown knowledge base。日常の vault 作業は小さい
反復タスクの集合になる：今日の daily note を開く、inbox を整理する、
有効な Bases YAML を書く、note 内に Mermaid 図を描く、PDF フォルダを
要約 note としてインポートする、session 終了時に会話の要約を保存する。

本 plugin はそれらのタスクを skill としてパッケージ化し、Claude Code が
intent に応じて dispatch する。Original skill は daily workflow / file intel /
ダッシュボード設計 / vault setup / 会話要約をカバー。Import 済 skill は
Obsidian 固有の markdown / Bases / Obsidian CLI / Defuddle web 抽出 /
Canvas 作成 / Excalidraw 図 / Mermaid 図をカバー。

## Router と agent

### Router

`using-obsidian` が entry skill。ユーザーの依頼内容（daily note、vault setup、
file processing、図、cleanup など）に応じて適切な skill に routing する。

slash command は `/using-obsidian` で呼び出す。

### Agent

`obsidian-vault-organizer` は vault 保守用 agent。定期的な hygiene 作業
（`inbox/` の振り分け、broken wikilink の修復、frontmatter 正規化、
重複候補の検出、tag 名の統一）を担当する。**ファイルは削除しない** —
move か edit のみ。振り分け先が曖昧な場合は確認を取る。

## Skills

### Original skill（this project）

| Skill | 用途 |
|---|---|
| `using-obsidian` | Router — vault workflow の intent を適切な skill に routing |
| `obsidian-daily` | 今日の daily note を読み込み or 作成、`inbox/` を sweep、上位 3 priority を提示 |
| `obsidian-vault-setup` | 対話型 vault 初期設定 — 自由記述の回答から role と scope を推定 |
| `obsidian-tldr` | 会話の要約を vault に保存し、`memory.md` を更新 |
| `obsidian-research` | トピックを web 調査（英語＋日本語、テーマ固有の言語があればそれを主に追加）し、目次付きの研究ノートを `research/` に保存 |
| `obsidian-knowledge` | 任意の project からローカル vault を検索（読み取り専用）。SessionStart hook が各 session に vault の場所を伝える。Grep/Glob 不要 |
| `obsidian-file-intel` | PDF / PPTX / XLSX / DOCX / CSV / JSON を Gemini で抽出し、Obsidian-ready な要約を生成 |
| `dashboard-design` | デジタル庁ダッシュボード設計ガイドラインに基づき、要件整理から layout までを引導 |

### kepano（Steph Ango）からの import

Upstream: [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills)
— MIT, Copyright (c) 2026 Steph Ango。

| Skill | 用途 |
|---|---|
| `obsidian-markdown` | Obsidian Flavored Markdown の作成 — wikilink、embed、callout、properties、コメント |
| `obsidian-bases` | `.base` ファイルの作成・編集 — view、filter、formula、summary |
| `obsidian-cli` | 起動中の Obsidian instance を公式 CLI で操作 — read、create、search、plugin / theme 開発 |
| `defuddle` | Defuddle CLI で web ページと YouTube の文字起こしを抽出 |

### axtonliu（Axton Liu）からの import

Upstream: [`axtonliu/axton-obsidian-visual-skills`](https://github.com/axtonliu/axton-obsidian-visual-skills)
— MIT, Copyright (c) 2025 Axton Liu。

| Skill | 用途 |
|---|---|
| `obsidian-canvas` | Obsidian Canvas ファイルを MindMap / freeform layout で作成。さらにカンバン／ダッシュボード（ホームページ）／研究マップ／ムードボードの 4 つのコミュニティパターンとテンプレート、`.canvas` 出力検証スクリプト、そしてプラグインなしで使える応用パターン（ネストキャンバス／研究デュアルキャンバス／データパイプラインの文書化／監査・ポストモーテム・オンボーディング／教師用クラスキャンバス／ワールドビルディング／Bases-in-canvas 1.9+／canvas-only／2D MOC）に対応（kepano の json-canvas integration を統合） |
| `obsidian-excalidraw-diagram` | Excalidraw 図を Obsidian / Standard / Animated 形式で生成 |
| `obsidian-mermaid-visualizer` | Mermaid 17 図種（flow / data-viz / structural / time）— Obsidian 11.4.1 最適化、GitHub / Notion / HackMD にも portable |

## Install

独立版の導入実績は[検証記録](../docs/verification.md)にある過去の隔離 Codex
ローカルソース導入のみ。リモート導入、Claude/Cowork 互換性、実利用は未検証。
既存の導入を変更する前に[移行ガイド](../docs/migration.md)を確認すること。

`defuddle` skill は Defuddle CLI が必要：

```bash
npm install -g defuddle
```

`obsidian-cli` skill は公式 Obsidian CLI と起動中の Obsidian instance が必要 —
[help.obsidian.md/cli](https://help.obsidian.md/cli) 参照。

`obsidian-file-intel` skill は vault 内の外部互換スクリプト
`scripts/process_files_with_gemini.py` と、設定済の Gemini API key が必要。
スクリプトは同梱されず、取得・セットアップ手順も本配布にはない。
既存の互換スクリプトがなければ処理は利用できず、独立版での設定と実行は未検証。

`obsidian-knowledge` skill は他の project から vault を読む。SessionStart hook
（`hooks/hooks.json`）が session 開始時に vault のパスを出力する。検索は同梱の `skills/obsidian-knowledge/scripts/vault.sh`（POSIX sh。Obsidian 起動中は CLI、それ以外は BSD grep）を使う — macOS で Python も Grep/Glob も不要。vault の読み取りで
許可確認が出る場合は、`~/.claude/settings.json` → `permissions.allow` に読み取り
ルールを 1 行追加する（例：`Read(~/Documents/MyVault/**)`）。skill が正確な行を示し、
同意を得てから追加する。プライバシー：skill が読んだノート本文はモデル提供者に送信
される。対応状況：Claude Code の macOS は検証済、Linux は未検証、Windows は非対応。

## Usage

一日を始める：

```
> Start my day
```

`using-obsidian` が `obsidian-daily` に route。`daily/YYYY-MM-DD.md` を
読み込み or 作成し、`inbox/` の項目を列挙、上位 3 priority を提示する。

session 終了時に会話の要約を保存：

```
> Save a TLDR of this conversation
```

`using-obsidian` が `obsidian-tldr` に route。関連フォルダに markdown 要約を
書き込み、`memory.md` を更新する。

note 内に図を描く：

```
> OAuth device flow の Mermaid sequence 図を作って
```

`using-obsidian` が `obsidian-mermaid-visualizer` に route。sequence diagram type
を選択し、Obsidian 11.4.1 quirk を適用、` ```mermaid ` ブロックを出力する。

## Repository 構造

```
obsidian/
├── .claude-plugin/
│   └── plugin.json              # plugin metadata、version 4.2.0
├── agents/
│   └── obsidian-vault-organizer.md  # vault 保守 agent
├── hooks/                       # SessionStart vault pointer
├── skills/
│   ├── README.md                # skill 別 attribution 表
│   ├── using-obsidian/          # router（original）
│   ├── obsidian-daily/          # daily workflow（original）
│   ├── obsidian-vault-setup/    # vault 初期設定（original）
│   ├── obsidian-tldr/           # 会話要約（original）
│   ├── obsidian-research/       # web research → vault note（original）
│   ├── obsidian-knowledge/      # 読み取り専用 vault 検索（original）
│   ├── obsidian-file-intel/     # ファイル → Obsidian 要約（original）
│   ├── dashboard-design/        # ダッシュボード設計（original）
│   ├── obsidian-markdown/       # kepano から import
│   ├── obsidian-bases/          # kepano から import
│   ├── obsidian-cli/            # kepano から import
│   ├── defuddle/                # kepano から import
│   ├── obsidian-canvas/ # axtonliu から import
│   ├── obsidian-excalidraw-diagram/ # axtonliu から import
│   └── obsidian-mermaid-visualizer/ # axtonliu から import
├── README.md
├── README.ja.md
└── README.zh-TW.md
```

skill 別の attribution は [`skills/README.md`](skills/README.md)、
repo 全体の attribution は [`../ATTRIBUTION.md`](../ATTRIBUTION.md) を参照。

## 貢献

- bug 報告・機能要望：
  [github.com/kouko/obsidian-researchworker/issues](https://github.com/kouko/obsidian-researchworker/issues)
  に issue を開いてください。
- PR 歓迎。既存の skill 構造（frontmatter + workflow + reference ファイル）に
  合わせ、Conventional Commits を使うこと。
- import 済 skill については、kepano / axtonliu 上流からの変更が流れてくる。
  上流に該当する修正は upstream PR の検討も推奨。

## License

MIT — 詳細は repository root の [LICENSE](../LICENSE) を参照。

import 済 skill は各 skill の `LICENSE` ファイルに原著作権表示を保持：

- `defuddle`、`obsidian-bases`、`obsidian-cli`、`obsidian-markdown` — MIT,
  Copyright (c) 2026 Steph Ango。各 skill 配下の `LICENSE` 参照。
- `obsidian-canvas`、`obsidian-excalidraw-diagram`、
  `obsidian-mermaid-visualizer` — MIT, Copyright (c) 2025 Axton Liu。
  各 skill 配下の `LICENSE` 参照。（`obsidian-canvas` は kepano 由来の
  json-canvas integration も同梱。）

プロジェクト全体の license は [LICENSE](../LICENSE)、third-party コンポーネント
全体は [ATTRIBUTION.md](../ATTRIBUTION.md) を参照。
