# modele d'entrainement d'image de produit a partir de la bdd de Tw

# recoit une image en entree puis retourne un id ou une liste d'id de produit de la bdd(util)

# spbi_model.py
import os
import json
import sqlite3
from typing import List, Tuple, Optional, Iterable, Dict

# --- TensorFlow / Keras ---
import tensorflow as tf
from tensorflow.keras import layers, models

# --- Optional: Django ORM wiring if DJANGO_SETTINGS_MODULE is provided ---
def _maybe_setup_django():
    dj_settings = os.getenv("DJANGO_SETTINGS_MODULE")
    if dj_settings:
        import django  # type: ignore
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", dj_settings)
        django.setup()
        return True
    return False


# ----------------------------
# Data loading from database
# ----------------------------
def load_data_from_django(
    app_label: str,
    model_name: str,
    image_field: str = "image",
    id_field: str = "id",
    queryset_filter: Optional[dict] = None,
) -> List[Tuple[str, int]]:
    """
    Load (image_path, id) using Django ORM.
    Assumes a model like MyApp.MyModel with an ImageField/FileField at `image_field`.

    Returns list of tuples: (filesystem_path_or_url, id)
    """
    from django.apps import apps  # type: ignore

    Model = apps.get_model(app_label, model_name)
    qs = Model.objects.all()
    if queryset_filter:
        qs = qs.filter(**queryset_filter)

    records: List[Tuple[str, int]] = []
    for obj in qs.iterator():
        img = getattr(obj, image_field, None)
        if not img:
            continue
        # handle ImageField/FileField (.path may fail if stored remotely; then use .url)
        img_path = getattr(img, "path", None) or getattr(img, "url", None)
        if not img_path:
            continue
        records.append((str(img_path), int(getattr(obj, id_field))))
    return records


def load_data_from_sqlite(
    sqlite_path: str,
    table: str = "products",
    id_column: str = "id",
    image_column: str = "image_path",
    where_clause: Optional[str] = None,
    params: Optional[Iterable] = None,
) -> List[Tuple[str, int]]:
    """
    Load (image_path, id) from an sqlite3 database.
    Table must have columns: `id_column` (int) and `image_column` (text path/url).
    """
    conn = sqlite3.connect(sqlite_path)
    cur = conn.cursor()
    sql = f"SELECT {id_column}, {image_column} FROM {table}"
    if where_clause:
        sql += f" WHERE {where_clause}"
    cur.execute(sql, params or [])
    rows = cur.fetchall()
    conn.close()
    # Return as (image_path, id)
    return [(row[1], int(row[0])) for row in rows]


# ----------------------------
# tf.data pipeline utilities
# ----------------------------
def _build_class_index(ids: List[int]) -> Tuple[Dict[int, int], Dict[int, int]]:
    """
    Build mappings:
      dbid_to_class: DB id -> 0..C-1
      class_to_dbid: 0..C-1 -> DB id
    """
    unique_ids = sorted(set(ids))
    dbid_to_class = {dbid: idx for idx, dbid in enumerate(unique_ids)}
    class_to_dbid = {idx: dbid for dbid, idx in dbid_to_class.items()}
    return dbid_to_class, class_to_dbid


def _load_image(path: tf.Tensor, target_size: Tuple[int, int]) -> tf.Tensor:
    """
    Robust image loader for local path or URL. If it's a URL, tf.io.read_file won't work directly.
    For remote URLs, you could extend this with `tf.keras.utils.get_file` first.
    """
    # NOTE: If paths are URLs (e.g., S3), pre-download or adapt this loader.
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img, channels=3, expand_animations=False)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, target_size, antialias=True)
    return img


def make_dataset(
    samples: List[Tuple[str, int]],
    dbid_to_class: Dict[int, int],
    img_size: Tuple[int, int] = (224, 224),
    batch_size: int = 32,
    shuffle: bool = True,
    cache: bool = False,
    augment: bool = True,
) -> tf.data.Dataset:
    """
    Create a tf.data Dataset from (image_path, db_id) samples.
    """
    image_paths = [s[0] for s in samples]
    class_indices = [dbid_to_class[s[1]] for s in samples]
    ds = tf.data.Dataset.from_tensor_slices((image_paths, class_indices))

    def _map_fn(path, label):
        img = _load_image(path, img_size)
        return img, tf.cast(label, tf.int32)

    ds = ds.map(_map_fn, num_parallel_calls=tf.data.AUTOTUNE)

    if augment:
        aug = tf.keras.Sequential(
            [
                layers.RandomFlip("horizontal"),
                layers.RandomRotation(0.02),
                layers.RandomZoom(0.1),
                layers.RandomContrast(0.05),
            ],
            name="augment",
        )
        ds = ds.map(lambda x, y: (aug(x, training=True), y), num_parallel_calls=tf.data.AUTOTUNE)

    if shuffle:
        ds = ds.shuffle(buffer_size=min(len(samples), 1000))

    if cache:
        ds = ds.cache()

    ds = ds.batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return ds


# ----------------------------
# Model building / training
# ----------------------------
def build_model(
    num_classes: int,
    input_shape: Tuple[int, int, int] = (224, 224, 3),
    base_trainable: bool = False,
) -> tf.keras.Model:
    """
    Transfer learning classifier using MobileNetV2 backbone.
    """
    base = tf.keras.applications.MobileNetV2(
        input_shape=input_shape, include_top=False, weights="imagenet"
    )
    base.trainable = base_trainable

    inputs = layers.Input(shape=input_shape)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(inputs)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs, name="spbi_classifier")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train_and_save(
    samples: List[Tuple[str, int]],
    model_path: str = "spbi_model.keras",
    class_index_path: str = "class_index.json",
    img_size: Tuple[int, int] = (224, 224),
    batch_size: int = 32,
    val_split: float = 0.1,
    epochs: int = 5,
) -> None:
    """
    Train the model on provided samples and save model + class index mapping.
    """
    assert len(samples) > 1, "Not enough samples to train."

    ids = [s[1] for s in samples]
    dbid_to_class, class_to_dbid = _build_class_index(ids)

    # Train/val split
    n_total = len(samples)
    n_val = max(1, int(n_total * val_split))
    train_samples = samples[:-n_val] if n_val < n_total else samples
    val_samples = samples[-n_val:] if n_val < n_total else samples[:0]

    train_ds = make_dataset(train_samples, dbid_to_class, img_size=img_size, batch_size=batch_size, augment=True)
    val_ds = make_dataset(val_samples, dbid_to_class, img_size=img_size, batch_size=batch_size, augment=False) if val_samples else None

    num_classes = len(class_to_dbid)
    model = build_model(num_classes=num_classes, input_shape=(*img_size, 3))

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=3, restore_best_weights=True)
        if val_ds is not None
        else tf.keras.callbacks.EarlyStopping(monitor="accuracy", patience=3, restore_best_weights=True)
    ]

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
    )

    # Save model + mapping
    model.save(model_path)
    with open(class_index_path, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in class_to_dbid.items()}, f, ensure_ascii=False, indent=2)


# ----------------------------
# Inference
# ----------------------------
def _load_class_index(class_index_path: str) -> Dict[int, int]:
    with open(class_index_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    # keys were saved as strings
    return {int(k): int(v) for k, v in raw.items()}


def _prepare_single_image(image_path: str, img_size: Tuple[int, int]) -> tf.Tensor:
    img = tf.io.read_file(image_path)
    img = tf.image.decode_image(img, channels=3, expand_animations=False)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, img_size, antialias=True)
    img = tf.expand_dims(img, 0)  # (1, H, W, 3)
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    return img


def predict_top_k(
    image_path: str,
    model_path: str = "spbi_model.keras",
    class_index_path: str = "class_index.json",
    k: int = 5,
    img_size: Tuple[int, int] = (224, 224),
) -> List[Tuple[int, float]]:
    """
    Predict top-k DB IDs for a given image file.
    Returns a list of (product_id, score).
    """
    model = tf.keras.models.load_model(model_path)
    class_to_dbid = _load_class_index(class_index_path)

    x = _prepare_single_image(image_path, img_size)
    preds = model.predict(x, verbose=0)[0]  # shape (C,)

    topk = tf.math.top_k(preds, k=min(k, preds.shape[0]))
    top_indices = topk.indices.numpy().tolist()
    top_scores = topk.values.numpy().tolist()

    return [(class_to_dbid[idx], float(score)) for idx, score in zip(top_indices, top_scores)]



# ----------------------------
# High-level convenience
# ----------------------------
def build_training_samples(
    use_django: bool = False,
    django_app_label: Optional[str] = None,
    django_model_name: Optional[str] = None,
    django_image_field: str = "image",
    django_id_field: str = "id",
    django_filter: Optional[dict] = None,
    sqlite_path: Optional[str] = None,
    table: str = "products",
    id_column: str = "id",
    image_column: str = "image_path",
    where_clause: Optional[str] = None,
    params: Optional[Iterable] = None,
) -> List[Tuple[str, int]]:
    """
    Wrapper to build [(image_path, id), ...] from either Django ORM or SQLite.
    """
    if use_django:
        if not _maybe_setup_django():
            raise RuntimeError("DJANGO_SETTINGS_MODULE not set. Cannot use Django ORM mode.")
        if not (django_app_label and django_model_name):
            raise ValueError("Provide django_app_label and django_model_name for Django ORM mode.")
        return load_data_from_django(
            app_label=django_app_label,
            model_name=django_model_name,
            image_field=django_image_field,
            id_field=django_id_field,
            queryset_filter=django_filter,
        )
    else:
        if not sqlite_path:
            raise ValueError("Provide sqlite_path for SQL mode.")
        return load_data_from_sqlite(
            sqlite_path=sqlite_path,
            table=table,
            id_column=id_column,
            image_column=image_column,
            where_clause=where_clause,
            params=params,
        )


# ----------------------------
# Example CLI usage
# ----------------------------
if __name__ == "__main__":
    """
    Examples:

    # --- Django ORM mode ---
    export DJANGO_SETTINGS_MODULE="myproject.settings"
    python spbi_model.py train \
        --mode django \
        --app myapp \
        --model Product \
        --image_field image \
        --id_field id \
        --model_path spbi_model.keras \
        --index_path class_index.json

    # --- SQLite mode ---
    python spbi_model.py train \
        --mode sqlite \
        --sqlite /path/to/db.sqlite3 \
        --table products \
        --id_col id \
        --img_col image_path

    # --- Predict ---
    python spbi_model.py predict --image /path/to/img.jpg
    """
    import argparse

    parser = argparse.ArgumentParser(description="SPBI TensorFlow Image→IDs model")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_train = sub.add_parser("train", help="Train the model")
    p_train.add_argument("--mode", choices=["django", "sqlite"], default="django")
    p_train.add_argument("--app", dest="app_label", default=None)
    p_train.add_argument("--model", dest="model_name", default=None)
    p_train.add_argument("--image_field", default="image")
    p_train.add_argument("--id_field", default="id")
    p_train.add_argument("--sqlite", dest="sqlite_path", default=None)
    p_train.add_argument("--table", default="products")
    p_train.add_argument("--id_col", default="id")
    p_train.add_argument("--img_col", default="image_path")
    p_train.add_argument("--model_path", default="spbi_model.keras")
    p_train.add_argument("--index_path", default="class_index.json")
    p_train.add_argument("--img_size", type=int, nargs=2, default=(224, 224))
    p_train.add_argument("--batch", type=int, default=32)
    p_train.add_argument("--epochs", type=int, default=5)
    p_train.add_argument("--val_split", type=float, default=0.1)

    p_pred = sub.add_parser("predict", help="Predict top-k IDs for an image")
    p_pred.add_argument("--image", required=True)
    p_pred.add_argument("--model_path", default="spbi_model.keras")
    p_pred.add_argument("--index_path", default="class_index.json")
    p_pred.add_argument("--k", type=int, default=5)
    p_pred.add_argument("--img_size", type=int, nargs=2, default=(224, 224))

    args = parser.parse_args()

    if args.cmd == "train":
        if args.mode == "django":
            samples = build_training_samples(
                use_django=True,
                django_app_label=args.app_label,
                django_model_name=args.model_name,
                django_image_field=args.image_field,
                django_id_field=args.id_field,
            )
        else:
            samples = build_training_samples(
                use_django=False,
                sqlite_path=args.sqlite_path,
                table=args.table,
                id_column=args.id_col,
                image_column=args.img_col,
            )

        print(f"[INFO] Loaded {len(samples)} samples")
        train_and_save(
            samples=samples,
            model_path=args.model_path,
            class_index_path=args.index_path,
            img_size=tuple(args.img_size),
            batch_size=args.batch,
            epochs=args.epochs,
            val_split=args.val_split,
        )
        print(f"[OK] Saved model to {args.model_path} and index to {args.index_path}")

    elif args.cmd == "predict":
        ids = predict_top_k(
            image_path=args.image,
            model_path=args.model_path,
            class_index_path=args.index_path,
            k=args.k,
            img_size=tuple(args.img_size),
        )
        print(json.dumps({"top_ids": ids}, ensure_ascii=False))

