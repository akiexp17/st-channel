# Xcode 26.3、Agentic Coding機能を統合へ——OpenAIとAnthropicとの連携を強化

## 参照元
- [TechCrunch: Xcode moves into agentic coding with deeper OpenAI and Anthropic integrations](https://techcrunch.com/2026/02/03/xcode-moves-into-agentic-coding-with-deeper-openai-and-anthropic-integrations/)

## 3行まとめ
- **Xcode 26.3がリリースされ、AnthropicのClaude AgentとOpenAIのCodexを含むAgentic Coding機能が統合された。**
- **MCP（Model Context Protocol）を採用し、外部のエージェントツールとXcodeの機能（プロジェクト探索、ビルド、テスト、ドキュメント参照）をシームレスに連携。**
- **AIエージェントは自律的に計画、コーディング、テスト、エラー修正を行い、開発者はそのプロセスを可視化・管理できる。**

## 詳細
Appleは火曜日、Xcode 26.3のリリースを発表し、本格的な「Agentic Coding（エージェント型コーディング）」機能を導入しました。昨年導入されたChatGPTやClaudeの統合を一歩進め、今回はAIモデルが単なるコード提案にとどまらず、プロジェクト全体の構造理解、ファイルの変更、ビルド、テスト、そしてエラー修正までを自律的に行えるようになります。

### 主な特徴
- **深い統合**: AnthropicのClaude AgentおよびOpenAIのCodexがXcode内で直接動作し、Appleの最新の開発者ドキュメントやAPIにアクセスしながらコーディングを行います。
- **MCPの採用**: XcodeはMCP（Model Context Protocol）を活用して、外部のMCP対応エージェントと接続。これにより、プロジェクトのディスカバリーやファイル操作などが標準化されたプロトコルで行われます。
- **自律的なワークフロー**: エージェントはタスクを小さなステップに分解し、ドキュメントを参照してからコーディングを開始。変更内容はリアルタイムで可視化され、開発者はいつでも以前の状態にロールバック可能です。
- **教育的側面**: エージェントの思考プロセスや変更履歴がトランスクリプトとして表示されるため、特に新しい開発者がコードの仕組みを学ぶのに役立つとされています。

## 所感
ついにXcodeがIDEとして「エージェントネイティブ」な進化を遂げました。特に注目すべきはMCPの採用で、これによりAppleの閉じたエコシステムと外部の強力なAIモデルが標準プロトコルで繋がることになります。WindsurfやCursorといったAIエディタが先行していましたが、公式のXcodeがこれをネイティブサポートすることで、iOS/macOS開発のワークフローは劇的に変わるでしょう。「エージェントに設計させて、人間はレビューする」というスタイルが、モバイルアプリ開発でも標準になりそうです。
