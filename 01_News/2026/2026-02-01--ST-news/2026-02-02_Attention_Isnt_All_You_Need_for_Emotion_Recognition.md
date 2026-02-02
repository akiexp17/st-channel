# Attention Isn't All You Need for Emotion Recognition: ドメイン特性の重要性

> [!info] 引用元
> [Attention Isn't All You Need for Emotion Recognition: Domain Features Outperform Transformers on the EAV Dataset](https://arxiv.org/abs/2601.22161)

# 概要
感情認識（Emotion Recognition）においては、汎用的なTransformerよりも、ドメイン固有の特徴量が依然として優れているという研究結果。

# 詳細レポート
EAVデータセットを用いた感情認識タスクにおいて、最新のTransformerモデルと従来のドメイン特化型特徴量（音声の韻律や顔の表情筋パラメータなど）の性能を比較。驚くべきことに、計算コストの高いAttentionベースのモデルよりも、適切に設計されたドメイン特徴量を用いたモデルの方が高い精度を記録した。AI開発において「とりあえずTransformer」という風潮に一石を投じ、タスクの性質に応じたアーキテクチャ選択の重要性を再認識させる結果である。
