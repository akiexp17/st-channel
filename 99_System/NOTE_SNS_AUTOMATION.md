# Note + SNS 運用手順（0から開始用）

## 目的
- 最新科学技術論文を、面白く・実務に使える形で発信する。
- note を収益導線、X/Instagram を集客導線として運用する。

## このリポジトリでやること
1. 記事草稿を作る
2. SNS投稿文を作る
3. 投稿チェックリストで公開漏れを防ぐ

## 1本目の完成ファイル
- 記事本文: `02_Articles/2026/2026-02-07_SCALAR_materials_foundation_models_note.md`
- SNS文面: `99_System/social/2026-02-07_SCALAR_posts.md`

## 量産コマンド
```bash
python3 99_System/scripts/create_note_campaign.py \
  --date 2026-02-08 \
  --slug lora-variants \
  --title "LoRA派生を追う前に読むべき1本" \
  --topic "LLMファインチューニング評価" \
  --paper-title "A Unified Study of LoRA Variants" \
  --paper-url "https://arxiv.org/abs/2601.22708"
```

## 投稿まで全部自動化できるか
- この環境では、外部アカウント（note / X / Instagram）の認証情報が未設定のため、API経由の実投稿は未実行。
- ただし、投稿本文と公開順は作成済みなので、アカウントログイン後に即公開可能。

## 公開時の実務ルール
- 一次情報リンク（論文URL）を必ず載せる。
- 「無料部分: 学び」「有料部分: 時短/実装テンプレ」を明確に分ける。
- 投稿後24時間で反応を見て、Xで追記投稿を1本追加する。
