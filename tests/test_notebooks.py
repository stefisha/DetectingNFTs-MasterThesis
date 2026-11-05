"""Offline regression checks for notebook code, using synthetic examples only.

No research data, training, pretrained weights, or network access is required.
"""

import ast
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]


def cell(notebook, position):
    contents = json.loads((ROOT / notebook).read_text(encoding="utf-8"))
    return "".join(contents["cells"][position - 1]["source"])


def execute(notebook, position, namespace):
    with redirect_stdout(io.StringIO()):
        exec(
            compile(cell(notebook, position), f"{notebook}:cell-{position}", "exec"),
            namespace,
        )


def functions(notebook, position, namespace):
    tree = ast.parse(cell(notebook, position))
    tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    exec(compile(tree, f"{notebook}:cell-{position}", "exec"), namespace)
    return namespace


class NotebookTests(unittest.TestCase):
    def test_missing_data_has_actionable_error(self):
        for name, position in (
            ("Images_NFTs_Master.ipynb", 3),
            ("Metadata_NFTs_Master.ipynb", 5),
            ("Domains_NFT_Master.ipynb", 4),
        ):
            with (
                self.subTest(notebook=name),
                tempfile.TemporaryDirectory() as directory,
            ):
                ns = functions(name, position, {"DATA_ROOT": Path(directory)})
                with self.assertRaisesRegex(FileNotFoundError, "NFT_DATA_ROOT"):
                    ns["require_data_path"]("missing.csv")
                existing = Path(directory) / "present.csv"
                existing.touch()
                self.assertEqual(ns["require_data_path"]("present.csv"), existing)

    def test_imagenet_preprocessing_does_not_mutate_shared_images(self):
        ns = functions("Images_NFTs_Master.ipynb", 6, {"np": np})
        images = np.full((2, 4, 4, 3), 0.5, dtype=np.float32)
        original = images.copy()

        def mutating_preprocess(pixels):
            pixels -= 100
            return pixels

        result = ns["imagenet_inputs"](images, mutating_preprocess)
        np.testing.assert_array_equal(images, original)
        np.testing.assert_allclose(result, 27.5)
        self.assertFalse(np.shares_memory(images, result))

    def test_image_roc_uses_probability_ranking(self):
        # Every probability is below 0.5; class labels lose the perfect ranking.
        labels = np.array([0, 1, 0, 1])
        probabilities = np.array([0.1, 0.4, 0.2, 0.3])
        predictions = np.column_stack([1 - probabilities, probabilities])
        ns = {
            "np": np,
            "model": SimpleNamespace(predict=lambda _: predictions),
            "X_test_reshaped": np.zeros((4, 1)),
            "y_test": np.eye(2)[labels],
            "classification_report": lambda *args: "synthetic report",
            "confusion_matrix": confusion_matrix,
            "roc_auc_score": roc_auc_score,
        }
        execute("Images_NFTs_Master.ipynb", 22, ns)
        self.assertEqual(ns["roc_auc"], 1.0)
        self.assertEqual(roc_auc_score(labels, predictions.argmax(axis=1)), 0.5)

    def synthetic_text(self):
        return pd.DataFrame(
            {
                "processed_content": [
                    f"collection item{i} artwork" for i in range(100)
                ],
                "label": [0, 1] * 50,
            }
        )

    def test_tfidf_excludes_test_vocabulary(self):
        frame = self.synthetic_text()
        _, test = train_test_split(
            frame, test_size=0.2, random_state=42, stratify=frame.label
        )
        frame.loc[test.index, "processed_content"] += " holdoutsecret"
        ns = {
            "combined_data": frame,
            "train_test_split": train_test_split,
            "TfidfVectorizer": TfidfVectorizer,
        }
        execute("Metadata_NFTs_Master.ipynb", 14, ns)
        self.assertNotIn("holdoutsecret", ns["tfidf_vectorizer"].vocabulary_)
        self.assertTrue(set(ns["text_train"].index).isdisjoint(ns["text_test"].index))
        self.assertEqual(ns["X_train_idf"].shape[1], ns["X_test_idf"].shape[1])

    def test_description_preprocessing_handles_empty_and_numeric_values(self):
        import re

        ns = functions(
            "Metadata_NFTs_Master.ipynb",
            12,
            {"pd": pd, "re": re, "ENGLISH_STOP_WORDS": ENGLISH_STOP_WORDS},
        )
        preprocess = ns["preprocess_text"]
        self.assertEqual(preprocess(None), "")
        self.assertEqual(preprocess(12345), "")
        self.assertEqual(preprocess("ARTWORK https://example.test 42"), "artwork")

    def test_document_vector_handles_unknown_words(self):
        ns = functions("Metadata_NFTs_Master.ipynb", 16, {"np": np})

        class Vectors:
            key_to_index = {"known": 0}

            def __getitem__(self, words):
                return np.array([[1.0, 3.0] for _ in words])

        model = SimpleNamespace(wv=Vectors(), vector_size=2)
        np.testing.assert_array_equal(ns["document_vector"](model, ["unknown"]), [0, 0])
        np.testing.assert_array_equal(
            ns["document_vector"](model, ["unknown", "known"]), [1, 3]
        )

    def test_bert_receives_text_and_separate_validation(self):
        frame = self.synthetic_text()
        text_train, text_test, y_train, y_test = train_test_split(
            frame.processed_content,
            frame.label,
            test_size=0.2,
            random_state=42,
            stratify=frame.label,
        )

        class Tokenizer:
            @classmethod
            def from_pretrained(cls, _):
                return cls()

            def __call__(self, texts, **kwargs):
                self_test.assertTrue(
                    all(
                        isinstance(text, str) and "collection" in text for text in texts
                    )
                )
                return {"input_ids": [[1, 2] for _ in texts]}

        self_test = self
        fake_transformers = SimpleNamespace(
            DistilBertTokenizer=Tokenizer,
            DistilBertForSequenceClassification=object,
            Trainer=object,
            TrainingArguments=object,
        )
        ns = {
            "train_test_split": train_test_split,
            "text_train": text_train,
            "text_test": text_test,
            "y_train_text": y_train,
            "y_test_text": y_test,
        }
        with patch.dict("sys.modules", {"transformers": fake_transformers}):
            execute("Metadata_NFTs_Master.ipynb", 30, ns)
        self.assertTrue(
            set(ns["bert_train_text"].index).isdisjoint(ns["bert_val_text"].index)
        )
        self.assertTrue(set(ns["bert_val_text"].index).isdisjoint(text_test.index))
        self.assertEqual(ns["X_test_bert"], text_test.tolist())
        self.assertEqual(ns["y_test_bert"], y_test.tolist())

    def test_domain_features_exclude_held_out_vocabulary_and_suffixes(self):
        frame = pd.DataFrame(
            {
                "url": [f"collection{i}.test" for i in range(100)],
                "domain_length": [10] * 100,
                "domain_suffix_code": ["test"] * 100,
                "label": [0, 1] * 50,
            }
        )
        _, test = train_test_split(
            frame, test_size=0.2, random_state=42, stratify=frame.label
        )
        frame.loc[test.index, "url"] = "holdoutsecret.unseen"
        frame.loc[test.index, "domain_suffix_code"] = "unseen"
        ns = {
            "pd": pd,
            "combined_data": frame,
            "train_test_split": train_test_split,
            "TfidfVectorizer": TfidfVectorizer,
        }
        execute("Domains_NFT_Master.ipynb", 15, ns)
        execute("Domains_NFT_Master.ipynb", 16, ns)
        execute("Domains_NFT_Master.ipynb", 17, ns)
        self.assertNotIn("holdoutsecret", ns["tfidf_vectorizer"].vocabulary_)
        self.assertTrue((ns["X_test"].domain_suffix_code == -1).all())
        self.assertEqual(list(ns["X_train"].columns), list(ns["X_test"].columns))
        self.assertEqual(list(ns["X_test"].index), list(ns["y_test"].index))

    def test_loo_accepts_mixed_container_types_and_preserves_holdout(self):
        ns = {"np": np}
        execute("Domains_NFT_Master.ipynb", 20, ns)
        data = pd.DataFrame({"value": [10, 20, 30, 40]}, index=[7, 3, 1, 8])
        labels = [0, 1, 0, 1]
        folds = list(ns["loo_train_test_split"](data, labels))
        self.assertEqual(len(folds), 4)
        self.assertEqual([fold[1].iloc[0, 0] for fold in folds], [10, 20, 30, 40])
        self.assertEqual([fold[3][0] for fold in folds], labels)
        ns.update(
            {
                "X_train": data,
                "y_train": labels,
                "X_test": "untouched",
                "y_test": "untouched",
                "RUN_LEAVE_ONE_OUT": True,
                "loo_models": [
                    SimpleNamespace(fit=lambda *args: None, score=lambda *args: 0.5)
                ],
            }
        )
        execute("Domains_NFT_Master.ipynb", 22, ns)
        self.assertIs(ns["X_train"], data)
        self.assertIs(ns["y_train"], labels)
        self.assertEqual(ns["X_test"], "untouched")
        self.assertEqual(ns["y_test"], "untouched")


if __name__ == "__main__":
    unittest.main()
