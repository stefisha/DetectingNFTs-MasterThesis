# Code cleanup and verification

The original research datasets are no longer available. This maintenance pass
improves code clarity and corrects identifiable defects without retraining models
or claiming to reproduce the thesis experiments.

## Historical evidence

All saved outputs, execution counts, cell metadata, and cell positions have been
retained. **They predate the edited source code and do not validate it.** In
particular, saved ROC values and model accuracies have not been recalculated.
Saved execution counts describe the historical notebook session, not a new run.

The exact source before this cleanup remains available at commit
[`c4d269b00887d0ce3039511714836d9d66d49970`](https://github.com/stefisha/DetectingNFTs-MasterThesis/tree/c4d269b00887d0ce3039511714836d9d66d49970).
The repository validator checks hashes of the historical cell evidence against
that baseline. The [results record](RESULTS.md) preserves manuscript figures and
documents discrepancies with saved outputs.

## Changes affecting future runs

| Area | Maintenance changes |
| --- | --- |
| All notebooks | Consistent formatting and TensorFlow Keras imports; configurable `NFT_DATA_ROOT`; explicit missing-input errors; defined zero-division behavior for classical precision/recall/F1 |
| Images | Close image files reliably; use float32 RGB inputs; report unreadable files and reject empty classes; sort input filenames; seed TensorFlow; compute ROC-AUC from positive-class probabilities |
| Image transfer learning | Apply the corresponding ImageNet preprocessing consistently to training, validation, and test arrays; use separate arrays so VGG16 cannot mutate shared test images; use the defined ResNet early-stopping callback; allow the LSTM learning-rate callback to reduce the rate |
| Descriptions | Split raw text before fitting TF-IDF or Word2Vec; compare representations using the same held-out items; fit embedding vocabulary on training text only |
| DistilBERT | Tokenize descriptions instead of numeric vectors converted to strings; reserve validation examples from training; use corresponding text-test labels at final evaluation |
| Description FNN | Fit a separate vocabulary on its training subset; use separate validation and the shared held-out text test set |
| Domains | Fit suffix encoding and TF-IDF on training examples only; handle unseen suffixes; omit arbitrary integer encodings of full URL identifiers |
| Domain evaluation | Keep the XGBoost module alias intact; preserve the held-out split during optional leave-one-out diagnostics; use probabilities for ROC; remove an unused native XGBoost CV parameter |
| Domain recurrent model | Fit character vocabulary and sequence length on training examples; support unknown characters; reserve validation from training; wire up early stopping and checkpoint saving; preserve the classical-model split |

These changes alter preprocessing, split usage, or model selection in future
executions. Any new metrics must be reported separately from the thesis figures.
Sorting image filenames also means future split membership may differ from the
historical, unrecorded filesystem order.

## Offline checks

```sh
python -m pip install -r requirements-test.txt
python scripts/validate_repository.py
python -m unittest discover -s tests -v
cffconvert --validate
```

The synthetic tests execute selected notebook functions and preprocessing cells.
They check missing-data errors, preservation of shared image arrays, ROC ranking,
training-only text vocabularies, unseen domain suffixes, split alignment,
description inputs for the transformer tokenizer, and leave-one-out state safety.
The transformer test uses a tokenizer substitute and downloads no model. Tests
do not measure classification performance or validate a complete training run.

Optional framework checks in `tests/test_frameworks.py` use Pillow and an installed
TensorFlow runtime for image loading, real ImageNet preprocessing, and character
tokenization. They skip when those dependencies are absent. They do not train.

Validation for this maintenance pass: all 12 tests passed using Python 3.9,
NumPy 1.26.4, pandas 2.2.3, scikit-learn 1.4.2, TensorFlow 2.17.1, and Keras 3.6.0.
Notebook syntax, historical-evidence hashes, local documentation links, and the
citation schema also passed. This records the tested checks, not a verified
environment for complete notebook training.

## Remaining research and runtime limitations

- The historical environment was not locked. A complete clean-kernel notebook run
  has not been verified. Legacy `ImageDataGenerator` and `Tokenizer` APIs remain;
  framework compatibility, including Transformers training arguments, must be
  checked in a chosen training environment.
- Optional domain leave-one-out and grid-search diagnostics reuse preprocessing
  fitted on the full training partition. Their internal CV scores are not
  leakage-free estimates. A future benchmark needs a preprocessing pipeline
  fitted separately inside each fold.
- SMOTE still operates on the original numerical domain-feature representation,
  including an ordinal suffix code. Its treatment of categorical features needs
  reconsideration before a new benchmark.
- Collection overlap, near duplicates, temporal generalization, calibration,
  external validity, and statistical uncertainty cannot be established without
  suitable data. Cleanup does not establish the validity of historical scores.

See [research notes](RESEARCH_NOTES.md) for the broader evaluation limitations.
