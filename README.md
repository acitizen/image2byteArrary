# E-ink Display Image Converter
This tool converts images to byte arrays in the format required by the Waveshare EPD Library. It generates both .cpp and .h files that are compatible with e-ink display projects using the EPD Library.

Used in conjunction with EPD Library for e-ink displays: https://github.com/Bodmer/EPD_Libraries/tree/master

## Features
- Converts images to the exact format required by EPD Library
- Supports customizable display dimensions
- Generates both .cpp and .h files with proper headers
- Option to invert black and white pixels
- Automatic image resizing and grayscale conversion
- Configurable variable names

## Requirements
- Python 3.6 or higher
- PIL (Python Imaging Library)
- NumPy

## Installation
1. Install the required dependencies:
   ```bash
   pip install Pillow numpy
   ```

## Usage
Basic usage:
```bash
python image2ByteArray.py -i input.png -o imagedata.cpp -w 152 --height 296
```

All available options:
```bash
python image2ByteArray.py -i input.png -o imagedata.cpp -w 152 --height 296 --invert --var-name CUSTOM_NAME
```

### Arguments
- `-i, --input`: Input image file path (required)
- `-o, --output`: Output cpp file path (required)
- `-w, --width`: Display width in pixels (default: 152)
- `--height`: Display height in pixels (default: 296)
- `--invert`: Invert black and white pixels (optional)
- `-v, --var-name`: Variable name in generated code (default: IMAGE_DATA)

## Output Format
The script generates two files:

1. A .cpp file containing:
```cpp
/**
 *  @filename   :   imagedata.cpp
 *  @brief      :   Image data converted for e-ink display
 *  ...
 */
#include "imagedata.h"
#include <avr/pgmspace.h>

const unsigned char IMAGE_DATA[5624] PROGMEM = {
    0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
    // ... more data ...
};
```

2. A .h file containing:
```cpp
/**
 *  @filename   :   imagedata.h
 *  @brief      :   head file for imagedata.cpp
 *  ...
 */

extern const unsigned char IMAGE_DATA[]; //152*296
/* FILE END */
```

## Example Use with EPD Library
1. Convert your image:
   ```bash
   python image2ByteArray.py -i your_image.png -o imagedata.cpp -w 152 --height 296
   ```
2. Copy both generated files (imagedata.cpp and imagedata.h) to your Arduino project
3. Check this header in your main sketch:
   ```cpp
   #include "imagedata.h"
   ```

## Acknowledgments
- Based on the EPD Library format by Waveshare
- Thanks to the PIL and NumPy teams for their excellent libraries
- All examples I could find to convert b&w images to byte arrays where for Windows, so created this simple image conversion tools for my e-ink display projects. Hope it can help you too!
