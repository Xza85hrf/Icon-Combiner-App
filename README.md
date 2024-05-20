# Icon Combiner App

Icon Combiner App is a Python-based GUI application that allows users to combine two ICO icons into one. The application uses CUDA (if available) or CPU for upscaling the icons to a user-specified size or automatically sizes them based on their original dimensions. It provides detailed logging for error tracking and debugging.

## Features

- Load two ICO icons and combine them into one.
- Upscale icons using CUDA or CPU.
- Choose automatic sizing based on original icon dimensions or specify a custom size.
- Detailed logging for error tracking and debugging.
- Save the combined icon to a file.

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
    cd icon-combiner-app
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

