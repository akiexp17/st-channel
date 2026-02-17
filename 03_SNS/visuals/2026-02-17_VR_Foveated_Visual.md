# Visual Brief: 世界はボヤけている (Foveated Rendering)

## メタ情報

- 元記事: `03_SNS/posts/2026-02-17_VR_Foveated.md`
- 図解タイプ: concept / heat map
- スタイル: dark (ST Channel Brand)
- アスペクト比: 9:16 (Vertical)

---

## 情報抽出

| # | エンティティ | 役割 | ラベル |
| :-- | :-- | :-- | :-- |
| 1 | Central Vision | 中心視野（高解像度） | FOVEAL AREA (HQ) |
| 2 | Peripheral Vision | 周辺視野（低解像度） | PERIPHERAL AREA (LQ) |
| 3 | GPU Load | 負荷軽減の表現 | GPU LOAD |
| 4 | Eye Gaze | 視点位置 | GAZE POINT |

## 関係性/フロー

Contrast between "What we think we see" vs "What is actually rendered".
Focus point = High Quality.
Surroundings = Low Quality (Blurred/Pixelated).

## レイアウト指示

**メインビジュアル: 一人称視点（FPS）**
- サイバーパンクな街並み、または美しい自然の風景。
- 中央に「視点マーカー（ターゲットサイト）」があり、そこだけが**超高精細・クリア**。
- その周囲に行くにつれて、同心円状に**モザイク/ボカシ**が強くなっていく（周辺視野のシミュレーション）。
- ※ただし、画像としては「技術解説図」に見えるように、あえて極端に差をつける。

**オーバーレイ要素**
- 中央: 「FOVEAL ZONE: 100% Quality」というタグ。
- 周辺: 「PERIPHERAL ZONE: 10% Quality」というタグ。
- 下部にグラフ的なインジケーター: 「GPU SAVE: 90%」

## 画像生成プロンプト

> A first-person view technical visualization of "Foveated Rendering". Vertical 9:16 format. Dark sci-fi city background.
>
> The image simulates a human eye's focus:
> 1.  **Center (Gaze Point)**: A sharp, high-resolution circular area showing detailed buildings and neon lights. Label "HQ ZONE".
> 2.  **Periphery**: The rest of the image outside the center circle is noticeably blurry or pixelated, getting lower quality towards the edges. Label "LQ ZONE".
>
> Overlay text: "GPU LOAD REDUCED BY 90%".
> Style: Cyberpunk HUD aesthetics, heavy contrast between sharp center and blurry edges. Blue and purple neon tones.

