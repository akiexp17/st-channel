# A Unified Study of LoRA Variants: Taxonomy, Review, Codebase, and Empirical Evaluation

> [!info] 引用元
> [A Unified Study of LoRA Variants: Taxonomy, Review, Codebase, and Empirical Evaluation](https://arxiv.org/abs/2601.22708)

# 概要
パラメータ効率の良いファインチューニング手法「LoRA」とその多数の派生手法について、体系的な分類と統一的な評価を行った研究。結論として、**「適切に調整すれば、オリジナルのLoRAがほとんどの派生手法と同等以上の性能を出す」**という重要な知見が得られた。

# 背景
LoRAの登場以降、AdaLoRA, DoRA, VeRAなど無数の派生手法（Variants）が提案されているが、評価条件がバラバラで「結局どれを使えばいいのか」が不明瞭だった。本研究はこの混乱を整理し、統一的なコードベース「LoRAFactory」を公開した。

# 詳細
- **4つの分類軸**: ランク(Rank)、最適化ダイナミクス、初期化、MoE統合の観点から派生手法を分類。
- **実験結果**: 自然言語生成・理解、画像分類などのタスクで大規模比較を実施。
    - LoRAおよびその派生は学習率（Learning Rate）の選択に非常に敏感である。
    - 適切なハイパーパラメータを設定すれば、元祖LoRAは多くの派生手法に勝るとも劣らない性能を発揮する。
- **LoRAFactory**: 統一インターフェースで様々なLoRA派生を試せるモジュラーなコードベースを提供。

# 影響・考察
実務者にとって非常に価値のある「ネガティブ・リザルト（派生手法の優位性否定）」を含む研究。「新しいLoRA派生を追いかけるよりも、標準LoRAのパラメータチューニングに注力すべき」という指針は、多くのエンジニアの時間を節約するだろう。
