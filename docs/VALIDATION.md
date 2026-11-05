# Validation

```sh
python -m pip install -r requirements-test.txt
python scripts/validate_repository.py
python -m unittest discover -s tests -v
cffconvert --validate
```

The checks validate notebook syntax, saved-output integrity, documentation links,
citation and widget metadata, and selected code paths using synthetic inputs. They cover
text preprocessing, training-only vocabularies, split alignment, unknown domain
suffixes, image preprocessing, ROC ranking, and cross-validation state handling.
The transformer tokenizer is substituted during testing; no model is downloaded.

Optional framework tests use an installed TensorFlow/Pillow runtime for image
loading, ImageNet preprocessing, character tokenization, and a recurrent-model
forward pass. They skip when those dependencies are absent.

All 13 checks passed with Python 3.9, NumPy 1.26.4, pandas 2.2.3,
scikit-learn 1.4.2, TensorFlow 2.17.1, and Keras 3.6.0. These checks do not train
models or independently reproduce the thesis results.
