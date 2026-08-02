import cv2
import os
import sys
import glob

# Detailed characters for smooth image transitions
ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

def main():
    # Automatically search the current folder for any .jpg file
    jpg_files = glob.glob("*.jpg")
    
    if not jpg_files:
        print("Error: Could not find any .jpg images in this folder!")
        print("Make sure your image is saved in the exact same folder as this script.")
        return
        
    # Select the first JPG image found
    image_file = jpg_files[0]
    print(f"Loading image: {image_file}...\n")

    img = cv2.imread(image_file)
    if img is None:
        print("Error: Could not read or open the image file.")
        return

    # Turn on Windows ANSI styling and clear screen
    os.system("")
    os.system("cls")

    # Set up resolution scaling boundaries
    target_width = 160
    h_orig, w_orig = img.shape[:2]
    aspect = h_orig / float(w_orig)
    target_height = int(target_width * aspect * 0.52) # Compresses vertical height for text rows
    
    resized_img = cv2.resize(img, (target_width, target_height))
    gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

    num_chars = len(ASCII_CHARS)
    output_lines = []

    # Loop through the image pixels to apply colors and shapes
    for y in range(target_height):
        line_chars = []
        for x in range(target_width):
            brightness = gray_img[y, x]
            char_idx = int(brightness / 256 * num_chars)
            char = ASCII_CHARS[char_idx]

            # Read RGB channels
            b, g, r = resized_img[y, x]

            # Embed TrueColor color tags
            line_chars.append(f"\033[38;2;{r};{g};{b}m{char}")
        
        output_lines.append("".join(line_chars))

    # Output the final image directly onto the terminal screen
    sys.stdout.write("\n".join(output_lines) + "\033[0m\n")

if __name__ == "__main__":
    main()
