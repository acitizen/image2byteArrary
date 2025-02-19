#!/usr/bin/env python3
"""
Image to E-ink Display Converter
-------------------------------

This script converts images to byte arrays suitable for e-ink displays and generates
Arduino-compatible code. It supports customizable display dimensions and can handle
various image formats.

Usage:
    python image2ByteArray.py --input input.png --output image_data.h --width 152 --height 296 [--invert]

Requirements:
    - PIL (Python Imaging Library)
    - numpy
"""

from PIL import Image
import numpy as np
import argparse
import sys
import os

def convert_image_to_eink_bytes(image_path, width, height, inverted=False):
    """
    Convert an image to a byte array suitable for e-ink displays.

    Args:
        image_path (str): Path to the input image file
        width (int): Desired width of the output image
        height (int): Desired height of the output image
        inverted (bool): Whether to invert the black and white pixels

    Returns:
        bytearray: Processed image data as bytes

    Raises:
        FileNotFoundError: If the input image file doesn't exist
        PIL.UnidentifiedImageError: If the input file is not a valid image
    """
    try:
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
            
            # Calculate required bytes (1 bit per pixel)
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
    except FileNotFoundError:
        print(f"Error: Input file '{image_path}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        sys.exit(1)

def save_as_arduino_code(byte_array, output_path, var_name="IMAGE_DATA"):
    """
    Save the byte array as Arduino code with PROGMEM.

    Args:
        byte_array (bytearray): The processed image data
        output_path (str): Path where the Arduino code will be saved
        var_name (str): Name of the variable in the generated code

    Raises:
        IOError: If there's an error writing to the output file
    """
    try:
        with open(output_path, 'w') as f:
            # Write header guard
            header_guard = os.path.basename(output_path).replace('.', '_').upper()
            f.write(f"#ifndef _{header_guard}_\n")
            f.write(f"#define _{header_guard}_\n\n")
            
            # Write array size definition
            f.write(f"#define {var_name}_SIZE {len(byte_array)}\n\n")
            
            # Write array declaration with PROGMEM
            f.write(f"const unsigned char {var_name}[{var_name}_SIZE] PROGMEM = {{\n")
            
            # Write bytes in groups of 16 per line
            for i in range(0, len(byte_array), 16):
                chunk = byte_array[i:i+16]
                hex_values = [f"0x{b:02X}" for b in chunk]
                f.write("    " + ", ".join(hex_values) + ",\n")
            
            # Close the array and header guard
            f.write("};\n\n")
            f.write("#endif\n")
            
    except IOError as e:
        print(f"Error writing to output file: {str(e)}")
        sys.exit(1)

def main():
    """
    Main function to handle command line arguments and process the image.
    """
    parser = argparse.ArgumentParser(
        description="Convert images to byte arrays for e-ink displays",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument('-i', '--input', required=True,
                        help='Input image file path')
    parser.add_argument('-o', '--output', required=True,
                        help='Output Arduino header file path')
    parser.add_argument('-w', '--width', type=int, default=152,
                        help='Display width in pixels')
    parser.add_argument('-h', '--height', type=int, default=296,
                        help='Display height in pixels')
    parser.add_argument('--invert', action='store_true',
                        help='Invert black and white pixels')
    parser.add_argument('-v', '--var-name', default='IMAGE_DATA',
                        help='Variable name in generated code')
    
    args = parser.parse_args()
    
    print(f"Converting {args.input} to byte array...")
    
    # Convert image to byte array
    byte_array = convert_image_to_eink_bytes(
        args.input, 
        args.width, 
        args.height, 
        args.invert
    )
    
    # Save as Arduino code
    save_as_arduino_code(byte_array, args.output, args.var_name)
    
    print(f"Arduino code saved to {args.output}")
    print(f"Array size: {len(byte_array)} bytes")

if __name__ == "__main__":
    main()
