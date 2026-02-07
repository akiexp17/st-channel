---
name: ST_News_Publisher
description: Inboxからのニュース選定、日刊記事作成、週刊まとめ更新、ウェブサイトへのデプロイまでの一連の広報ワークフローを自動化します。RSS収集後の「編集・公開」フェーズを担当します。
---

# ST News Publisher

このスキルは、ST Channelにおけるニュース公開プロセスを標準化・自動化するための手順書です。

## 概要

このスキルを使用して、以下のタスクを実行します：
1.  **週次管理**: 現在の日付に基づき、適切な週次フォルダ（日曜始まり）を特定または作成する。
2.  **ニュース選定**: Inbox内のRSSリストをスコアリングし、重複統合して上位記事を抽出する。
3.  **記事作成**: 選定記事を固定構成テンプレートでMarkdown化する。
4.  **品質チェック**: 公開前に品質ゲートを実施する。
5.  **タイトル最適化**: タイトル3案を作成し最終案を採用する。
6.  **まとめ更新**: 週次まとめファイル（Folder Note）に記事リンクを追加する。
6.  **デプロイ**: 変更をGitHubにプッシュし、公開サイトへ反映する。

## 使い方 (Usage)

このスキルは、**InboxにRSS記事が収集された状態で**、ユーザーから以下のような依頼があった際に使用する。

> 「ニュースを更新して」
> 「今週のまとめ記事を作って公開して」
> 「InboxのRSSから記事を作成して」

このスキルを呼び出すことで、ターゲットフォルダの計算からGit Pushまでの一連の流れを自律的に実行できる。

## 前提条件

- カレントディレクトリが `10_Projects/ST_channnel`（リポジトリルート）であること。
- `01_News/Inbox` にRSS収集済みの未処理ファイルが存在すること。

## 手順 (Workflow)

### 1. ターゲットフォルダの特定

週次フォルダのパスを計算するために、ヘルパースクリプトを実行する。

```bash
python3 .agent/skills/ST_News_Publisher/scripts/get_weekly_target.py
```

- **出力 `STATUS=NEW` の場合**:
    - 出力された `TARGET_DIR` パスに新しいディレクトリを作成する。
    - その中に `YYYY-MM-DD--ST-news.md` を作成する（`index.md` ではなく、フォルダ名と同名のファイル）。
    - ファイルの先頭に `# YYYY-MM-DD--ST-news` を記述し、テーブルヘッダーを用意する。
- **出力 `STATUS=EXISTS` の場合**:
    - 既存の `TARGET_DIR` とまとめファイルを使用する。

### 2. ニュース選定と記事執筆

`01_News/Inbox` 内の最新のMarkdownファイル（例: `YYYY-MM-DD_RSS_Links.md`）を読み込む。
**News Research Prompt** (`.agent/skills/ST_News_Publisher/assets/prompts/news_research_prompt.md`) の基準とフォーマットに従い、以下の処理を行う。

1.  **1コマンド実行**で RSS取得 + スコアリング + 重複統合を実行する。

```bash
python3 .agent/skills/ST_News_Publisher/scripts/run_news_pipeline.py
```

- 既存Inboxを使って再スコアリングのみ行う場合:

```bash
python3 .agent/skills/ST_News_Publisher/scripts/run_news_pipeline.py \
  --skip-fetch \
  --inbox 01_News/Inbox/YYYY-MM-DD_RSS_Links.md \
  --top 8 \
  --min-score 5.2
```

2.  （手動分割で実行する場合）Inboxをスコアリングし、重複統合して上位候補を抽出する。

```bash
python3 .agent/skills/ST_News_Publisher/scripts/select_news_candidates.py \
  --inbox 01_News/Inbox/YYYY-MM-DD_RSS_Links.md \
  --top 8 \
  --min-score 5.2
```

3.  生成された `YYYY-MM-DD_Ranked_Candidates.md` の上位記事のみを執筆対象にする。
4.  各ニュースについて、**必ずリンク先の本文をツールで取得・熟読し**、`TARGET_DIR` 内に日刊記事ファイル (`YYYY-MM-DD_Title.md`) を作成する。
    - 内容は `.agent/skills/ST_News_Publisher/assets/templates/Daily_News_Template.md` の固定構成
      (`何が起きた→なぜ重要か→技術ポイント→懐疑点・未確定要素→実務インパクト`)
      に従うこと。
5.  タイトルは「事実＋驚き＋具体性」で3案生成し、最終1案を採用する。

```bash
python3 .agent/skills/ST_News_Publisher/scripts/title_optimizer.py \
  --fact "<事実>" \
  --surprise "<驚き>" \
  --specific "<具体性>"
```

6.  各記事に対して品質ゲートを実行し、PASSしたものだけ公開対象にする。

```bash
python3 .agent/skills/ST_News_Publisher/scripts/quality_gate.py \
  --file 01_News/YYYY/YYYY-MM-DD--ST-news/YYYY-MM-DD_Title.md
```

### 3. まとめファイルの更新

作成した記事を `TARGET_DIR/YYYY-MM-DD--ST-news.md` の一覧テーブルに追加する。

- **フォーマット**:
  `| **[[File_Name|Title]]**<br>[Summary] | [Link](File_Name) | [Source](URL) |`
- **注意**: リンク切れを防ぐため、`File_Name` は作成したファイル名と完全に一致させること。

### 4. 変更の公開 (Deploy)

すべての記事作成とまとめ更新が完了したら、以下のコマンド順でデプロイを実行する。

```bash
git add .
git commit -m "Update news: YYYY-MM-DD"
git push origin main
```

プッシュ成功を確認し、ユーザーに完了を報告する。

## 追加ルール（優先度A）

### ニュース選定スコアリング
- 4軸で0〜10採点:
  - 技術新規性
  - 実務影響
  - 信頼性
  - 鮮度
- 総合スコア:
  `0.35*技術新規性 + 0.30*実務影響 + 0.20*信頼性 + 0.15*鮮度`
- 上位のみ採用する（通常5〜8件）。

### 重複検知
- URL正規化で同一URLを統合する。
- タイトル類似度で近似重複を統合する。
- 統合後の代表記事のみを執筆する。

### 品質ゲート
- 一次ソース有無
- 日付整合
- 主張と根拠の一致
- 誇張表現除去

上記4点が1つでもNGなら公開しない。
