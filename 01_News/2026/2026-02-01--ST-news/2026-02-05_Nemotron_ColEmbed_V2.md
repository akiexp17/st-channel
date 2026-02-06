# NVIDIA、マルチモーダル検索を強化する「Nemotron ColEmbed V2」を発表

> [!info] 引用元
> [Nemotron ColEmbed V2: Raising the Bar for Multimodal Retrieval with ViDoRe V3’s Top Model](https://huggingface.co/blog/nvidia/nemotron-colembed-v2)

# 概要
NVIDIAは、マルチモーダル検索（RAG）のための最新埋め込みモデルファミリー「Nemotron ColEmbed V2」を発表した。テキストと画像の相互作用を詳細に捉える「Late Interaction」メカニズムを採用し、ViDoRe V3ベンチマークで各サイズカテゴリ（8B, 4B, 3B）のトップスコアを記録した。

# 背景
従来のRAG（検索拡張生成）ではテキスト検索が主流だったが、図表やインフォグラフィックを含む複雑なドキュメントの検索精度向上が課題となっていた。ColBERTのようなLate Interactionモデルは精度が高いが、計算・ストレージコストが高い。NVIDIAはこの手法をマルチモーダルに拡張した。

# 詳細
- **モデルラインナップ**: 8B, 4B, 3Bの3モデル。
- **アーキテクチャ**: Qwen3-VL（8B/4B）およびLlama-3.2（3B）をベースに、双方向Self-AttentionとColBERTスタイルのLate Interactionを採用。
- **MaxSim演算**: クエリトークンとドキュメントトークンの最大類似度を計算し、合計することでスコアを算出。
- **性能**: ViDoRe V3ベンチマークで1位を獲得。特に視覚的にリッチなドキュメントの検索に強み。
- **用途**: マルチメディア検索エンジン、クロスモーダル検索システム、リッチな入力理解を持つ会話AIなど。

# 影響・考察
企業のナレッジベースはPDFやスライドなど視覚情報を含むものが多く、テキスト単体の検索では限界があった。このモデルは、図表やレイアウトを考慮した高精度な検索を可能にし、エンタープライズRAGの実用性を大きく向上させる。ただし、トークン埋め込みを全て保存する必要があるため、ストレージ要件には注意が必要である。
