from PIL import Image, ImageEnhance

# Load the image
image = Image.open('image.png')

# Create an enhancer object for brightness
enhancer = ImageEnhance.Brightness(image)

# Darken the image (factor < 1 darkens, factor = 1 is original, factor > 1 is brighter)
darkened_image = enhancer.enhance(0.5)

# Save the darkened image
darkened_image.save('image_dark.png')

print("Image darkened and saved to image_dark.png")
