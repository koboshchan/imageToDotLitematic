import os,json
from PIL import Image, ImageStat
imgs=os.listdir('blackwhite')
colors={}
def rgb_to_hex(r, g, b):
    return '{:02x}{:02x}{:02x}'.format(r, g, b)
for img in imgs:
    if img==".DS_Store":
        continue
    im = Image.open('blocks/'+img)
    im=im.convert('RGB')
    median = ImageStat.Stat(im).median
    # print(median)
    colors[rgb_to_hex(int(median[0]),int(median[1]),int(median[2]))]=img.split('.')[0]

with open('blocks.json', 'w') as f:
    json.dump(colors, f, indent=4, sort_keys=True)