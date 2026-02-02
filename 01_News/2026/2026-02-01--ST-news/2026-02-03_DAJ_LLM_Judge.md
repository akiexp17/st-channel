# DAJ: Data-Reweighted LLM Judge for Test-Time Scaling in Code Generation

> [!info] 引用元
> [DAJ: Data-Reweighted LLM Judge for Test-Time Scaling in Code Generation](https://arxiv.org/abs/2601.22230)

# 概要
コード生成におけるTest-Time Scaling（推論時の計算量増加による性能向上）のための新しいLLM Judge学習フレームワーク「DAJ」の提案。データの重要度を重み付け（Reweighting）して学習させることで、SOTA性能を達成した。

# 背景
推論時に複数の候補を生成して最良のものを選ぶ「Best-of-N」手法は有効だが、その選定を行う評価モデル（Judge）の学習が難しい。学習データとテストデータの分布のズレや、安価なモデルで生成した学習データの質の問題があるためである。

# 詳細
- **Bi-level Data Reweighting**: ターゲットとなるベンチマーク（メタセット）での汎化性能が最大化されるように、学習データの重み（ドメインレベルまたはインスタンスレベル）を自動的に学習するフレームワークを採用。
- **効果**: 手作業によるヒューリスティクスなしに、難易度の高い問題や、分布の合ったデータ、正しい推論軌跡を持つデータを自動的に重視して学習できる。
- **成果**: LiveCodeBenchやBigCodeBenchにおいて、既存の強力なベースラインやプロプライエタリモデルを上回るSOTA性能を達成。

# 影響・考察
OpenAI o1やDeepSeek-R1のような「推論モデル」のトレンドの中で、生成された回答の良し悪しを判定する「Reward Model / Judge Model」の重要性が高まっている。DAJのアプローチは、Judgeモデルを効率的に学習させるためのデータ中心のAI（Data-Centric AI）アプローチとして有望である。
