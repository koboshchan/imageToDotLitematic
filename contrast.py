from PIL import Image


def apply_contrast(pixel, threshold):
    """
    Apply high contrast to a pixel based on brightness threshold.
    
    Args:
        pixel: (r, g, b) tuple
        threshold: 0-100 value, where to separate light from dark
                  0 = all black, 100 = all white, 50 = middle gray
    
    Returns:
        (255, 255, 255) if bright, (0, 0, 0) if dark
    """
    # Calculate brightness (perceived luminance)
    r, g, b = pixel
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    
    # Convert threshold (0-100) to brightness (0-255)
    threshold_value = (threshold / 100.0) * 255
    
    # Return white or black based on threshold
    if brightness >= threshold_value:
        return (255, 255, 255)
    else:
        return (0, 0, 0)


# Configuration
CONTRAST_THRESHOLD = 45  # 0-100: where to separate light from dark
                         # 0 = everything is white (except pure black)
                         # 50 = middle gray is the separation
                         # 100 = everything is black (except pure white)

# Load and prepare image
img = Image.open('image.png').convert('RGB')

# Get dimensions
width, height = img.size

# Apply high contrast to all pixels
print(f"Applying contrast with threshold: {CONTRAST_THRESHOLD}/100")
print(f"Image size: {width}x{height}")

pixels = img.load()

for y in range(height):
    for x in range(width):
        original_pixel = pixels[x, y]
        pixels[x, y] = apply_contrast(original_pixel, CONTRAST_THRESHOLD)

# Save the high contrast image
output_filename = 'image_contrast.png'
img.save(output_filename)

print(f"Saved high contrast image to {output_filename}")
print(f"Threshold used: {CONTRAST_THRESHOLD}/100")