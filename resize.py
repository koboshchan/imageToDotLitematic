import argparse
from PIL import Image

# Level to size mapping
LEVEL_SIZES = {
    0: 128,
    1: 256,
    2: 512,
    3: 1024,
    4: 2048
}

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Resize image')
parser.add_argument('-s', '--size', type=int, help='Size of the image (overrides --level if specified)')
parser.add_argument('-l', '--level', type=int, default=0, choices=[0, 1, 2, 3, 4], help='Level (0-4): 0=128×128, 1=256×256, 2=512×512, 3=1024×1024, 4=2048×2048 (default: 0)')
args = parser.parse_args()

# Use --size if provided, otherwise use --level
size = args.size if args.size is not None else LEVEL_SIZES[args.level]

image = Image.open('image.png')
new_size = (size, size)
resized_image = image.resize(new_size)
resized_image.save('image.png')