# Content Blast Manifest: [トピック名]

- 作成日: YYYY-MM-DD
- トピック: [テーマ名]
- Evidence Pack: `[EPファイルパス]`
- ステータス: 🟢 Complete / 🟡 In Progress / 🔴 Not Started

---

## 生成物一覧

| # | コンテンツ | ステータス | ファイルパス | 備考 |
|:--|:--|:--|:--|:--|
| 1 | 📝 Deep Dive 記事 | ⬜ | `02_Articles/YYYY/YYYY-MM-DD_[slug].md` | 2000字以上 |
| 2 | 🎨 インフォグラフィック | ⬜ | `03_SNS/visuals/YYYY-MM-DD_[slug].webp` | 9:16縦長 |
| 3 | 📱 X投稿文 | ⬜ | `03_SNS/posts/YYYY-MM-DD_[slug]_posts.md` | 単発3案+スレッド1案 |
| 4 | 🎙️ ポッドキャスト | ⬜ | `04_Media/podcasts/YYYY-MM-DD_[slug].mp3` | NotebookLM |
| 5 | 🎬 動画 | ⬜ | `04_Media/videos/YYYY-MM-DD_[slug].mp4` | NotebookLM |

### ステータス記号
- ⬜ 未着手
- 🔄 生成中
- ✅ 完了
- ❌ 失敗（要再試行）

---

## 品質チェック

- [ ] EPにない新主張を追加していないか
- [ ] 全Factに出典URLがあるか
- [ ] 数値に単位・前提条件があるか
- [ ] NGワード使用なし
- [ ] Brand Voice 準拠
- [ ] 記事 2000字以上
- [ ] 画像 9:16縦長
- [ ] Podcast/Video 生成確認済み

---

## NotebookLM 情報

- Notebook ID: `[nlm notebook ID]`
- Alias: `[nlm alias]`
- Source IDs: 
  - EP: `[source-id]`
  - Article: `[source-id]`

---

## Deploy

```bash
git add .
git commit -m "Content Blast: [トピック名]"
git push origin main
```
