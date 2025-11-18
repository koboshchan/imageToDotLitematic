from PIL import Image, ImageFilter
import os

def selective_dilate_image(input_path, output_path, size=3, dilate_dark=True):
    """
    Loads an image, applies a dilation operation selectively to dark or light colors,
    and saves the result.

    Args:
        input_path (str): The file path of the input image.
        output_path (str): The file path for the dilated output image.
        size (int): The size of the kernel/window for the MaxFilter.
                    Higher values mean more dilation (thicker features).
        dilate_dark (bool): If True, dark colors will be dilated (made thicker).
                            If False, light colors will be dilated.
    """
    try:
        # 1. Load the image
        img = Image.open(input_path)
        print(f"Successfully loaded image: {input_path}")

        # Ensure the image is in a mode suitable for intensity-based operations,
        # like 'L' (grayscale) or 'RGB'. 'L' is often best for filters like MaxFilter.
        original_mode = img.mode
        if img.mode not in ['L', 'RGB', 'RGBA']:
            img = img.convert("RGB") # Convert to RGB if not already a suitable mode
            print("Converted image to RGB for processing.")

        processed_img = img

        if dilate_dark:
            # To dilate dark areas using MaxFilter (which expands bright areas),
            # we invert the image, dilate, then invert back.
            # Convert to grayscale first for a more consistent inversion logic.
            if processed_img.mode != 'L':
                processed_img = processed_img.convert("L")
                print("Converted to grayscale for dark dilation.")

            # Invert the image (dark becomes bright, bright becomes dark)
            inverted_img = Image.eval(processed_img, lambda x: 255 - x)

            # Apply MaxFilter (now dilating the original dark areas, which are bright in 'inverted_img')
            dilated_inverted = inverted_img.filter(ImageFilter.MaxFilter(size=size))

            # Invert back to get the dilated dark areas
            final_img = Image.eval(dilated_inverted, lambda x: 255 - x)

        else:
            # Dilate light areas directly.
            # MaxFilter naturally expands bright areas.
            final_img = processed_img.filter(ImageFilter.MaxFilter(size=size))

        # If the original image was 'L' and we converted to 'RGB' for processing,
        # we might want to convert back to original mode if it was 'L'.
        # However, for simplicity, we'll save in the mode of the `final_img`.
        # If original was RGBA, might need to re-add alpha channel if lost.
        # For general purpose, saving as 'RGB' or 'L' (if grayscale) is fine.

        # 3. Save the result
        final_img.save(output_path)
        print(f"Successfully saved dilated image to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Configuration ---
input_filename = "image.png" # <--- IMPORTANT: Change this to your image file name
output_filename = "image.png"
dilation_size = 5  # Adjust for more or less dilation (e.g., 3, 5, 7)

# Set to True to dilate dark lines/shapes
# Set to False to dilate light areas/highlights
dilate_dark_colors = True 
# ---------------------

# Run the function
selective_dilate_image(input_filename, output_filename, dilation_size, dilate_dark=dilate_dark_colors)