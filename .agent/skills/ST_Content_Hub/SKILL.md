---
name: ST_Content_Hub
description: >
  STチャンネルの統合コンテンツパイプライン。一つのトピックからDeep Research→記事→SNS投稿→画像→
  ポッドキャスト→動画→Short動画までを一括生成する「Content Blast」を実現するオーケストレーションスキル。
  多言語対応（--language ja/en）、NotebookLMウォーターマーク自動除去にも対応。
  トリガー: 「深掘りして全部作って」「このテーマを調査して」「EPから全コンテンツ」
  「Content Blast」「全部作って」「一括生成」「統合パイプライン」
---

# ST Content Hub — 統合コンテンツパイプライン

**1トピック → 全アウトプット**を実現する、STチャンネルのマスターオーケストレーションスキル。

## 概要

```
   トピック入力
       │
   ┌───▼───┐
   │ Deep  │  search_web + read_url_content で徹底調査
   │Research│  10-20ソース収集 → 交差検証
   └───┬───┘
       │
   ┌───▼───────────┐
   │ Evidence Pack │  構造化された調査結果
   │  (Enhanced)   │  Fact/Model/Hypothesis 分類済
   └───┬───────────┘
       │
   ┌───▼───────────────────────────────────────────┐
   │              Content Blast                      │
   │  ┌────────┬────────┬────────┬────────┬───────┬────────┐  │
   │  │Article │  Post  │ Visual │Podcast │ Video │ Short  │  │
   │  │ Forge  │ Forge  │ Forge  │ Forge  │ Forge │ Video  │  │
   │  └───┬────┴───┬────┴───┬────┴───┬────┴───┬───┴───┬────┘  │
   └──────┼────────┼────────┼────────┼────────┼────────┼───────┘
           │        │        │        │        │       │
           ▼        ▼        ▼        ▼        ▼       ▼
       02_Articles 03_SNS  03_SNS  04_Media 04_Media 04_Media
                   /posts  /visuals /podcasts /videos /videos
```

## トリガーキーワード

| キーワード | 実行内容 |
|:--|:--|
| 「深掘りして全部作って」 | Deep Research → Content Blast 全自動 |
| 「このテーマを調査して」 | Deep Researchのみ → EP生成 |
| 「EPから全コンテンツ」 | 既存EPからContent Blastのみ |
| 「ポッドキャストを作って」 | Podcast Forgeのみ（nlm連携） |
| 「動画を作って」 | Video Forgeのみ（nlm連携） |
| 「今週のコンテンツ計画」 | Campaign Forge |

---

## Mode 1: Deep Research

> ChatGPT Deep Research と同等の深い調査を、`search_web` + `read_url_content` で実現する。

### 手順

1. **スコープ定義**: トピックの核心となる「問い」を3つ設定する
   - 「これは何か？」（What）
   - 「なぜ重要か？」（Why）
   - 「どう機能するか？」（How）

2. **ソース収集**（10-20件を目標）
   ```
   search_web で以下を順に検索:
   ① "[トピック] 論文 研究" → 学術ソース
   ② "[トピック] mechanism how it works" → 英語技術資料
   ③ "[トピック] 最新 2025 2026" → 最新動向
   ④ "[トピック] 批判 限界 問題" → 反対意見・制約
   ⑤ "[トピック] 数値 データ 統計" → 定量情報
   ```

3. **ソース読み込み & 検証**
   - 各URLを `read_url_content` で全文取得
   - 重要な主張は**必ず2ソース以上で交差検証**
   - 信頼度ラベル付与: 一次（論文・公式）/ 二次（報道）/ 三次（まとめ）

4. **Evidence Pack 生成**
   - テンプレート: `assets/templates/Enhanced_Evidence_Pack.md`
   - 全情報に Fact / Model / Hypothesis ラベルを付与
   - 保存先: `03_SNS/research/` に日付付きで保存

### 品質基準
- [ ] ソースは10件以上あるか
- [ ] 一次資料が50%以上か
- [ ] 核心的主張は2ソース以上で検証済みか
- [ ] 反対意見・制約が最低1つ含まれるか

---

## Mode 2: Content Blast

> 1つのEvidence Packから6種類のコンテンツを順次生成する。多言語対応（`--lang ja/en`）。

### オーケストレーションスクリプト

```bash
python3 .agent/skills/ST_Content_Hub/scripts/content_blast.py \
  --ep "03_SNS/research/YYYY-MM-DD_EP_トピック.md" \
  --slug "topic_slug" \
  --lang ja  # 音声・動画の言語（デフォルト: ja）
```

### 実行順序（依存関係を考慮）

```
Step 1: Article Forge (記事が他コンテンツのベース)
    ↓
Step 2: Visual Forge (記事に挿入 & SNS投稿に添付)
    ↓
Step 3: Post Forge (記事+画像をベースにSNS投稿文生成)
    ↓
Step 4: Podcast Forge (NotebookLMにEPを投入→音声生成)
    ↓
Step 5: Video Forge (NotebookLMでExplainer動画生成)
    ↓
Step 6: Short Video Forge (NotebookLMでBrief動画生成)
    ↓
Step 7: Watermark除去 (NotebookLMロゴを自動除去)
    ↓
Step 8: Manifest更新 (全生成物のリンクを記録)
```

### Step 1: Article Forge — 深掘り記事

**使用スキル**: `ST_News_Publisher` の脱AI10ポイント + `ST_Social_Engine` の Story Forge

**手順**:
1. EPから最もインパクトのあるHookを選定
2. `assets/templates/Story_Template.md`（ST_Social_Engine参照）の構成で執筆
3. **2000文字以上**の深掘り記事を作成
4. 保存先: `02_Articles/YYYY/YYYY-MM-DD_[slug].md`

**記事構成**:
```
# [タイトル：読者の常識を揺さぶる1文]

[Introduction — 400字] Hook + 宣言

## 1. なぜ「X」はYなのか？
[500字] 課題分析/謎の提示 → 二層構造（直感→理屈）

## 2. Xの正体
[600字] 技術メカニズム → 二層構造

## 3. 数字が語る真実
[300字] データ裏付け → 数値翻訳

## 4. これでXは何が変わる？
[400字] So What? + 読者への問い

---
出典:
```

**品質ゲート（脱AI10ポイント）**:
- [ ] 教科書感がないか
- [ ] リズムに変化があるか（独白、倒置、体言止め）
- [ ] 感情が入っているか
- [ ] 最後に読者への「問い」があるか
- [ ] 文字数は2000字以上か

### Step 2: Visual Forge — インフォグラフィック

**使用ツール**: `generate_image`

**手順**:
1. EPの「仕組みの流れ」から図解タイプを決定
   - flow / compare / timeline / structure / misconception
2. ラベル3語ルール: 各要素を3語以内に圧縮
3. `generate_image` で以下の仕様で画像生成:

**画像仕様（必須）**:
- アスペクト比: **9:16 縦長ポートレート**
- スタイル: ダークネイビー背景（`#0F172A`）
- パネル: フロステッドグラス効果
- アクセント: 青（冷たい情報）↔ 赤（暖かいインパクト）
- テキスト: 英語ラベル（フォント可読性確保）
- ヒーロー: フォトリアルな写真素材

4. 保存先: `03_SNS/visuals/YYYY-MM-DD_[slug].webp`

### Step 3: Post Forge — X投稿文

**使用スキル**: `ST_Social_Engine` の Post Forge

**手順**:
1. 記事を「壊さず圧縮」
2. **アルゴリズムハック7鉄則**に従い投稿文を生成:
   - 単発案3つ（各Hookパターン）
   - スレッド案1つ（5-8ツイート）
3. 画像添付の指示を含む
4. テンプレート: `ST_Social_Engine/assets/templates/X_Post_Template.md`
5. 保存先: `03_SNS/posts/YYYY-MM-DD_[slug]_posts.md`

**Brand Voice チェック**:
- [ ] NGワードなし（画期的な/注目の/話題の 等）
- [ ] 絵文字は 🔬📊📎 程度
- [ ] ハッシュタグ 0-2個
- [ ] 出典省略なし

### Step 4: Podcast Forge — ポッドキャスト

**使用ツール**: `nlm`（NotebookLM CLI）

**手順**:
```bash
# 1. ノートブック作成（または既存のST Channel用ノートブックを使用）
nlm notebook create "ST Channel: [トピック名]"

# 2. Evidence Packのテキストをソースとして追加
nlm source add <nb-id> --text "<EPの全文>" --title "[トピック名] Evidence Pack"

# 3. 記事もソースとして追加
nlm source add <nb-id> --text "<記事の全文>" --title "[トピック名] 記事"

# 4. ポッドキャスト生成（--language で言語指定）
nlm audio create <nb-id> --format deep_dive --language ja --length default --confirm

# 5. 生成完了を待つ
nlm studio status <nb-id>

# 6. ダウンロード（日本語版は _ja サフィックス）
nlm download audio <nb-id> --output 04_Media/podcasts/YYYY-MM-DD_[slug]_ja.mp3
```

**多言語オプション**: `--language` に BCP-47 コード（`en`, `ja`, `es`, `fr`, `de`）を指定。
ファイル名には言語サフィックスを付与（例: `_ja.mp3`）。英語の場合はサフィックスなし。

### Step 5: Video Forge — Explainer動画

**使用ツール**: `nlm`（NotebookLM CLI）

**手順**:
```bash
# 同じノートブックからExplainer動画を生成
nlm video create <nb-id> --format explainer --style auto_select --language ja --confirm

# 生成完了を待つ
nlm studio status <nb-id>

# ダウンロード
nlm download video <nb-id> --output 04_Media/videos/YYYY-MM-DD_[slug]_ja.mp4
```

### Step 6: Short Video Forge — Short動画

**使用ツール**: `nlm`（NotebookLM CLI）

> TikTok/YouTube Shorts/Instagram Reels 向けの1分以内のショート動画を生成する。

**手順**:
```bash
# Brief形式でショート動画を生成
nlm video create <nb-id> --format brief --style auto_select --language ja --confirm

# 生成完了を待つ
nlm studio status <nb-id>

# ダウンロード（ファイル名に _short を付与）
nlm download video <nb-id> --output 04_Media/videos/YYYY-MM-DD_[slug]_short_ja.mp4
```

### Step 7: Watermark除去 — NotebookLMロゴ消去

NotebookLMが生成する動画には右下に「NotebookLM」ロゴ、末尾に「notebooklm.google.com」画面が含まれる。
公開前にこれらを自動除去する。

**使用スクリプト**: `scripts/remove_nlm_watermark.py`

```bash
# 全動画を一括処理（元ファイルを上書き）
python3 .agent/skills/ST_Content_Hub/scripts/remove_nlm_watermark.py \
  --dir 04_Media/videos/ --in-place

# 単一ファイルの処理
python3 .agent/skills/ST_Content_Hub/scripts/remove_nlm_watermark.py \
  --input 04_Media/videos/YYYY-MM-DD_[slug]_ja.mp4
```

**処理内容**:
1. 右下の「NotebookLM」テキスト＋アイコンを白塗り（drawbox）
2. 末尾3秒のエンドカード（notebooklm.google.com）をカット
3. CRF 18 で libx264 再エンコード

> **Note**: `--portrait` オプションで Short動画を 9:16 縦長に変換することも可能だが、NotebookLMの動画はテキストが画面全幅に配置されるため、中央クロップでは文字が見切れる。デフォルトでは 16:9 のまま処理する。

### Step 8: Manifest更新

Content Blast Manifest に全生成物のパスを記録:

```bash
python3 .agent/skills/ST_Content_Hub/scripts/update_manifest.py \
  --date YYYY-MM-DD \
  --slug [slug] \
  --article "02_Articles/YYYY/YYYY-MM-DD_[slug].md" \
  --visual "03_SNS/visuals/YYYY-MM-DD_[slug].webp" \
  --posts "03_SNS/posts/YYYY-MM-DD_[slug]_posts.md" \
  --podcast "04_Media/podcasts/YYYY-MM-DD_[slug]_ja.mp3" \
  --video "04_Media/videos/YYYY-MM-DD_[slug]_ja.mp4" \
  --short-video "04_Media/videos/YYYY-MM-DD_[slug]_short_ja.mp4"
```

---

## Mode 3: Campaign Forge

> 週間コンテンツカレンダーを生成し、投稿戦略を立てる。

**スケジュール**: 月〜金=1日1投稿, 土=スレッド, 日=休息
**タイムスロット**: 朝7-8時(通勤), 昼12-13時(ランチ), 夜20-22時(ピーク)

テンプレート: `ST_Social_Engine/assets/templates/Campaign_Calendar_Template.md`

---

## 既存スキルとの関係

```
ST_Content_Hub（このスキル: オーケストレーション層）
    │
    ├── ST_News_Publisher（記事品質基準・脱AI10ポイント）
    │     └── 記事執筆のライティングガイドとして参照
    │
    ├── ST_Social_Engine（各Forgeのテンプレート・ガイド）
    │     ├── Evidence Pack テンプレート
    │     ├── Story テンプレート
    │     ├── Post Forge テンプレート & アルゴリズムハック
    │     ├── Visual Forge 仕様
    │     └── Campaign Calendar テンプレート
    │
    └── nlm-skill（NotebookLM CLI操作ガイド）
          └── Podcast & Video 生成
```

> **重要**: ST_Content_Hubは既存スキルを**置き換えない**。
> 各スキルの専門性はそのまま活かし、統合パイプラインを提供する「指揮者」の役割。

---

## ディレクトリ構造

```
10_Projects/ST_channnel/
├── 01_News/              # RSS ニュース（既存）
├── 02_Articles/          # 深掘り記事
│   └── YYYY/
├── 03_SNS/               # SNS コンテンツ
│   ├── articles/         # SNS向け記事（既存）
│   ├── posts/            # X投稿文
│   ├── research/         # Evidence Packs
│   ├── themes/           # テーマ候補
│   └── visuals/          # インフォグラフィック
├── 04_Media/             # マルチメディア
│   ├── podcasts/         # ポッドキャスト音声 (*_ja.mp3, *.mp3)
│   ├── videos/           # 動画素材 (*_ja.mp4, *_short_ja.mp4)
│   └── manifests/        # Content Blast Manifests
├── 05_Simulations/       # インタラクティブシミュレーション
└── 99_System/            # システム設定
```

## ファイル命名規則（多言語対応）

| メディア種別 | 英語版 | 日本語版 |
|:--|:--|:--|
| ポッドキャスト | `{date}_{slug}.mp3` | `{date}_{slug}_ja.mp3` |
| Explainer動画 | `{date}_{slug}.mp4` | `{date}_{slug}_ja.mp4` |
| Short動画 | `{date}_{slug}_short.mp4` | `{date}_{slug}_short_ja.mp4` |

---

## Deploy

```bash
git add .
git commit -m "Content Blast: [トピック名] - article, posts, visual, podcast, video"
git push origin main
```

---

## スクリプト一覧

| スクリプト | 用途 |
|:--|:--|
| `scripts/content_blast.py` | Content Blastオーケストレーション（`--lang`で言語指定） |
| `scripts/deep_research.py` | Deep Researchオーケストレーション |
| `scripts/nlm_pipeline.py` | NotebookLM CLIラッパー |
| `scripts/update_manifest.py` | Manifest更新（`--short-video`対応） |
| `scripts/remove_nlm_watermark.py` | 動画ウォーターマーク自動除去 |

---

## 品質ゲート（Content Blast 完了前チェック）

- [ ] EPにない新主張を記事やポストに追加していないか
- [ ] 全Factに出典URLがあるか
- [ ] 数値に単位・前提条件があるか
- [ ] NGワードを使っていないか
- [ ] Brand Voice 7原則に違反していないか
- [ ] 記事は2000字以上か
- [ ] 画像は9:16縦長で生成されているか
- [ ] ポッドキャスト/動画/Short動画の生成状態を確認したか
- [ ] ウォーターマーク除去が完了しているか
- [ ] Manifestが正しく更新されているか（多言語版含む）
