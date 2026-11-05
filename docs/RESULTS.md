# Results and provenance

The tables below transcribe the results reported in the author-provided September 2023 thesis, *Примена вештачке интелигенције за препознавање лажних и малициозних NFT-ева*. The manuscript has not been published or redistributed in this repository. Printed page numbers below differ from PDF page indices by one because the cover is unnumbered.

These are historical reported measurements. No training or independent benchmark reproduction was performed as part of the repository presentation update.

## Thesis Table 4 — image classification

Printed page 57.

| Model | Reported accuracy |
| --- | ---: |
| Custom CNN | 98.36% |
| ResNet50 | 95.08% |
| VGG16 | 97.89% |
| RNN / LSTM | 97.89% |
| Hybrid ResNet50 + CNN | 98.17% |

## Thesis Table 5 — description classification

Printed page 59. The notebook instantiates `DistilBertForSequenceClassification`; the thesis table uses the broader label “BERT.”

| Model | Reported accuracy |
| --- | ---: |
| Logistic Regression | 93.84% |
| XGBoost | 94.78% |
| Random Forest | 94.83% |
| SVC | 93.96% |
| K-nearest neighbors | 94.70% |
| Decision tree | 94.62% |
| BERT, as labeled in the thesis | 94.33% |
| Feedforward neural network | 92.92% |

## Thesis Table 6 — collection-domain classification

Printed page 61. Some corresponding notebook experiments are commented out or lack saved outputs; this table is a manuscript record, not evidence that every row can be reproduced from the checked-in execution state.

| Model | Reported accuracy |
| --- | ---: |
| Random Forest | 81.87% |
| Random Forest with bagging | 80.86% |
| Random Forest with SMOTE | 81.47% |
| LightGBM | 79.63% |
| XGBoost | 84.32% |
| SVC | 77.18% |
| Random Forest + XGBoost ensemble | 83.91% |
| LSTM | 80.24% |
| GRU | 79.23% |

## Differences in saved notebook outputs

Notebook cell numbers here are one-based positions in the file, including markdown cells. The presentation update retains the cell order and the original experiment outputs.

| Notebook and cell | Saved output | Related thesis result |
| --- | --- | --- |
| [Image notebook](../Images_NFTs_Master.ipynb), cell 20 | CNN test accuracy `0.9859485030174255` (about 98.59%) | 98.36% |
| [Image notebook](../Images_NFTs_Master.ipynb), cell 45 | VGG16 test accuracy `0.3793911039829254` (about 37.94%) | 97.89% |
| [Image notebook](../Images_NFTs_Master.ipynb), cell 47 | Hybrid test accuracy `0.7845` (78.45%) | 98.17% |
| [Description notebook](../Metadata_NFTs_Master.ipynb), cell 38 | Text-classifier accuracy 94.21% | BERT: 94.33% |
| [Description notebook](../Metadata_NFTs_Master.ipynb), cell 41 | FNN accuracy 93.12%; cell 42 narrative states 93.68% | FNN: 92.92% |
| [Domain notebook](../Domains_NFT_Master.ipynb), cell 19 | Random Forest accuracy 79.43% | 81.87% |

The repository does not record enough run identifiers, frozen environments, datasets, or checkpoints to resolve these differences confidently. Possible explanations such as different runs or execution order remain hypotheses. Neither the original outputs nor the thesis figures have been silently replaced.

## Interpretation

- Each modality uses a different dataset and may use different split and preprocessing procedures. Ranking modalities by accuracy alone is not a controlled ablation study.
- Accuracy does not fully describe performance under class imbalance. Precision, recall, F1, confusion matrices, and error costs should accompany future comparisons.
- The image notebook computes `roc_auc_score` from predicted class labels in several cells. Those values are threshold-specific; future ranking-based ROC-AUC should use positive-class scores or probabilities.
- The reported accuracies do not establish performance on unseen NFT collections, later scam campaigns, or a live production distribution.
