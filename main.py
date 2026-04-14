import faulthandler
faulthandler.enable()

import numpy as np, json, tqdm, argparse
from PIL import Image
from litemapy import Schematic, Region, BlockState


def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        rgb.append(int(hex[i:i+2], 16))
    return tuple(rgb)


def closest(colors, color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors - color)**2, axis=1))
    index = np.argmin(distances)
    return colors[index]


def rgb_to_hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)


# Parse command-line arguments
parser = argparse.ArgumentParser(description='Convert image to Minecraft pixel art schematic')
parser.add_argument('-i', '--image', default='image.png', help='Input image file (default: image.png)')
parser.add_argument('-n', '--name', default='img', help='Schematic name and output file base name (default: img)')
args = parser.parse_args()

# Load block color mapping
with open('blocks.json') as f:
    blocks = json.load(f)

colors = list(map(hex_to_rgb, blocks.keys()))

# Load and prepare image
img = Image.open(args.image).convert('RGB')
img = img.resize((128, 128))
img = img.rotate(90, expand=True)
img = img.rotate(180)

pixels = list(img.get_flattened_data())
width, height = img.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

# Region for flat image (rotated 90° CCW around Y-axis: X = height, Y = 1, Z = width)
reg = Region(0, 0, 0, height, 1, width)
schem = reg.as_schematic(name=args.name, author="me", description="flat image pixel-art")

pbar = tqdm.tqdm(total=width * height)

# Build flat pixel art on ground (Y=0) with 90° CCW rotation around Y-axis
for z in range(height):
    for x in range(width):
        color = pixels[z][x]
        color = closest(colors, tuple(color))
        block_id = blocks[rgb_to_hex(*color)]

        # Rotate 90° counter-clockwise around Y-axis: (x, z) → (z, width-1-x)
        rotated_x = z
        rotated_z = width - 1 - x
        reg[rotated_x, 0, rotated_z] = BlockState("minecraft:" + block_id)

        pbar.update(1)

# Close progress bar explicitly
pbar.close()

# Save to litematic
schem.save(f"{args.name}.litematic")
