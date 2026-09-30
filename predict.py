import os
import sys
import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
from pathlib import Path

# ─── constants ────────────────────────────────────────────────────────────────

IMG_SIZE = (224, 224)

# These are two independent classifiers.  Their softmax scores must not be
# compared with one another: each score is only meaningful within its own
# model's set of classes.
MODELS = {
    "Apple": {
        "path": "apple_model/model.keras",
        "class_names_path": "apple_model/class_names.json",
    },
    "Grape": {
        # Keep the directory name used by the trained grape model.
        "path": "grape model/model.keras",
        # image_dataset_from_directory orders these folder names alphabetically.
        "class_names": [
            "Grape_Black_rot",
            "Grape_Esca",
            "Grape_healthy",
            "Grape_spot",
        ],
    },
}


# ─── helpers ──────────────────────────────────────────────────────────────────

def load_model_and_classes(model_name: str, config: dict):
    """
    Load one trained Keras model and its list of class names.
    Returns (model, class_names).
    """
    model_path = config["path"]
    if not os.path.isfile(model_path):
        print(f"Error: {model_name} model not found at '{model_path}'.")
        sys.exit(1)

    print(f"Loading {model_name} model ...")
    model = tf.keras.models.load_model(model_path)
    print(f"{model_name} model loaded.\n")

    if "class_names_path" in config:
        with open(config["class_names_path"], "r", encoding="utf-8") as f:
            class_names = json.load(f)
    else:
        class_names = config["class_names"]

    return model, class_names


def preprocess_image(image_path: str):
    """
    Read an image from disk, resize to IMG_SIZE, and return:
      - original_rgb : HxWx3 uint8 array for display
      - tensor       : 1x224x224x3 float32 tensor for the model
    """
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        print(f"Error: could not read image at '{image_path}'.")
        sys.exit(1)

    original_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # resize for the model
    resized = cv2.resize(original_rgb, IMG_SIZE)

    # add batch dimension  →  (1, 224, 224, 3)
    tensor = np.expand_dims(resized.astype(np.float32), axis=0)

    return original_rgb, tensor


def predict(model, tensor, class_names):
    """
    Run the model on a single preprocessed image tensor.
    Returns (predicted_class_name, confidence_percentage, full_probs_dict).
    """
    probs = np.asarray(model.predict(tensor, verbose=0)[0])
    if probs.ndim != 1 or len(probs) != len(class_names):
        raise ValueError(
            "Model output has "
            f"{len(probs) if probs.ndim == 1 else probs.shape} values, but "
            f"{len(class_names)} class names were configured."
        )

    top_idx    = int(np.argmax(probs))
    top_class  = class_names[top_idx]
    confidence = float(probs[top_idx]) * 100

    # build a dict of all class probabilities for display
    all_probs = {class_names[i]: float(probs[i]) * 100
                 for i in range(len(class_names))}

    return top_class, confidence, all_probs


def display_results(image_path: str, original_rgb: np.ndarray, results: dict):
    """
    Show the input image and the class probabilities from every classifier.
    Prints each classifier's prediction to the terminal as well.
    """

    # ── terminal output ───────────────────────────────────────────────────────
    print("=" * 50)
    print(f"Image: {Path(image_path).name}")
    for model_name, (predicted_class, confidence, all_probs) in results.items():
        print("-" * 50)
        print(f"{model_name} prediction : {predicted_class}")
        print(f"{model_name} confidence : {confidence:.2f}%")
        print("Class probabilities:")
        for cls, prob in sorted(all_probs.items(), key=lambda x: -x[1]):
            bar = "█" * int(prob / 2)   # simple ascii bar
            print(f"  {cls:35s} {prob:6.2f}%  {bar}")
    print("=" * 50)

    # ── matplotlib figure ─────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, len(results) + 1, figsize=(7 * (len(results) + 1), 6))
    fig.suptitle("🌿 Leaffliction — DL Classification", fontsize=16, y=1.02)

    # left panel: original image
    axes[0].imshow(original_rgb)
    axes[0].set_title(f"Input image\n{Path(image_path).name}", fontsize=11)
    axes[0].axis("off")

    for axis, (model_name, (predicted_class, confidence, all_probs)) in zip(
        axes[1:], results.items()
    ):
        classes = list(all_probs.keys())
        probs = list(all_probs.values())
        colors = ["#2ecc71" if cls == predicted_class else "#95a5a6" for cls in classes]
        bars = axis.barh(classes, probs, color=colors)
        axis.set_xlim(0, 100)
        axis.set_xlabel("Confidence (%)", fontsize=11)
        axis.set_title(f"{model_name} class probabilities", fontsize=11)
        axis.invert_yaxis()

        for bar, prob in zip(bars, probs):
            axis.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                      f"{prob:.1f}%", va="center", fontsize=10)

        for label, cls in zip(axis.get_yticklabels(), classes):
            if cls == predicted_class:
                label.set_color("#27ae60")
                label.set_fontweight("bold")

    plt.tight_layout()
    plt.show()


# ─── entry point ──────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) != 3:
        print("Usage:   python3 predict.py <apple|grape> <image_path>")
        print("Example: python3 predict.py apple ./Apple/Apple_healthy/image.JPG")
        sys.exit(1)

    crop = sys.argv[1].lower()
    image_path = sys.argv[2]

    model_name = crop.capitalize()
    if model_name not in MODELS:
        print(f"Error: unsupported crop '{sys.argv[1]}'. Choose 'apple' or 'grape'.")
        sys.exit(1)

    if not os.path.isfile(image_path):
        print(f"Error: '{image_path}' is not a valid file.")
        sys.exit(1)

    original_rgb, tensor = preprocess_image(image_path)
    model, class_names = load_model_and_classes(model_name, MODELS[model_name])
    results = {model_name: predict(model, tensor, class_names)}

    display_results(image_path, original_rgb, results)


if __name__ == "__main__":
    main()
