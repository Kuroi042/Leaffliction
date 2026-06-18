import os
import sys
import itertools
from pathlib import Path

# Import your existing augmentation functions
from Augmentation import (
    ft_rotate,
    ft_flip,
    ft_shear,
    skew,
    ft_crop,
    distort,
)

# The 6 augmentation functions, in the order you want them cycled
AUG_FUNCS = [ft_rotate, ft_flip, ft_shear, skew, ft_crop, distort]

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"}
AUG_TAGS = ["_Rotate", "_Flip", "_Shear", "_Skew", "_Crop", "_Distortion"]


def is_original_image(filename: str) -> bool:
    """
    Returns True only for original images, not ones already
    created by a previous augmentation run (e.g. skips '*_Rotate.JPG').
    """
    ext = os.path.splitext(filename)[1]
    if ext not in IMAGE_EXTENSIONS:
        return False
    stem = os.path.splitext(filename)[0]
    return not any(tag in stem for tag in AUG_TAGS)


def count_classes(root: Path) -> dict:
    """
    Walk the directory tree like Distribution.py's ft_load does,
    but only count ORIGINAL images (skip prior augmentation output).
    Returns {class_folder_path: [list of original image Paths]}.
    """
    counts = {}
    for current_root, dirs, files in os.walk(root):
        original_files = [f for f in files if is_original_image(f)]
        if len(original_files) == 0:
            continue
        class_path = Path(current_root)
        counts[class_path] = [class_path / f for f in original_files]
    return counts


def balance_dataset(root: str):
    root = Path(root)
    if not root.is_dir():
        print(f"Error: '{root}' is not a valid directory.")
        sys.exit(1)

    class_images = count_classes(root)

    if not class_images:
        print(f"No subdirectories with images found in '{root}'.")
        sys.exit(1)

    sizes = {cls: len(imgs) for cls, imgs in class_images.items()}
    target = max(sizes.values())

    print("\n📊 Current class distribution:")
    for cls, n in sizes.items():
        print(f"  {cls.name:30s} {n}")
    print(f"\n🎯 Target size per class: {target}\n")

    for cls, imgs in class_images.items():
        current = len(imgs)
        needed = target - current

        if needed <= 0:
            print(f"✅ {cls.name} already balanced ({current} images)")
            continue

        print(f"⚙️  {cls.name}: generating {needed} new images...")

        # Cycle through source images and augmentation functions together
        # so the workload is spread evenly across both.
        img_cycle = itertools.cycle(imgs)
        func_cycle = itertools.cycle(AUG_FUNCS)

        generated = 0
        while generated < needed:
            src_img = next(img_cycle)
            func = next(func_cycle)

            try:
                func(str(src_img))
                generated += 1
            except Exception as e:
                print(f"  ⚠️  Skipped {src_img.name} ({func.__name__}): {e}")

        print(f"  ✅ {cls.name}: +{generated} images → now {current + generated}\n")

    print("🏁 Balancing complete.")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 balance_dataset.py <directory>")
        print("Example: python3 balance_dataset.py ./Apple")
        sys.exit(1)

    balance_dataset(sys.argv[1])


if __name__ == "__main__":
    main()