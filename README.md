# Tessellate

Tessellate is a command-line tool for generating image mosaics and converting various image formats. It uses Python libraries such as photomosaic, Pillow, and pyheif to transform your images into stunning tessellations.

## Features

- Create image mosaics with customizable tile sizes and depth.
- Convert HEIC and other image formats to standard RGB images.
- User-friendly CLI with clear commands and options.

## Installation

Ensure you have Python 3.7+ installed. Then, install the package from the repository:

```bash
pip install .
```
or you can use uv for installation
```bash
uv sync
```

You can also just use the cli without cloning the repo
```bash
pip install git+https://github.com/waseemr02/tessellate
```

## Usage

### Generate Mosaic

```bash
tessellate mosaic <input_image> <output_image> <pool_path> [--tile_size="30,30"] [--depth=5]
```

### Convert Images

```bash
tessellate convert <input_dir> <output_dir> [--format=jpeg]
```
