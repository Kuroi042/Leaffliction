import os
import sys
import json
import zipfile
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

#config
IMG_SIZE    = (224, 224)
BATCH_SIZE  = 32
EPOCHS      = 30
SEED        = 42

def load_datasets(data_dir):
        train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=SEED,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical",
    )
 
        val_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed=SEED,
            image_size=IMG_SIZE,
            batch_size=BATCH_SIZE,
            label_mode="categorical",
        )
    
        class_names = train_ds.class_names
        print(f"\n✅ Classes found ({len(class_names)}): {class_names}\n")
    
        # Performance optimization: cache and prefetch
        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
        val_ds   = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    
        return train_ds, val_ds, class_names

def build_model(num_classes):
    """
    Transfer learning with MobileNetV2 pretrained on ImageNet.
    We freeze the base and only train the classification head.
    """
    # Normalization layer (scales pixels 0-255 → 0-1 expected by MobileNetV2)
    preprocess = tf.keras.applications.mobilenet_v2.preprocess_input
 
    base_model = MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,   # remove ImageNet classifier
        weights="imagenet",
    )
    base_model.trainable = False  # freeze pretrained weights
 
    inputs = tf.keras.Input(shape=(*IMG_SIZE, 3))
    x = preprocess(inputs)           # normalize
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)
 
    model = models.Model(inputs, outputs)
 
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
 
    model.summary()
    return model

def fine_tune(model, train_ds, val_ds, unfreeze_from=100):
    """
    Optional second training phase: unfreeze top layers of base model
    for fine-tuning with a very low learning rate.
    """
    base_model = model.layers[3]  # MobileNetV2 layer
    base_model.trainable = True
 
    # Freeze all layers except the top `unfreeze_from`
    for layer in base_model.layers[:-unfreeze_from]:
        layer.trainable = False
 
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
 
    print("\n🔧 Fine-tuning top layers...\n")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=10,
        callbacks=[
            EarlyStopping(monitor="val_accuracy", patience=5, restore_best_weights=True),
        ],
    )
    return history

def save_results(model, class_names, output_zip="model.zip"):
    """Save model + class names into a zip file (as required by subject)."""
    os.makedirs("model_output", exist_ok=True)
 
    model_path = "model_output/model.keras"
    model.save(model_path)
 
    classes_path = "model_output/class_names.json"
    with open(classes_path, "w") as f:
        json.dump(class_names, f)
 
    with zipfile.ZipFile(output_zip, "w") as zf:
        zf.write(model_path, arcname="model.keras")
        zf.write(classes_path, arcname="class_names.json")
 

def evaluate(model, val_ds, class_names):
    """Print final validation accuracy."""
    loss, acc = model.evaluate(val_ds, verbose=0)
    print(f"\n📊 Validation Accuracy : {acc * 100:.2f}%")
    print(f"📊 Validation Loss     : {loss:.4f}")
    if acc >= 0.90:
        print("✅ Accuracy above 90% — project requirement met!")
    else:
        print("⚠️  Accuracy below 90% — consider more epochs or fine-tuning.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python train.py <dataset_directory>")
        print("Example: python train.py ./Apple/")
        sys.exit(1)
 
    data_dir = sys.argv[1]
    if not os.path.isdir(data_dir):
        print(f"Error: '{data_dir}' is not a valid directory.")
        sys.exit(1)
 
    print(f"\n📂 Loading dataset from: {data_dir}")
    train_ds, val_ds, class_names = load_datasets(data_dir)
 
    num_classes = len(class_names)
    print(f"\n🏗️  Building model for {num_classes} classes...")
    model = build_model(num_classes)
 
    # ── Phase 1: Train only the head ─────────────────
    print("\n🚀 Phase 1: Training classification head...\n")
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        callbacks=[
            ModelCheckpoint(
                "model_output/best_model.keras",
                monitor="val_accuracy",
                save_best_only=True,
                verbose=1,
            ),
            EarlyStopping(
                monitor="val_accuracy",
                patience=7,
                restore_best_weights=True,
                verbose=1,
            ),
        ],
    )
 
    # ── Phase 2: Fine-tune top layers ────────────────
    fine_tune(model, train_ds, val_ds)
 
    # ── Evaluate & Save ───────────────────────────────
    evaluate(model, val_ds, class_names)
    save_results(model, class_names, output_zip="model.zip")
 
 
if __name__ == "__main__":
    main()