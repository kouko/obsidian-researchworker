# obsidian

[English](README.md) | **日本語** | [繁體中文](README.zh-TW.md)

> Obsidian vault workflow — daily note、markdown、Bases、図、Canvas、vault 管理、ダッシュボード設計を Claude Code plugin としてパッケージ化。

## スキルを選ぶ

利用条件と依頼例は[スキルガイド](skills/README.ja.md)へ。複数回にわたる研究プロジェクトと、単発の調査ノートには別々のガイドがあります。

## ホストの検証状況

[11 月 19 日の Codex 受け入れ試験](../docs/loom/2026-11-19-start-and-update-research-topic/evidence/acceptance-test-evidence.md#re-run-on-2026-11-19-at-18136e9531691e5b0fdd439a0bb4bea71d7462ff)では、導入済みキャッシュを試験対象のリビジョンと照合し、新規セッションでプロジェクトの作成、更新、同じ根拠の再投入を検証しました。[11 月 20 日の試験](../docs/skill-dogfood/2026-11-20-research-evidence-confidence/report.md)では、作業ツリーのスキルをテスト用 vault で実行しました。Cowork で Defuddle の URL 取得が制限される場合があると upstream は報告しています。

## Version

4.2.0 — [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) を参照。

Vault 初期設定は、個人に合わせた命名・ノート品質・現行 skill の規則を
`AGENTS.md` にまとめ、`CLAUDE.md` は `@AGENTS.md` と末尾の改行だけにする。
既存の両ファイルを読み、復元可能な非公開バックアップを取ってから統合する。
既存の memory とローカル skill は変更せず、不足ファイルの作成は preview の
明示的な承認が必要。個人の規則とバックアップはローカルに保持する。
Vault 初期設定は Codex の探索と Claude の import を利用します。初期設定が生成した規則を
新規セッションで読み込めるかは未検証です。global 設定や cache は自動変更しない。
別管理の OpenCode package は 0.2.0。

## 独立配布

[Monkey Skills](https://github.com/kouko/monkey-skills) から抽出し、
[Obsidian ResearchWorker](../README.md) で独立管理する。
plugin 名 `obsidian` は保持する。4.0.0 は 14 skill を提供し、8 つの wiki skill と
daily-news-digest を削除する。通常の daily note、単一テーマの研究、Defuddle 抽出、
wikilink は保持し、既存 vault の出力や設定は変更しない。切り替え前に
[移行ガイド](../docs/migration.md)を確認してください。
4.2.0 ではローカル検索を `obsidian-knowledge` に改名し、同梱の読み取り専用シェルスクリプトへ移行しました。
現在の作業ツリーには `obsidian-research-project` を含め、15 個のスキルがあります。

## 背景

Obsidian は local-first な markdown knowledge base。日常の vault 作業は小さい
反復タスクの集合になる：今日の daily note を開く、inbox を整理する、
有効な Bases YAML を書く、note 内に Mermaid 図を描く、session 終了時に会話の要約を保存する。

本 plugin はそれらのタスクを skill としてパッケージ化し、Claude Code が
intent に応じて dispatch する。Original skill は daily workflow /
ダッシュボード設計 / vault setup / 会話要約をカバー。Import 済 skill は
Obsidian 固有の markdown / Bases / Obsidian CLI / Defuddle web 抽出 /
Canvas 作成 / Excalidraw 図 / Mermaid 図をカバー。

## Router と agent

### Router

`using-obsidian` が entry skill。ユーザーの依頼内容（daily note、vault setup、
図、cleanup など）に応じて適切な skill に routing する。

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
| `obsidian-research-project` | 保存した研究を複数回にわたって開始・更新する。各ラウンドの範囲を確認し、過去の根拠を保持する。 |
| `obsidian-knowledge` | 任意の project からローカル vault を検索（読み取り専用）。SessionStart hook が各 session に vault の場所を伝える。Grep/Glob 不要 |
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
| `obsidian-mermaid-visualizer` | Mermaid 30 図種（flow / data-viz / structural / time）— Obsidian 1.15（Pele エンジン）最適化、`scripts/validate.sh` で検証、標準 Mermaid syntax なので GitHub / Notion / HackMD でも利用可 |

## Install

Codex の検証範囲は[ホストの検証状況](#ホストの検証状況)を参照してください。リモート導入と Claude/Cowork 互換性は未検証です。導入を切り替える前に[移行ガイド](../docs/migration.md)を確認してください。

`defuddle` skill は Defuddle CLI が必要：

```bash
npm install -g defuddle
```

`obsidian-cli` skill は公式 Obsidian CLI と起動中の Obsidian instance が必要 —
[help.obsidian.md/cli](https://help.obsidian.md/cli) 参照。

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
を選択し、Obsidian 1.15（Pele）の quirk を適用、` ```mermaid ` ブロックを出力する。

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
│   ├── obsidian-research-project/ # 複数回にわたる研究プロジェクト
│   ├── obsidian-knowledge/      # 読み取り専用 vault 検索（original）
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
