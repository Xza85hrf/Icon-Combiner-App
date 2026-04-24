# Icon Combiner App

Icon Combiner App is a Python-based GUI application that allows users to
combine two ICO icons into one. It resizes the icons to a user-specified
size (or automatically to the larger of the two inputs) using PyTorch's
`nn.functional.interpolate` — bilinear interpolation, accelerated on GPU
via CUDA when available and falling back to CPU otherwise. The output is
written as a single `.ico` file. This is classic interpolated resizing,
not AI super-resolution; detail that is not in the source icons will not
appear in the output.

## Features

- Load two `.ico` icons and blend them into a single combined icon.
- Resize via bilinear interpolation on CUDA (if available) or CPU.
- Choose automatic sizing based on the original icon dimensions, or
  specify a custom output size.
- Detailed logging for error tracking and debugging.
- Saves the combined result as an `.ico` file.

## Requirements

- Python 3.x
- Pillow
- sv_ttk
- torch
- numpy

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Xza85hrf/icon-combiner-app.git
    ```

2. Change to the project directory:

    ```bash
    cd Icon-Combiner-App
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```bash
    python icon_combiner_app.py
    ```

2. Use the GUI to load two ICO icons, specify the size, and combine them.

## Logging

The application creates a log file `icon_combiner.log` in the project directory to track events and errors.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

