# Holo2-235B-A22B: UIローカリゼーションでSOTAを達成した巨大モデル

## 参照元
- [Hugging Face Blog: H Company's new Holo2 model takes the lead in UI Localization](https://huggingface.co/blog/Hcompany/introducing-holo2-235b-a22b)

## 3行まとめ
- **H Companyが、UI要素の特定（ローカリゼーション）に特化したモデル「Holo2-235B-A22B Preview」を公開。**
- **ScreenSpot-Proベンチマークで78.5%というState-of-the-Art (SOTA) スコアを記録し、既存のモデルを大きく上回る性能を実証。**
- **「Agentic Localization」手法を採用し、一度の推論で決めるのではなく、ステップごとに座標を修正・洗練させることで精度を向上。**

## 詳細
UI操作自動化（GUI Agent）において最も難しいのが「画面上のどこにボタンがあるか（Grounding）」を正確に当てることです。4Kモニタのような高解像度環境では特に困難ですが、Holo2の新モデルはこの壁を突破しました。

### 技術的ポイント
- **Agentic Localization**: モデルが自身の予測結果を反復的に見直し（Refinement）、ターゲットへの「ズームイン」や「位置修正」を行うことで、10〜20%の精度向上を実現しています。
- **性能**: OSWorld Gベンチマークでも79.0%を記録しており、WebUIだけでなくOSレベルの複雑な画面操作でも高い認識能力を持ちます。

## 所感
GUIエージェントの実用化における最大のボトルネックの一つが「ボタンの押し間違い」です。Holo2のアプローチは、人間が細かい文字を読むときに目を凝らす動作に似ています。「一発で当てる」のではなく「確認しながら探す」というエージェント的な振る舞いをローカリゼーション（位置特定）そのものに組み込んだ点が画期的です。
