# Visual Brief: 腸が脳を老化させる？

## メタ情報

- 元記事: `10_Projects/ST_channnel/03_SNS/articles/2026-02-16_Microbiome_Brain_Rejuvenation.md`
- 図解タイプ: mechanism / flow
- スタイル: dark / tech
- アスペクト比: 9:16（縦長）

---

## 情報抽出

| # | エンティティ | 役割 | ラベル（3語以内） |
| :-- | :-- | :-- | :-- |
| 1 | Aged Gut | 老化シグナルの発信源 | Aged Microbiome |
| 2 | Eotaxin-1 | 老化を伝えるメッセンジャー | Eotaxin-1 (Signal) |
| 3 | Aged Brain | 炎症で機能低下した脳 | Inflamed Brain |
| 4 | Rejuvenated Brain | 信号遮断で回復した脳 | Rejuvenated Brain |
| 5 | Antibiotics | 信号を断つ介入 | Block / Reset |

## 関係性/フロー

```
[Aged Microbiome] --(Eotaxin-1)--> [Inflamed Brain] (Aging)
       |
    (Block!)
       |
[Rejuvenated Brain] (New Neurons!)
```

---

## レイアウト指示

### 構図

上下分割（Before / After）または フロー図。

```
┌─────────────────────────────────┐
│     BRAIN AGING MECHANISM       │
│                                 │
│  🔴 AGING PATHWAY               │
│  ┌─────────┐   ⚡Eotaxin-1      │
│  │ Aged Gut│ ──────────────→ 🧠 │
│  └─────────┘   Inflammation     │
│                                 │
│  ─────────────────────────────  │
│                                 │
│  🟢 REJUVENATION PATHWAY        │
│  ┌─────────┐   🚫 Blocked       │
│  │ Reset   │ ──//──────────→ 🧠✨│
│  └─────────┘                    │
│   (Antibiotics)  New Neurons!   │
│                                 │
│  [Source: bioRxiv 2026.02.13]   │
└─────────────────────────────────┘
```

### 配色

| 要素 | 色 |
| :-- | :-- |
| 背景 | #0F172A (Deep Navy) |
| テキスト | #F1F5F9 (Slate White) |
| Aging (Bad) | #EF4444 (Red) |
| Rejuvenation (Good) | #10B981 (Emerald Green) |
| Eotaxin-1 | #F59E0B (Amber) |

### テキストオーバーレイ

- **タイトル**: 脳の若返りは腸から？ (Brain Rejuvenation Starts in the Gut?)
- **サブタイトル**: Antibiotics restore neurogenesis
- **注釈**: Mouse Model Study
- **出典**: bioRxiv

---

## 画像生成プロンプト (参考)

> 3D medical infographic, vertical 9:16.
> Top half shows "Aging": An aged intestine section emitting red particles (Eotaxin-1) traveling to a gray, dull brain model, causing red inflammation glow.
> Bottom half shows "Rejuvenation": The intestine is clear/reset, no red particles, leading to a glowing blue/cyan brain with bright neural sparks (neurogenesis).
> High-tech, dark background (#0F172A), professional medical illustration style, clean composition, cinematic lighting.
