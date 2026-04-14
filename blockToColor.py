import os, json, math
from PIL import Image, ImageStat


def int_to_rgb(i):
    return ((i >> 16) & 255, (i >> 8) & 255, i & 255)


def rgb_to_hex(r, g, b):
    return "{:02x}{:02x}{:02x}".format(r, g, b)


def color_distance(rgb1, rgb2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))


with open("colors.json", "r") as f:
    data = json.load(f)

color_list = []
for color_id, color_data in data.items():
    for shade_index, shade_int in enumerate(color_data["colors"]):
        color_list.append(
            {"rgb": int_to_rgb(shade_int), "hex": rgb_to_hex(*int_to_rgb(shade_int))}
        )

imgs = os.listdir("cheap")
colors = {}

for img_name in imgs:
    if img_name == ".DS_Store":
        continue

    im = Image.open("blocks/" + img_name)
    im = im.convert("RGB")
    median = ImageStat.Stat(im).median
    median_rgb = (int(median[0]), int(median[1]), int(median[2]))

    # Find closest color in color_list
    best_match = None
    min_distance = float("inf")
    for color in color_list:
        dist = color_distance(median_rgb, color["rgb"])
        if dist < min_distance:
            min_distance = dist
            best_match = color

    if best_match:
        colors[best_match["hex"]] = img_name.split(".")[0]

with open("blocks.json", "w") as f:
    json.dump(colors, f, indent=4, sort_keys=True)
