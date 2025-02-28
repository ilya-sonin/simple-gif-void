# Simple GIF Void

[README на русском](README.ru.md)

A lightweight Python tool to remove background colors from GIF files, making them transparent. By default, it removes white backgrounds (`#FFFFFF`), but you can specify any color or multiple colors in HEX or RGB format.

## Features

- Removes one or multiple background colors from GIFs.
- Supports HEX (`#RRGGBB`) and RGB (`rgb(r,g,b)`) color formats.
- Preserves GIF animation with original frame durations.
- Provides progress output in the console.
- Generates a standalone binary executable via PyInstaller.

## Installation

### Using Source Code
1. Ensure you have Python 3.12+ installed.
2. Clone the repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Using Binary
1. Go to the "Actions" tab in this repository.
2. Select the latest successful workflow run.
3. Download the `simple-gif-void-binary-linux` artifact (or other OS-specific versions if available).

## Usage

### Command Line
Run the script or binary with the following options:
```bash
# Remove default white background
python src/remove_background.py -i input.gif -o output.gif

# Remove specific colors
python src/remove_background.py -i input.gif -o output.gif -c "#FF0000,#00FF00"
python src/remove_background.py -i input.gif -o output.gif -c "rgb(255,0,0),#FFFFFF"
```

#### Options
- `-i, --input`: Input GIF file (default: `input.gif`)
- `-o, --output`: Output GIF file (default: `output.gif`)
- `-c, --color`: Background colors to remove, comma-separated (default: `#FFFFFF`)

### Example Output
```
Processing input.gif (10 frames): 10/10 (100.0%)
Processing input.gif (10 frames): Done. Saved to output.gif
```

## Building the Binary Locally

To create a standalone executable:
1. Install PyInstaller (included in `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
2. Build the binary:
   ```bash
   pyinstaller --onefile src/remove_background.py
   ```
3. Find the executable in the `dist/` folder.

## Running Tests

To verify the functionality:
```bash
pytest tests/ -v
```

## CI/CD

This project uses GitHub Actions to:
- Run tests on every push or pull request to the `main` branch.
- Build and upload a Linux binary as an artifact if tests pass.

Check the "Actions" tab for workflow runs and artifacts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to open issues or submit pull requests with improvements or bug fixes!

---
© 2025 ilya-sonin