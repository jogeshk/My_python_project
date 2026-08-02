import os
import sys
import time

# --- AUTOMATIC LIBRARY INSTALLER ---
try:
    import cv2
except ImportError:
    print("OpenCV not found. Downloading and installing 'opencv-python'...")
    import subprocess
    # Runs the pip install command silently in the background
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
    import cv2
    print("Installation complete!\n")

# Ask the user for the image file name
IMAGE_FILE = input("The image must be in the same folder. Name of the image (e.g., photo.jpg): ")
ASCII_CHARS = " .:-=+*%%@@##"

def main():
    if not os.path.exists(IMAGE_FILE):
        print(f"Error: Could not find '{IMAGE_FILE}'")
        return

    # Load the static image file
    frame = cv2.imread(IMAGE_FILE)
    if frame is None:
        print("Error: Could not decode the image file. Ensure it is a valid image format.")
        return
    
    os.system("")
    os.system("cls")

    num_chars = len(ASCII_CHARS)

    # Resolution settings for large screen layout
    TARGET_WIDTH = 240
    TARGET_HEIGHT = 65

    # 1. Downsize resolution to the new larger target dimensions
    resized_frame = cv2.resize(frame, (TARGET_WIDTH, TARGET_HEIGHT))
    height, width, _ = resized_frame.shape
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    # 2. Compile lines manually using the optimized loop configuration
    output = []
    for y in range(height):
        line = []
        for x in range(width):
            brightness = gray_frame[y, x]
            char = ASCII_CHARS[(int(brightness) * num_chars) // 256]
            b, g, r = resized_frame[y, x]
            
            line.append(f"\033[38;2;{r};{g};{b}m{char}")
        output.append("".join(line))
    
    # 3. Print the static frame block once
    sys.stdout.write("\033[1;1H" + "\n".join(output))
    sys.stdout.flush()

    print("\033[0m\n\nImage rendered successfully! Press Ctrl + C to close.")

    # Keep the program running so the terminal doesn't close immediately
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[0m\nDone!")

if __name__ == "__main__":
    main()
