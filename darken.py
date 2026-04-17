import argparse
from PIL import Image

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Darken image")
parser.add_argument(
    "-i", "--input", default="image.png", help="Input image file (default: image.png)"
)
parser.add_argument(
    "-o",
    "--output",
    default="image_dark.png",
    help="Output image file (default: image_dark.png)",
)
parser.add_argument(
    "-f",
    "--factor",
    type=float,
    default=0.91,
    help="Brightness factor (default: 0.91, < 1 darkens, > 1 brightens)",
)
parser.add_argument(
    "-w",
    "--ignore-white-percent",
    type=int,
    help="Percentage (0-100) to ignore darkening",
)
args = parser.parse_args()

# Load the image
image = Image.open(args.input).convert("RGB")
pixels = image.load()
width, height = image.size

# Process pixels
for x in range(width):
    for y in range(height):
        r, g, b = pixels[x, y]

        should_darken = True
        if args.ignore_white_percent is not None and args.ignore_white_percent != -1:
            sum_rgb = r + g + b
            if sum_rgb == 0:
                value = 100
            else:
                value = sum_rgb / (255 * 3) * 100
            if value > args.ignore_white_percent:
                should_darken = False

        if should_darken:
            # Apply darkening factor
            new_r = min(255, int(r * args.factor))
            new_g = min(255, int(g * args.factor))
            new_b = min(255, int(b * args.factor))
            pixels[x, y] = (new_r, new_g, new_b)

# Save the darkened image
image.save(args.output)
print(f"Image darkened and saved to {args.output}")
