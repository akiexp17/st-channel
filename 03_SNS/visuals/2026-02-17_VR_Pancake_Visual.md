# Visual Brief: VRのダイエット (Pancake Lens)

## メタ情報

- 元記事: `03_SNS/posts/2026-02-17_VR_Pancake.md`
- 図解タイプ: structure / comparison
- スタイル: dark (ST Channel Brand)
- アスペクト比: 9:16 (Vertical)

---

## 情報抽出

| # | エンティティ | 役割 | ラベル |
| :-- | :-- | :-- | :-- |
| 1 | Old Lens | 比較対象（厚い） | FRESNEL LENS |
| 2 | New Lens | 主役（薄い） | PANCAKE LENS |
| 3 | Light Path | 光の軌跡 | LIGHT PATH |
| 4 | Display | 映像源 | DISPLAY |
| 5 | Eye | 観察者 | EYE |

## 関係性/フロー

Comparison of Light Paths.
Old: Straight path (Long physical distance).
New: Folded path (Short physical distance).

## レイアウト指示

上下2分割の比較図。

**上段: FRESNEL LENS (Legacy)**
- 側面図。
- DisplayからEyeまで、光が「真っ直ぐ」進む。
- その分、DisplayとLensの距離が遠い（矢印で「Bulky」と記述）。

**下段: PANCAKE LENS (Modern)**
- 側面図。
- Displayから出た光が、レンズ内で「Z字」のように反射・往復してからEyeに届く。
- DisplayとLensの距離が圧倒的に近い（矢印で「Compact (-40%)」と記述）。
- レンズ内部で光が折りたたまれている様子を強調。

## 画像生成プロンプト

> A split-screen technical diagram comparing "Fresnel Lens" vs "Pancake Lens" in VR headsets. Vertical 9:16 format. Dark navy background (#0F172A).

> Top section "OLD: FRESNEL LENS":
> - Side view cross-section. Light rays travel straight from a Display on the left to an Eye on the right.
> - The distance between Display and Lens is long. Label "BULKY".
> - Simple convex lens shape.

> Bottom section "NEW: PANCAKE LENS":
> - Side view cross-section. Light rays from Display travel to the Lens, then BOUNCE back and forth explicitly inside the lens elements (folded optics) before reaching the Eye.
> - The distance between Display and Lens is very short/thin. Label "COMPACT".
> - Multi-element flat lens shape.

> Style: Neon blueprint aesthetic. Cyan and Magenta light rays. High contrast. Clean vector lines.

