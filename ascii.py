import os
import sys
from PIL import Image
import shutil

# Define the ASCII characters (from dark to light)
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

# Resize image to fit terminal width and scale down
def resize_image(image, scale_factor=0.1):
    # Get terminal width
    terminal_width, _ = shutil.get_terminal_size()

    # Calculate the new width for the image (subtract some padding for margins)
    new_width = int(terminal_width * scale_factor)
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    
    resized_image = image.resize((new_width, new_height))
    return resized_image

# Convert image to grayscale
def grayscale_image(image):
    return image.convert("L")

# Convert each pixel to an ASCII character
def pixel_to_ascii(pixel_value):
    return ASCII_CHARS[pixel_value // 25]

# Convert the image to ASCII
def image_to_ascii(image_path, scale_factor=0.1):
    try:
        # Open the image file
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return None
    
    # Resize image and convert to grayscale
    image = resize_image(image, scale_factor)
    image = grayscale_image(image)

    # Generate ASCII characters
    ascii_str = ""
    for y in range(image.height):
        for x in range(image.width):
            pixel_value = image.getpixel((x, y))
            ascii_str += pixel_to_ascii(pixel_value)
        ascii_str += "\n"

    return ascii_str

# Save the ASCII art to a text file
def save_ascii_to_file(ascii_str, output_path="ascii.txt"):
    try:
        with open(output_path, "w") as file:
            file.write(ascii_str)
        print(f"ASCII art has been saved to {output_path}.")
    except Exception as e:
        print(f"Error saving ASCII art: {e}")

# Validate image file path
def validate_image_path(image_path):
    if not os.path.isfile(image_path):
        print(f"Error: The file {image_path} does not exist.")
        sys.exit(1)
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verify if the image is valid
    except (IOError, SyntaxError) as e:
        print(f"Error: The file {image_path} is not a valid image.")
        sys.exit(1)

# Main function
def main():
    # Ask the user for the image file path
    image_path = input("Enter the path to the image: ")

    # Ask for the scale factor (optional, default to 0.1)
    try:
        scale_factor = float(input("Enter scale factor (default 0.1): ") or 0.1)
    except ValueError:
        print("Invalid scale factor. Using default 0.4.")
        scale_factor = 0.4

    # Validate image path
    validate_image_path(image_path)

    # Convert image to ASCII art
    ascii_art = image_to_ascii(image_path, scale_factor)
    
    if ascii_art:
        print("\n[ASCII Art Generated]:")
        print(ascii_art)
        # Save ASCII art to the current directory as 'ascii.txt'
        save_ascii_to_file(ascii_art, "ascii_image.txt")

if __name__ == "__main__":
    main()
