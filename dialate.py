from PIL import Image, ImageFilter

def selective_dilate_image(input_path, output_path, size=3, dilate_dark=True, min_dimension=200):
    """
    Loads an image, applies a dilation operation selectively to dark or light colors,
    and saves the result. Automatically resizes UP if image is small, applies filter, then resizes back.

    Args:
        input_path (str): The file path of the input image.
        output_path (str): The file path for the dilated output image.
        size (int): The size of the kernel/window for the MaxFilter.
                    Higher values mean more dilation (thicker features).
        dilate_dark (bool): If True, dark colors will be dilated (made thicker).
                            If False, light colors will be dilated.
        min_dimension (int): Minimum pixel dimension for processing. If image is smaller,
                            it will be resized up. Default 200. Set to 0 to disable resizing.
    """
    try:
        # 1. Load the image
        img = Image.open(input_path)
        print(f"Successfully loaded image: {input_path}")
        original_size = img.size
        print(f"Original size: {original_size}")

        # Ensure the image is in a mode suitable for intensity-based operations,
        # like 'L' (grayscale) or 'RGB'. 'L' is often best for filters like MaxFilter.
        original_mode = img.mode
        if img.mode not in ['L', 'RGB', 'RGBA']:
            img = img.convert("RGB") # Convert to RGB if not already a suitable mode
            print("Converted image to RGB for processing.")

        # 2. Smart automatic resize UP if needed
        use_resize = False
        if min_dimension > 0:
            smaller_dimension = min(original_size[0], original_size[1])
            if smaller_dimension < min_dimension:
                # Calculate scale factor to reach minimum dimension
                scale_factor = min_dimension / smaller_dimension
                resized_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                img = img.resize(resized_size, Image.Resampling.LANCZOS)
                use_resize = True
                print(f"Resized UP to: {resized_size} (scale factor: {scale_factor:.2f})")
            else:
                print(f"Image size sufficient ({smaller_dimension}px >= {min_dimension}px), no resizing needed")

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

        # 3. Smart resize back DOWN to original size if we resized up
        if use_resize:
            final_img = final_img.resize(original_size, Image.Resampling.LANCZOS)
            print(f"Resized back down to original: {original_size}")

        # If the original image was 'L' and we converted to 'RGB' for processing,
        # we might want to convert back to original mode if it was 'L'.
        # However, for simplicity, we'll save in the mode of the `final_img`.
        # If original was RGBA, might need to re-add alpha channel if lost.
        # For general purpose, saving as 'RGB' or 'L' (if grayscale) is fine.

        # 4. Save the result
        final_img.save(output_path)
        print(f"Successfully saved dilated image to: {output_path}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Configuration ---
input_filename = "image.png" # <--- IMPORTANT: Change this to your image file name
output_filename = "image_dilated.png"
dilation_size = 3  # Adjust for more or less dilation (e.g., 3, 5, 7)
min_pixel_dimension = 200  # Minimum pixel dimension. If image is smaller, it will be resized UP for better quality.
                           # Set to 0 to disable automatic resizing.

# Set to True to dilate dark lines/shapes
# Set to False to dilate light areas/highlights
dilate_dark_colors = True 
# ---------------------

# Run the function
selective_dilate_image(input_filename, output_filename, dilation_size, dilate_dark=dilate_dark_colors, min_dimension=min_pixel_dimension)