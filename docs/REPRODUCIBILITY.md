# Reproducibility guide

## What can be verified now

The repository preserves three exploratory notebooks, their code, and saved outputs. Readers can inspect the experiments and compare the saved evidence with [reported thesis results](RESULTS.md). Repository checks validate file structure and presentation without training models.

The original data, trained checkpoints, a frozen environment, and complete run manifests are not included. End-to-end reproduction of the thesis scores therefore cannot currently be guaranteed.

## Reviewing the notebooks

1. Read the research question and modality map in the [README](../README.md).
2. Inspect the relevant notebook from the beginning, including dataset and split cells.
3. Use [data documentation](DATA.md) to identify the required external inputs.
4. Compare saved outputs with [results provenance](RESULTS.md), keeping manuscript results distinct from notebook execution snapshots.

## Executing an experiment

1. Open the notebook through its Colab badge, or use a compatible local Jupyter environment. Private repositories require appropriate access.
2. Obtain the required datasets and confirm that you may use them.
3. Mount your own storage if needed and update the notebook's data paths.
4. Inspect the imports and any installation cells before execution. The code spans TensorFlow/Keras, scikit-learn, PyTorch/Transformers, Gensim, XGBoost, LightGBM, and imbalanced-learn.
5. Choose an environment supporting the legacy APIs used by that notebook. For example, `keras.preprocessing.text` and `keras.preprocessing.image.ImageDataGenerator` belong to older Keras workflows. A current default Colab runtime may need compatibility changes.
6. Execute cells in order from a clean kernel. Some experiments reuse variables such as `model`, `X_train`, and `y_train`; isolate a model's construction, training, and evaluation when comparing runs.
7. Record the exact environment, data checksums, seed settings, preprocessing, split assignments, hardware, and run identifier with each result.

The thesis describes Colab CPU, GPU, and TPU resources. The image notebook has GPU metadata and the description notebook has TPU metadata, but this does not establish a minimum hardware requirement or that every cell uses those accelerators. Transfer-learning weights and transformer checkpoints may require downloads.

## Split and evaluation review

The image notebook records stratified 70/15/15 splitting with `random_state=42`. Description and domain experiments mostly use 80/20 splits; not every branch uses the same stratification or validation procedure.

Before making new benchmark claims:

- Fit vocabularies, encoders, and other learned preprocessing on training data only.
- Group related NFT items by collection and control exact and near duplicates.
- Separate model selection from the final test set. Some archived sequence-model training uses the test partition as validation data.
- Use suitable positive-class scores for ROC-AUC and report class-specific errors.
- Repeat experiments across seeds and report uncertainty and class distributions.

These are recommendations for future replication, not changes made to the original research code.

## Lightweight validation

```sh
python -m pip install -r requirements-review.txt
python scripts/validate_repository.py
cffconvert --validate
```

`requirements-review.txt` is a tooling environment, not a training environment. These commands require no datasets, API credentials, model downloads, or experiment execution.
