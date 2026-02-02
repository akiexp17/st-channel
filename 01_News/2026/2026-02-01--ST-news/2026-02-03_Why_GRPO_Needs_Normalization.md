# Why GRPO Needs Normalization: A Local-Curvature Perspective on Adaptive Gradients

> [!info] 引用元
> [Why GRPO Needs Normalization: A Local-Curvature Perspective on Adaptive Gradients](https://arxiv.org/abs/2601.23135)

# 概要
DeepSeek-R1などで採用されている強化学習手法「GRPO (Group Relative Policy Optimization)」において、なぜ「標準偏差による正規化」が重要なのかを理論的・実験的に解明した研究。正規化が実質的に適応的勾配（Adaptive Gradient）として機能していることを示した。

# 背景
LLMの推論能力向上において、GRPOはCriticモデル（価値関数）を学習せずに済むため、計算効率の良い標準的な手法となっている。GRPOではプロンプトごとのベースラインと分散正規化を用いるが、この「正規化」がなぜ性能向上に寄与するのか、その数理的なメカニズムは不明確だった。

# 詳細
- **局所曲率の視点**: ポリシー勾配の局所的な曲率（Local Curvature）を通して分析した結果、標準偏差による正規化は、パラメータ更新における「適応的なステップサイズ調整」として機能していることが判明した。
- **3つの学習フェーズ**: GSM8KやMATHベンチマークでの実験により、学習は3段階で進行することがわかった。
    1.  **初期加速フェーズ**: 高い分散と特徴量の直行性が適応的スケーリングに有利に働き、学習が急速に進む。
    2.  **安定遷移フェーズ**: 比較的安定した学習が進む。
    3.  **終盤フェーズ**: 直行性の喪失により、正規化による利益が限定的になる。

# 影響・考察
GRPOは現在最も注目されているRL手法の一つであり、その挙動を理論的に裏付けた本研究は重要である。「なぜ効くのか」が分かったことで、Critic-freeなRLアルゴリズムのさらなる改良や、より効率的なハイパーパラメータ設計への道が開かれたと言える。
