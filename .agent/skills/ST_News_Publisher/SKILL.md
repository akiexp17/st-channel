---
name: ST_News_Publisher
description: Inboxからのニュース選定、日刊記事作成、週刊まとめ更新、ウェブサイトへのデプロイまでの一連の広報ワークフローを自動化します。RSS収集後の「編集・公開」フェーズを担当します。
---

# ST News Publisher

このスキルは、ST Channelにおけるニュース公開プロセスを標準化・自動化するための手順書です。

## 概要

このスキルを使用して、以下のタスクを実行します：
1.  **週次管理**: 現在の日付に基づき、適切な週次フォルダ（日曜始まり）を特定または作成する。
2.  **記事作成**: Inbox内のRSSリストから重要記事を選定し、指定されたテンプレートでMarkdownを作成する。
3.  **まとめ更新**: 週次まとめファイル（Folder Note）に記事リンクを追加する。
4.  **デプロイ**: 変更をGitHubにプッシュし、公開サイトへ反映する。

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

1.  Inboxのリストから、技術的に重要でインパクトのあるニュースを選定する。
2.  各ニュースについて、**必ずリンク先の本文をツールで取得・熟読し**、`TARGET_DIR` 内に日刊記事ファイル (`YYYY-MM-DD_Title.md`) を作成する。
    - 内容は `.agent/skills/ST_News_Publisher/assets/templates/Daily_News_Template.md` に従うこと（テンプレートも移動している場合）。

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
