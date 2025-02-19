from PIL import Image
import numpy as np

def convert_image_to_eink_bytes(image_path, width, height, inverted=False):
    """
    Convert an image to a byte array suitable for e-ink displays.
    """
    # Open and resize image
    with Image.open(image_path) as img:
        # Convert to grayscale
        img = img.convert('L')
        
        # Resize image
        img = img.resize((width, height))
        
        # Convert to numpy array for easier processing
        img_array = np.array(img)
        
        # Apply threshold to convert to pure black and white
        threshold = 128
        img_binary = (img_array > threshold).astype(np.uint8)
        
        if inverted:
            img_binary = ~img_binary
        
        # Calculate how many bytes we need
        # Each byte represents 8 pixels (1 bit per pixel)
        num_bytes = (width * height + 7) // 8
        
        # Create output byte array
        out_bytes = bytearray(num_bytes)
        
        # Convert bits to bytes
        byte_index = 0
        bit_index = 0
        
        for y in range(height):
            for x in range(width):
                # If pixel is white (1), set the corresponding bit
                if img_binary[y, x]:
                    out_bytes[byte_index] |= (1 << (7 - bit_index))
                
                bit_index += 1
                if bit_index == 8:
                    byte_index += 1
                    bit_index = 0
        
        return out_bytes

def save_as_arduino_code(byte_array, output_path):
    """
    Save the byte array as Arduino code with PROGMEM.
    """
    with open(output_path, 'w') as f:
        # Write array declaration with PROGMEM - copy exactly from example
        f.write("const unsigned char IMAGE_DATA[{}] PROGMEM = {{\n".format(len(byte_array)))
        
        # Write bytes in groups of 16 per line
        for i in range(0, len(byte_array), 16):
            chunk = byte_array[i:i+16]
            hex_values = [f"0X{b:02X}" for b in chunk]
            f.write("   " + ",".join(hex_values) + ",\n")
        
        # Close the array
        f.write("};")

# Example usage:
if __name__ == "__main__":
    # Input and output file paths
    IMAGE_PATH = "input.png"
    OUTPUT_PATH = "image_data.txt"
    
    # Common e-ink display dimensions
    DISPLAY_WIDTH = 152
    DISPLAY_HEIGHT = 296
    
    print(f"Converting {IMAGE_PATH} to byte array...")
    
    # Convert image to byte array
    byte_array = convert_image_to_eink_bytes(IMAGE_PATH, DISPLAY_WIDTH, DISPLAY_HEIGHT)
    
    # Save as Arduino code
    save_as_arduino_code(byte_array, OUTPUT_PATH)
    print(f"Arduino code saved to {OUTPUT_PATH}")
    print(f"Array size: {len(byte_array)} bytes")