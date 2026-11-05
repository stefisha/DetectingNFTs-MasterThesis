"""Optional offline checks against an already installed TensorFlow/Pillow runtime."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from test_notebooks import execute, functions


@unittest.skipUnless(
    importlib.util.find_spec("tensorflow") and importlib.util.find_spec("PIL"),
    "Optional TensorFlow/Pillow runtime is not installed",
)
class FrameworkTests(unittest.TestCase):
    def test_image_loading_rgb_dtype_and_unreadable_files(self):
        from PIL import Image, UnidentifiedImageError

        ns = functions(
            "Images_NFTs_Master.ipynb",
            6,
            {
                "np": np,
                "Image": Image,
                "UnidentifiedImageError": UnidentifiedImageError,
            },
        )
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "grayscale.png"
            broken = Path(directory) / "broken.png"
            Image.new("L", (8, 8), 128).save(image)
            broken.write_bytes(b"not an image")
            data, labels = ns["load_and_preprocess_images"]([image, broken], "legit")
            self.assertEqual(labels, ["legit"])
            self.assertEqual(data[0].shape, (128, 128, 3))
            self.assertEqual(data[0].dtype, np.float32)
            np.testing.assert_allclose(data[0], 128 / 255)
            with self.assertRaisesRegex(ValueError, "No readable images"):
                ns["load_and_preprocess_images"]([], "scam")

    def test_real_imagenet_preprocessing_preserves_shared_input(self):
        from tensorflow.keras.applications.resnet50 import preprocess_input as resnet
        from tensorflow.keras.applications.vgg16 import preprocess_input as vgg

        ns = functions("Images_NFTs_Master.ipynb", 6, {"np": np})
        images = np.array([[[[0.1, 0.2, 0.3]]]], dtype=np.float32)
        original = images.copy()
        for preprocess in (resnet, vgg):
            actual = ns["imagenet_inputs"](images, preprocess)
            np.testing.assert_allclose(actual, preprocess(original.copy() * 255))
            np.testing.assert_array_equal(images, original)

    def test_domain_sequences_validation_callbacks_and_forward_pass(self):
        from tensorflow.keras.preprocessing.text import Tokenizer
        from tensorflow.keras.preprocessing.sequence import pad_sequences
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import (
            Embedding,
            Bidirectional,
            LSTM,
            Dropout,
            Dense,
        )
        from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

        train = pd.DataFrame(
            {"url": [f"collection{i}.test" for i in range(80)], "label": [0, 1] * 40}
        )
        test = pd.DataFrame(
            {"url": ["unseen-Ω.test", "other.test"], "label": [1, 0]}, index=[100, 101]
        )
        classical_test = object()
        ns = dict(
            domain_train=train,
            domain_test=test,
            train_test_split=train_test_split,
            Tokenizer=Tokenizer,
            pad_sequences=pad_sequences,
            Sequential=Sequential,
            Embedding=Embedding,
            Bidirectional=Bidirectional,
            LSTM=LSTM,
            Dropout=Dropout,
            Dense=Dense,
            EarlyStopping=EarlyStopping,
            ModelCheckpoint=ModelCheckpoint,
            X_test=classical_test,
        )
        for position in (42, 43, 44, 45):
            execute("Domains_NFT_Master.ipynb", position, ns)
        self.assertIs(ns["X_test"], classical_test)
        self.assertTrue(
            set(ns["sequence_train"].index).isdisjoint(ns["sequence_val"].index)
        )
        self.assertNotIn("ω", ns["tokenizer"].word_index)
        self.assertIn(ns["tokenizer"].word_index["[UNK]"], ns["X_test_seq"][0])
        np.testing.assert_array_equal(ns["y_test_seq"], [1, 0])
        prediction = ns["model"](ns["X_test_seq"], training=False).numpy()
        self.assertEqual(prediction.shape, (2, 1))
        self.assertTrue(((prediction >= 0) & (prediction <= 1)).all())
        calls = {}

        class RecordingModel:
            def fit(self, *args, **kwargs):
                calls.update(kwargs)
                return object()

        ns["model"] = RecordingModel()
        execute("Domains_NFT_Master.ipynb", 46, ns)
        self.assertIs(calls["validation_data"][0], ns["X_val_seq"])
        self.assertEqual(
            calls["callbacks"], [ns["early_stopping"], ns["model_checkpoint"]]
        )


if __name__ == "__main__":
    unittest.main()
