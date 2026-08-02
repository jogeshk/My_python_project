#zoom out to see the clear video#

import cv2
import os
import time
import sys

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

VIDEO_FILE = input("the video must be in the same folder.Name of the video:")
ASCII_CHARS = " .:-=+*%%@@##"
print("zoom out to see the clear video!")

def main():
    if not os.path.exists(VIDEO_FILE):
        print(f"Error: Could not find '{VIDEO_FILE}'")
        return

    cap = cv2.VideoCapture(VIDEO_FILE)
    
    os.system("")
    os.system("cls")

    num_chars = len(ASCII_CHARS)

    # --- ENLARGE RESOLUTION HERE ---
    # Standard terminal fonts are roughly twice as tall as they are wide.
    # To maintain a proper 16:9 video aspect ratio, your column count 
    # needs to be roughly 3.5 to 4 times larger than your row count.
    TARGET_WIDTH = 240
    TARGET_HEIGHT = 65

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

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
                    # Fixed potential index error out-of-bounds bug
                    char = ASCII_CHARS[(int(brightness) * num_chars) // 256]
                    b, g, r = resized_frame[y, x]
                    
                    line.append(f"\033[38;2;{r};{g};{b}m{char}")
                output.append("".join(line))
            
            # 3. Print the frame block from top-left
            sys.stdout.write("\033[1;1H" + "\n".join(output))
            sys.stdout.flush()
            
            time.sleep(0.03)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        print("\033[0m\nDone!")

if __name__ == "__main__":
    main()
