---
name: ST_Social_Engine
description: >
  ST Channelの科学技術コンテンツをX(Twitter)向けに企画・リサーチ・執筆・投稿最適化する統合スキル。
  以下のキーワードで発動: 「SNSのネタ」「テーマを考えて」「調べて」「Evidence Pack」「記事を書いて」
  「Xに投稿」「図解を作って」「SNS戦略」「投稿カレンダー」「Post Forge」「Research Forge」「Story Forge」
  「Visual Forge」「Campaign Forge」「Theme Forge」
---

# ST Social Engine

科学技術を「正確に、面白く、継続的に」発信する**完全自律型コンテンツパイプライン**。

## 6つのForge

| # | Forge | 一言 | トリガー例 |
| :-- | :-- | :-- | :-- |
| 1 | **Theme Forge** | ネタ発掘 | 「SNSのネタを考えて」 |
| 2 | **Research Forge** | 深掘り調査 | 「なぜ空は青いか調べて」 |
| 3 | **Story Forge** | 記事執筆 | 「EPから記事を書いて」 |
| 4 | **Post Forge** | X投稿文生成 | 「この記事をXに投稿して」 |
| 5 | **Visual Forge** | 図解設計 | 「図解を作って」 |
| 6 | **Campaign Forge** | 週間戦略 | 「今週のSNS戦略を立てて」 |

**パイプライン**: Theme → Research → Story → Post/Visual → Campaign
各モードは単独実行も可。`ST_News_Publisher`の記事をPost Forgeに直接入力することも可能。

## 出力先

```
10_Projects/ST_channnel/03_SNS/
├── themes/      ├── research/    ├── articles/
├── posts/       ├── visuals/     └── campaigns/
```

---

## Design Thinking — 全Forge共通の哲学

コンテンツを作る前に、必ずこの3問を自問する:

1. **誰の「えっ、マジで？」を狙うのか**: ターゲットの常識を特定し、それを裏切る
2. **何が検証可能で、何が推測か**: Fact / Model / Hypothesis を常に区別する
3. **「だから何？」に答えられるか**: So What? がないコンテンツは出さない

## 鉄のルール

> **新しい事実はResearch Forge以外で追加しない。**
> Story ForgeやPost Forgeが「面白そうだから」と捏造した情報は、出典不明になり信頼を破壊する。

## Brand Voice — ST Channel X Voice

**トーン**: 学者が居酒屋で語る — 正確だけど堅くない。
- 知的好奇心の着火: 「へぇ」ではなく「えっ、マジで？」
- 数値は翻訳する: 「3,300トン」→「東京ドームX杯分」
- 意見を持つ。中立は退屈
- 絵文字は 🔬📊📎 程度。🎉🙌❤️ は禁止
- ハッシュタグ 0-2個
- 出典は省略しない

**NGワード**: 画期的な / 注目の / 話題の / 衝撃の / ついに / いよいよ /
〜してみた / 〜がヤバすぎる / いかがでしたか？ / まとめ / 参考になれば幸いです

---

## Mode Details

### 1. Theme Forge

ユーザーと**対話**でテーマを探索する。3カテゴリから均等に候補を出す:
- 🔍 **日常の謎**: 当たり前を「なぜ？」に（空が青い、ゴムが伸びる）
- 🔧 **テック深掘り**: バズワードの中身を解剖（GPU、量子もつれ）
- ⚖️ **社会×科学**: 噂を科学で検証（添加物、5G）

10件候補 → 5軸スコアリング → 上位3件にHook・誤解・図解の型を添えて提案。
テンプレート: `assets/templates/Theme_Candidates_Template.md`

### 2. Research Forge

テーマについて `search_web` + `read_url_content` で調査し、**Evidence Pack (EP)** を作成。
- 一次資料を優先（論文、公式、政府報告書）
- 重要主張は2ソース以上で交差検証
- 全情報に Fact / Model / Hypothesis ラベル

EP構成: 要点3行 → 用語辞書 → 仕組みの流れ → 誤解ポイント → 数値 → 限界 → Hook候補 → 比喩候補 → 出典テーブル
テンプレート: `assets/templates/Evidence_Pack_Template.md`

### 3. Story Forge

EPを**Newton/NatGeo風の読者体験**に変換する。

**Story Spine**: Hook(400字) → なぜ?(500字) → 仕組み(600字) → 証拠(300字) → 未来(400字)

**二層構造**: 全技術説明は「直感（比喩）→ 理屈（正確な説明）」の2段階で書く。

**脱AI10ポイント**: 教科書感排除 / リズム変化 / 感情注入 / 会話調 / 共感獲得 /
具体的比喩 / 思考プロセス露出 / 中立病打破 / 語尾バリエーション / 最後の問い

テンプレート: `assets/templates/Story_Template.md`
ライティングガイド: `references/writing_guide.md`

### 4. Post Forge — アルゴリズムハック

記事を「壊さず圧縮」し、**Xアルゴリズム（Heavy Ranker）のスコアを最大化する**投稿文に変換する。

**アルゴリズム重み付け（いいね=1x基準）**:
- リプライのリプライ（会話）×75 / リプライ ×27 / RT ×20 / ブックマーク ×10 / いいね ×1

**7つの鉄則**:
1. **会話を設計**: 二択問いで締めリプライ×27-75を狙う
2. **スレッドで滞在時間**: 5-8ツイートで2分超滞在×22-150を稼ぐ
3. **事実の弾丸**: 共有したくなるデータでRT×20を誘発
4. **保存知識**: チートシートでブックマーク×10を狙う
5. **リンク分離**: 外部URLはリプ欄へ（本文ペナルティ-50〜90%回避）
6. **メディア添付**: 図解・動画で大幅ブースト（10秒以上視聴×8）
7. **初速最大化**: 投稿時間は朝7-8/昼12-13/夜20-22時

システムプロンプト: `assets/prompts/post_forge_system.md`
テンプレート: `assets/templates/X_Post_Template.md`, `assets/templates/X_Thread_Template.md`

### 5. Visual Forge

X投稿に添付する図解を設計し、**実際に画像を生成する**。

**図解タイプ**: flow / compare / timeline / structure / misconception
**ラベル3語ルール**: 各要素を3語以内に圧縮

**画像仕様（必須）**:
- アスペクト比: **9:16 縦長ポートレート**（スマホ/Reels/Stories向け）
- スタイル: シックなダークネイビー（`#0F172A`）、ゴールド禁止
- ヒーロー: **フォトリアルな製品写真**（イラスト調NG）
- パネル: フロステッドグラス効果、青（冷）↔ 赤（暖）のアクセント
- `generate_image` ツールで実際に画像を生成し `03_SNS/visuals/` に保存

システムプロンプト: `assets/prompts/visual_forge_system.md`
テンプレート: `assets/templates/Visual_Brief_Template.md`

### 6. Campaign Forge

週単位の投稿戦略・カレンダーを生成する。

**スケジュール**: 月〜金=1日1投稿, 土=スレッド, 日=休息
**タイムスロット**: 朝7-8時(通勤), 昼12-13時(ランチ), 夜20-22時(最高エンゲージメント)

テンプレート: `assets/templates/Campaign_Calendar_Template.md`

---

## 品質ゲート（全Forge共通・出力前に必ず確認）

- [ ] EPにない新主張を追加していないか
- [ ] Factに出典URLがあるか
- [ ] 数値に単位・前提条件があるか
- [ ] NGワードを使っていないか
- [ ] Brand Voice 7原則に違反していないか
