import numpy as np,json,tqdm
from PIL import Image
from litemapy import Schematic, Region, BlockState

# Shortcut to create a schematic with a single region


def hex_to_rgb(hex):
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal)
  
  return tuple(rgb)

def closest(colors,color):
    colors = np.array(colors)
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest]
    return smallest_distance
def rgb_to_hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)
with open('blocks.json') as f:
    blocks = json.load(f)

colors=list(map(hex_to_rgb,blocks.keys()))

img=Image.open('image.png').convert('RGB')
img=img.resize((img.width//1,img.height//1))
img=img.resize((128,128))
img=img.rotate(90,expand=True)
img=img.rotate(180)

pixels = list(img.getdata())
width, height = img.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

reg = Region(0, 0, 0, 1, img.width, img.height)
schem = reg.as_schematic(name="img", author="me", description="idh one")

# create a tqdm progress bar
pbar = tqdm.tqdm(total=img.width*img.height)
# Build the planet
for z in range(img.height):
    for y in range(img.width):
        color=pixels[z][y]
        color=closest(colors,tuple(color))[0]
        block=blocks[rgb_to_hex(color[0],color[1],color[2])]
        reg.setblock(0, y, z, BlockState(block))
        pbar.update(1)
# rotate schem so it is flat
# schem.rotate(0, 90)
schem.save("img.litematic")