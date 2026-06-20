import os
import sys
import json
import zipfile
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
from pathlib import Path

# ─── constants ────────────────────────────────────────────────────────────────

IMG_SIZE   = (224, 224)
MODEL_ZIP  = "model.zip"
MODEL_FILE = "model_output/model.keras"
NAMES_FILE = "model_output/class_names.json"


# ─── helpers ──────────────────────────────────────────────────────────────────

def extract_model(zip_path: str):
    """
    Always extract fresh model.keras and class_names.json from model.zip,
    overwriting any stale model_output/ from a previous run.
    """
    if not os.path.exists(zip_path):
        print(f"Error: '{zip_path}' not found.")
        print("Make sure model.zip is in the same directory as predict.py.")
        sys.exit(1)

    if os.path.exists("model_output"):
        import shutil
        shutil.rmtree("model_output")

    print(f"Extracting model from {zip_path} ...")
    os.makedirs("model_output", exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall("model_output")
    print("Extraction done.\n")


def load_model_and_classes():
    """
    Load the trained Keras model and the list of class names.
    Returns (model, class_names).
    """
    extract_model(MODEL_ZIP)

    print("Loading model ...")
    model = tf.keras.models.load_model(MODEL_FILE)
    print("Model loaded.\n")

    with open(NAMES_FILE, "r") as f:
        class_names = json.load(f)

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
    probs      = model.predict(tensor, verbose=0)[0]   # shape: (num_classes,)
    top_idx    = int(np.argmax(probs))
    top_class  = class_names[top_idx]
    confidence = float(probs[top_idx]) * 100

    # build a dict of all class probabilities for display
    all_probs = {class_names[i]: float(probs[i]) * 100
                 for i in range(len(class_names))}

    return top_class, confidence, all_probs


def display_result(image_path: str,
                   original_rgb: np.ndarray,
                   predicted_class: str,
                   confidence: float,
                   all_probs: dict):
    """
    Show a two-panel figure:
      Left  – original image
      Right – bar chart of class probabilities
    Prints the prediction to the terminal as well.
    """

    # ── terminal output ───────────────────────────────────────────────────────
    print("=" * 50)
    print(f"Image      : {Path(image_path).name}")
    print(f"Prediction : {predicted_class}")
    print(f"Confidence : {confidence:.2f}%")
    print("-" * 50)
    print("All class probabilities:")
    for cls, prob in sorted(all_probs.items(), key=lambda x: -x[1]):
        bar = "█" * int(prob / 2)   # simple ascii bar
        print(f"  {cls:35s} {prob:6.2f}%  {bar}")
    print("=" * 50)

    # ── matplotlib figure ─────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("🌿 Leaffliction — DL Classification", fontsize=16, y=1.02)

    # left panel: original image
    axes[0].imshow(original_rgb)
    axes[0].set_title(f"Input image\n{Path(image_path).name}", fontsize=11)
    axes[0].axis("off")

    # right panel: probability bar chart
    classes = list(all_probs.keys())
    probs   = list(all_probs.values())
    colors  = ["#2ecc71" if c == predicted_class else "#95a5a6" for c in classes]

    bars = axes[1].barh(classes, probs, color=colors)
    axes[1].set_xlim(0, 100)
    axes[1].set_xlabel("Confidence (%)", fontsize=11)
    axes[1].set_title("Class probabilities", fontsize=11)
    axes[1].invert_yaxis()

    # annotate each bar with the percentage
    for bar, prob in zip(bars, probs):
        axes[1].text(
            bar.get_width() + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{prob:.1f}%",
            va="center", fontsize=10
        )

    # highlight the predicted class label in green
    for label, cls in zip(axes[1].get_yticklabels(), classes):
        if cls == predicted_class:
            label.set_color("#27ae60")
            label.set_fontweight("bold")

    plt.tight_layout()
    plt.show()


# ─── entry point ──────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) != 2:
        print("Usage:   python3 predict.py <image_path>")
        print("Example: python3 predict.py ./Apple/Apple_healthy/image.JPG")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.isfile(image_path):
        print(f"Error: '{image_path}' is not a valid file.")
        sys.exit(1)

    model, class_names = load_model_and_classes()
    original_rgb, tensor = preprocess_image(image_path)
    predicted_class, confidence, all_probs = predict(model, tensor, class_names)
    display_result(image_path, original_rgb, predicted_class, confidence, all_probs)


if __name__ == "__main__":
    main()