from PIL import Image

image = Image.open('image.png')
new_size = (128, 128)
resized_image = image.resize(new_size)
resized_image.save('image.png')