import os
import sys
import shutil
import itertools
import random
from pathlib import Path

from Augmentation import (
    ft_rotate,
    ft_flip,
    ft_shear,
    skew,
    ft_crop,
    distort,
)

# ─── constants ───────────────────────────────────────────────────────────────

AUG_FUNCS = [ft_rotate, ft_flip, ft_shear, skew, ft_crop, distort]

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}

AUG_TAGS = ["_Rotate", "_Flip", "_Shear", "_Skew", "_Crop", "_Distortion"]

# 80 % of originals go to train, 20 % to val — no augmented image ever
# enters the val split, so validation accuracy reflects true generalization.
VAL_SPLIT = 0.2

SEED = 42


# ─── helpers ─────────────────────────────────────────────────────────────────

def is_original(filename: str) -> bool:
    """
    Return True only for images that were NOT produced by a previous
    augmentation run (i.e. their stem contains none of the AUG_TAGS).
    """
    ext = Path(filename).suffix
    if ext not in IMAGE_EXTENSIONS:
        return False
    stem = Path(filename).stem
    return not any(tag in stem for tag in AUG_TAGS)


def collect_classes(root: Path) -> dict:
    """
    Walk root and return {class_path: [list of original image Paths]}.
    Skips any directory that contains zero original images.
    """
    classes = {}
    for current, dirs, files in os.walk(root):
        originals = [Path(current) / f for f in files if is_original(f)]
        if originals:
            classes[Path(current)] = originals
    return classes


def split_originals(images: list, val_split: float, seed: int):
    """
    Deterministically split a list of image Paths into (train, val).
    Shuffles with a fixed seed so the split is reproducible.
    """
    images = images.copy()
    random.seed(seed)
    random.shuffle(images)
    cut = int(len(images) * (1 - val_split))
    return images[:cut], images[cut:]


def copy_images(image_paths: list, destination: Path):
    """
    Copy a list of image Paths into destination, preserving filenames.
    Creates destination if it does not exist.
    """
    destination.mkdir(parents=True, exist_ok=True)
    for src in image_paths:
        shutil.copy2(src, destination / src.name)


def augment_to_target(train_dir: Path, target: int):
    """
    Augment images inside train_dir (in-place) until the total image
    count reaches `target`.  Only original images are used as sources —
    augmented files are never re-augmented.
    """
    # count what is already there
    current_files = [
        f for f in train_dir.iterdir()
        if f.suffix in IMAGE_EXTENSIONS
    ]
    current_originals = [f for f in current_files if is_original(f.name)]
    current_total     = len(current_files)

    needed = target - current_total
    if needed <= 0:
        print(f"    ✅  already has {current_total} images — no augmentation needed.")
        return

    print(f"    ⚙️   generating {needed} augmented images …")

    img_cycle  = itertools.cycle(current_originals)
    func_cycle = itertools.cycle(AUG_FUNCS)

    generated = 0
    while generated < needed:
        src  = next(img_cycle)
        func = next(func_cycle)
        try:
            func(str(src))
            generated += 1
        except Exception as e:
            print(f"    ⚠️   skipped {src.name} ({func.__name__}): {e}")

    print(f"    ✅  +{generated} images → train folder now has "
          f"{current_total + generated} images.")


# ─── main logic ──────────────────────────────────────────────────────────────

def balance_dataset(root: str, output: str):
    """
    1. Scan `root` for class folders containing original images.
    2. Split each class 80 / 20 into train / val using original images only.
    3. Copy originals into  <output>/train/<class>/  and  <output>/val/<class>/
    4. Augment only the training side of each class until every train
       folder reaches the same target count (= largest training split).
    5. Validation folders are NEVER touched by augmentation — every image
       in val/ is a genuine original the model has never seen.
    """

    root   = Path(root)
    output = Path(output)

    if not root.is_dir():
        print(f"Error: '{root}' is not a valid directory.")
        sys.exit(1)

    classes = collect_classes(root)
    if not classes:
        print(f"No class folders with images found in '{root}'.")
        sys.exit(1)

    # ── step 1: figure out split sizes ───────────────────────────────────────
    print("\n📊 Original image counts per class:")
    split_map = {}   # class_path -> (train_images, val_images)
    for cls_path, imgs in classes.items():
        train_imgs, val_imgs = split_originals(imgs, VAL_SPLIT, SEED)
        split_map[cls_path] = (train_imgs, val_imgs)
        print(f"  {cls_path.name:35s}  "
              f"total={len(imgs):4d}  "
              f"train={len(train_imgs):4d}  "
              f"val={len(val_imgs):4d}")

    # target = largest training split across all classes
    target = max(len(t) for t, _ in split_map.values())
    print(f"\n🎯 Target training images per class (after augmentation): {target}")
    print(f"📁 Output directory: {output}\n")

    # ── step 2: copy originals into output structure ──────────────────────────
    for cls_path, (train_imgs, val_imgs) in split_map.items():
        cls_name  = cls_path.name
        train_dst = output / "train" / cls_name
        val_dst   = output / "val"   / cls_name

        print(f"📂 {cls_name}")
        print(f"  copying {len(train_imgs)} originals → train/")
        copy_images(train_imgs, train_dst)

        print(f"  copying {len(val_imgs)} originals  → val/")
        copy_images(val_imgs, val_dst)

        # ── step 3: augment the training split only ───────────────────────────
        augment_to_target(train_dst, target)
        print()

    # ── step 4: summary ───────────────────────────────────────────────────────
    print("─" * 60)
    print("✅ Balancing complete.\n")
    print("Final image counts:")
    for cls_path in split_map:
        cls_name  = cls_path.name
        train_dir = output / "train" / cls_name
        val_dir   = output / "val"   / cls_name
        n_train = sum(
            1 for f in train_dir.iterdir() if f.suffix in IMAGE_EXTENSIONS
        )
        n_val = sum(
            1 for f in val_dir.iterdir() if f.suffix in IMAGE_EXTENSIONS
        )
        print(f"  {cls_name:35s}  train={n_train:4d}  val={n_val:4d}")

    print(f"\n📌 Point train.py at:  {output}/train")
    print(f"📌 Point val   at:     {output}/val")
    print("\n⚠️  Remember to update train.py so it loads train/ and val/")
    print("   as separate datasets instead of using validation_split.\n")


# ─── entry point ─────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) not in (3,):
        print("Usage:   python3 leafbalance.py <source_dir> <output_dir>")
        print("Example: python3 leafbalance.py ./Apple ./Apple_balanced")
        sys.exit(1)

    balance_dataset(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()