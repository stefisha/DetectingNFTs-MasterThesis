# Reproducibility guide

## What can be verified now

The repository contains three research notebooks with saved outputs. Readers can inspect the experiments and compare them with [reported thesis results](RESULTS.md). Offline checks validate notebook structure and selected code paths using synthetic inputs.

To discuss data access and reproducing the experiments, contact [Stefan Veličković](https://github.com/stefisha).

## Reviewing the notebooks

1. Read the research question and modality map in the [README](../README.md).
2. Inspect the relevant notebook from the beginning, including dataset and split cells.
3. Use [data documentation](DATA.md) to identify the required external inputs.
4. Compare saved outputs with [results provenance](RESULTS.md), keeping manuscript results distinct from notebook execution snapshots.

## Running the experiments

1. Open the notebook through its Colab badge, or use a compatible local Jupyter environment. Private repositories require appropriate access.
2. Contact the author to discuss data access, then prepare the inputs described in [data documentation](DATA.md).
3. Mount your own storage if needed and set `NFT_DATA_ROOT` to the root containing the documented `Images/`, `Metadata/`, and `Domains/` inputs. Missing inputs produce an explanatory error.
4. Inspect the imports and any installation cells before execution. The code spans TensorFlow/Keras, scikit-learn, PyTorch/Transformers, Gensim, XGBoost, LightGBM, and imbalanced-learn.
5. Choose an environment supporting the legacy APIs used by that notebook. For example, `tensorflow.keras.preprocessing.text.Tokenizer` and `tensorflow.keras.preprocessing.image.ImageDataGenerator` belong to older Keras workflows. A current default Colab runtime may need compatibility changes.
6. Execute cells in order from a clean kernel. Some experiments reuse variables such as `model`, `X_train`, and `y_train`; isolate a model's construction, training, and evaluation when comparing runs.
7. Record the exact environment, data checksums, seed settings, preprocessing, split assignments, hardware, and run identifier with each result.

The thesis describes Colab CPU, GPU, and TPU resources. The image notebook has GPU metadata and the description notebook has TPU metadata, but this does not establish a minimum hardware requirement or that every cell uses those accelerators. Transfer-learning weights and transformer checkpoints may require downloads.

## Split and evaluation review

The image source uses stratified 70/15/15 splitting with `random_state=42`. The description and domain notebooks use stratified 80/20 outer train/test splits; the transformer, description FNN, and domain recurrent branches reserve 20% of the training partition for validation. Saved outputs are historical experiment records.

Before making new benchmark claims:

- Keep learned preprocessing confined to training data; optional internal domain CV still needs a pipeline fitted separately within each fold.
- Group related NFT items by collection and control exact and near duplicates.
- Keep model selection separate from the final test set and record the exact item assignments. Sequence-model training uses a separate validation partition.
- Use suitable positive-class scores for ROC-AUC and report class-specific errors.
- Repeat experiments across seeds and report uncertainty and class distributions.

See [research notes](RESEARCH_NOTES.md) for evaluation limitations and [validation](VALIDATION.md) for the offline checks.

## Lightweight validation

```sh
python -m pip install -r requirements-test.txt
python scripts/validate_repository.py
python -m unittest discover -s tests -v
cffconvert --validate
```

`requirements-test.txt` supplies lightweight test dependencies; `requirements-review.txt` supplies documentation tooling only. Neither is a historical training lockfile. These commands require no research datasets, API credentials, model downloads, or training. Optional framework checks skip if TensorFlow/Pillow is absent. No complete clean-kernel training run is claimed.
