# AI開発フローの実験: Google Stitchでデザイン、Antigravityで実装

## 参照元
- [Qiita: UIデザインから実装までをAIエージェントに丸投げしてみた](https://qiita.com/kunitomo926/items/205aa17d0acc88a34bf4?utm_campaign=popular_items&utm_medium=feed&utm_source=popular_items)

## 3行まとめ
- **「ChatGPTで要件定義 → Google StitchでUI生成 → Antigravity × Claude Opus 4.5でFlutter実装」という完全AI任せの開発フローを検証。**
- **Google Stitchはプロンプトから高品質なUIデザインを生成し、AntigravityはMCP（Model Context Protocol）経由でこれを読み込み、コードに変換。**
- **ワイヤーフレーム作成や手動コーディングなしで、シミュレータでの起動まで到達。ツール間の連携（MCP）が鍵となった。**

## 詳細
この記事は、最新のAIツールを組み合わせることで、どこまで人間の手を介さずにアプリ開発ができるかを実験したレポートです。

### ワークフロー
1.  **ChatGPT**: Google Stitchへの指示用プロンプトを作成。
2.  **Google Stitch**: 指示に基づき、旅行アプリのUI（言語選択、チェックリスト、ダッシュボード等）を生成。
3.  **Antigravity (Agent Manager)**: MCPサーバー設定を行い、Google Stitchをツールとして認識させる。
4.  **Claude Opus 4.5**: Antigravity上で動作し、生成されたUIデザインをもとにFlutterコードを実装。

結果として、複雑な画面遷移を含むアプリが、ほぼ自動でコンパイル・実行可能な状態まで組み上がりました。

## 所感
「Google Stitch」というツール（おそらくGoogle Labs系のプロトタイプ含め）と、エージェント環境「Antigravity」の連携事例として非常に興味深いです。特に重要なのは、これらをつなぐ**MCP (Model Context Protocol)** の役割です。デザインツールとコーディングエージェントが共通のプロトコルで会話することで、「画像のスクショを渡して終わり」ではなく、構造化されたデザインデータを元にした正確な実装が可能になっています。デザインから実装までの「死の谷」をAIが埋めつつあることを実感させます。
