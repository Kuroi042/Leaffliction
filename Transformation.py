"""Leaf image transformations for the Leaffliction project.

Use one image to display the transformations:
    python3 Transformation.py path/to/leaf.jpg

Use a directory to save them without opening windows:
    python3 Transformation.py -src path/to/leaves -dst transformed_leaves
"""

import argparse
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np
from plantcv import plantcv as pcv


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
DISPLAY_SIZE = (256, 256)


class LeafTransformer:
    """Create visual leaf features from one input image."""

    def __init__(self, path):
        self.path = Path(path)
        self.rgb = None
        self.blur = None
        self.mask = None
        self.masked = None
        self.roi = None
        self.analyzed = None
        self.landmarks = None
        self.contour = None
        self.centroid = None

    def read_original(self):
        """Read the input image once and keep it in RGB for matplotlib."""
        bgr = cv2.imread(str(self.path))
        if bgr is None:
            raise ValueError(f"Cannot read image: {self.path}")
        self.rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        # The reference output in the subject is built on a 256 x 256 image.
        self.rgb = cv2.resize(
            self.rgb, DISPLAY_SIZE, interpolation=cv2.INTER_AREA
        )
        return self.rgb

    def gaussian_blur(self):
        """Create the thresholded Gaussian-blur view shown in the brief."""
        if self.rgb is None:
            self.read_original()
        saturation = pcv.rgb2gray_hsv(rgb_img=self.rgb, channel="s")
        smooth_saturation = cv2.GaussianBlur(saturation, (7, 7), 1)
        self.blur = pcv.threshold.binary(
            gray_img=smooth_saturation, threshold=65, object_type="light"
        )
        return self.blur

    def create_mask(self):
        """Segment saturated leaf pixels, then fill small holes."""
        if self.rgb is None:
            self.read_original()
        if self.blur is None:
            self.gaussian_blur()
        self.mask = pcv.fill(bin_img=self.blur, size=200)
        self.masked = pcv.apply_mask(
            img=self.rgb, mask=self.mask, mask_color="white"
        )
        return self.mask

    def _largest_contour(self):
        if self.mask is None:
            self.create_mask()
        contours, _ = cv2.findContours(
            self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if not contours:
            return None
        return max(contours, key=cv2.contourArea)

    def roi_objects(self):
        """Show the segmented leaf and its bounding rectangle."""
        if self.rgb is None:
            self.read_original()
        self.contour = self._largest_contour()
        result = self.rgb.copy()
        if self.contour is None:
            self.roi = result
            return result

        overlay = pcv.visualize.colorize_masks(
            masks=[self.mask], colors=["green"]
        )
        result = cv2.addWeighted(result, 0.5, overlay, 0.6, 0)
        height, width = self.rgb.shape[:2]
        cv2.rectangle(
            result, (0, 0), (width - 1, height - 1), (0, 0, 255), 3
        )
        self.roi = result
        return result

    def analyze_object(self):
        """Draw the contour, convex hull, centroid, and leaf major axis."""
        if self.contour is None:
            self.roi_objects()
        result = self.rgb.copy()
        if self.contour is None:
            self.analyzed = result
            return result

        # The threshold image retains the leaf's internal regions. Drawing its
        # contours in blue reproduces the secondary layer in Figure IV.5.
        inner_contours, _ = cv2.findContours(
            self.blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        leaf_contours = []
        for contour in inner_contours:
            if cv2.contourArea(contour) < 20:
                continue
            moments = cv2.moments(contour)
            if moments["m00"] == 0:
                continue
            x = int(moments["m10"] / moments["m00"])
            y = int(moments["m01"] / moments["m00"])
            if self.mask[y, x] > 0:
                leaf_contours.append(contour)
        cv2.drawContours(result, leaf_contours, -1, (0, 0, 255), 3)
        hull = cv2.convexHull(self.contour)
        cv2.drawContours(result, [hull], -1, (255, 0, 255), 5)

        moments = cv2.moments(self.contour)
        if moments["m00"] == 0:
            self.analyzed = result
            return result

        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
        self.centroid = (cx, cy)
        hull_points = hull.reshape(-1, 2)
        distances = np.linalg.norm(hull_points - np.array([cx, cy]), axis=1)
        tip = hull_points[np.argmax(distances)]
        direction = tip - np.array([cx, cy])
        length = np.linalg.norm(direction)
        if length:
            unit = direction / length
            projections = (hull_points - np.array([cx, cy])) @ unit
            opposite = np.array([cx, cy]) + projections.min() * unit
            cv2.line(
                result, tuple(opposite.astype(int)), tuple(tip),
                (255, 0, 255), 5
            )

        cv2.line(
            result, (cx, 0), (cx, result.shape[0] - 1), (255, 0, 255), 5
        )
        cv2.circle(result, self.centroid, 7, (255, 0, 255), -1)
        self.analyzed = result
        return result

    def pseudo_landmarks(self):
        """Draw PlantCV's top, bottom, and centre pseudolandmarks."""
        if self.analyzed is None:
            self.analyze_object()
        result = self.rgb.copy()
        if self.contour is None or self.centroid is None:
            self.landmarks = result
            return result

        top, bottom, centre = pcv.homology.x_axis_pseudolandmarks(
            img=self.rgb, mask=self.mask
        )
        for points, color in (
            (top, (0, 0, 255)),
            (bottom, (255, 0, 255)),
            (centre, (255, 102, 0)),
        ):
            for point in np.asarray(points).reshape(-1, 2):
                cv2.circle(result, tuple(point.astype(int)), 5, color, -1)
        self.landmarks = result
        return result

    def process(self):
        self.read_original()
        self.gaussian_blur()
        self.create_mask()
        self.roi_objects()
        self.analyze_object()
        self.pseudo_landmarks()
        return self

    def display(self):
        """Display the exact seven-panel sequence used in the project brief."""
        if self.landmarks is None:
            self.process()
        figures = [
            ("Figure IV.1: Original", self.rgb, None),
            ("Figure IV.2: Gaussian blur", self.blur, "gray"),
            ("Figure IV.3: Mask", self.masked, None),
            ("Figure IV.4: Roi objects", self.roi, None),
            ("Figure IV.5: Analyze object", self.analyzed, None),
            ("Figure IV.6: Pseudolandmarks", self.landmarks, None),
        ]
        fig, axes = plt.subplots(3, 2, figsize=(10, 14))
        axes = axes.ravel()
        for axis, (title, image, cmap) in zip(axes, figures):
            axis.imshow(image, cmap=cmap)
            axis.set_title(title)
            axis.axis("off")
        fig.tight_layout()
        histogram, histogram_axis = plt.subplots(figsize=(10, 6))
        self._plot_histogram(histogram_axis)
        histogram.tight_layout()
        plt.show()

    def _plot_histogram(self, axis):
        lab = cv2.cvtColor(self.rgb, cv2.COLOR_RGB2LAB)
        hsv = cv2.cvtColor(self.rgb, cv2.COLOR_RGB2HSV)
        channels = (
            ("blue", self.rgb[:, :, 2], "blue"),
            ("blue-yellow", lab[:, :, 2], "gold"),
            ("green", self.rgb[:, :, 1], "green"),
            ("green-magenta", lab[:, :, 1], "magenta"),
            ("hue", hsv[:, :, 0], "blueviolet"),
            ("lightness", lab[:, :, 0], "dimgray"),
            ("red", self.rgb[:, :, 0], "red"),
            ("saturation", hsv[:, :, 1], "cyan"),
            ("value", hsv[:, :, 2], "orange"),
        )
        # The reference histogram is calculated from the complete input image,
        # including the background, rather than from the segmented leaf only.
        selected = np.ones(self.rgb.shape[:2], dtype=bool)
        for name, channel, color in channels:
            values = channel[selected]
            counts, edges = np.histogram(values, bins=100, range=(0, 256))
            # PlantCV reports each channel against all three image channels.
            proportions = counts / (values.size * 3) * 100
            axis.plot(
                (edges[:-1] + edges[1:]) / 2, proportions,
                color=color, label=name,
            )
        axis.set_facecolor("#eaeaf2")
        axis.grid(True, color="white", linewidth=1.2)
        axis.set_xlim(0, 256)
        axis.set_xlabel("Pixel intensity")
        axis.set_ylabel("Proportion of pixels (%)")
        axis.legend(title="color Channel")

    def save(self, destination):
        """Save all transformations for this image inside *destination*."""
        if self.landmarks is None:
            self.process()
        destination = Path(destination)
        destination.mkdir(parents=True, exist_ok=True)
        stem = self.path.stem
        suffix = self.path.suffix or ".png"
        images = {
            "Original": self.rgb,
            "GaussianBlur": self.blur,
            "Mask": self.masked,
            "ROI": self.roi,
            "Analysis": self.analyzed,
            "Pseudolandmarks": self.landmarks,
        }
        for name, image in images.items():
            output = destination / f"{stem}_{name}{suffix}"
            if image.ndim == 3:
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if not cv2.imwrite(str(output), image):
                raise OSError(f"Could not write {output}")

        figure, axis = plt.subplots(figsize=(8, 5))
        self._plot_histogram(axis)
        figure.tight_layout()
        figure.savefig(destination / f"{stem}_ColorHistogram.png", dpi=150)
        plt.close(figure)


def image_paths(source):
    return sorted(
        path for path in Path(source).rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Display or save seven leaf image transformations."
    )
    parser.add_argument("image", nargs="?", help="One image to display")
    parser.add_argument(
        "-src", metavar="DIRECTORY", help="Directory of input images"
    )
    parser.add_argument(
        "-dst", metavar="DIRECTORY", help="Directory for saved transformations"
    )
    parser.add_argument(
        "-mask",
        action="store_true",
        help="Compatibility option; every saved set includes the mask.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.image and not args.src and not args.dst:
        transformer = LeafTransformer(args.image)
        transformer.process()
        transformer.display()
        return
    if args.src and args.dst and not args.image:
        paths = image_paths(args.src)
        if not paths:
            raise SystemExit(f"No supported images found in: {args.src}")
        for path in paths:
            transformer = LeafTransformer(path)
            transformer.process()
            relative_parent = path.relative_to(args.src).parent
            transformer.save(Path(args.dst) / relative_parent)
        print(f"Saved transformations for {len(paths)} image(s) to {args.dst}")
        return
    raise SystemExit(
        "Use one image, or use both -src DIRECTORY and -dst DIRECTORY. See -h."
    )


if __name__ == "__main__":
    main()
