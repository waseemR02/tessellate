import os
from PIL import Image, ImageOps
import pyheif
from tqdm import tqdm
import subprocess

def convert_heic_to_image(heic_path, output_format='JPEG'):
    """Convert HEIC file to PIL Image using pyheif"""
    try:
        heif_file = pyheif.read(heic_path)
        image = Image.frombytes(
            heif_file.mode, 
            heif_file.size, 
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        # Apply EXIF orientation
        image = ImageOps.exif_transpose(image)
        return image
    except Exception as e:
        raise RuntimeError(f"HEIC conversion failed: {str(e)}")

def convert_images(input_dir, output_dir, target_format):
    """
    Convert all images (including HEIC) to RGB format
    Requires libheif: 
      macOS: brew install libheif
      Ubuntu: sudo apt-get install libheif-dev
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    print(f"Converting images in {input_dir} to {target_format.upper()} format and saving to {output_dir}")
    # First check if HEIC dependencies are available
    try:
        subprocess.run(['which', 'heif-convert'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Error: libheif not installed. Required for HEIC support.")
        print("Install with:")
        print("  macOS: brew install libheif")
        print("  Ubuntu/Debian: sudo apt install libheif-dev libde265")
        return

    supported_extensions = ('.heic', '.png', '.jpg', '.jpeg', '.webp', '.bmp')
    all_files = [f for f in os.listdir(input_dir) 
                if f.lower().endswith(supported_extensions)]
    
    errors = []
    converted = 0
    
    with tqdm(total=len(all_files), desc="Converting images", unit="file", bar_format='{l_bar}{bar:30}{r_bar}') as pbar:
        for filename in all_files:
            try:
                input_path = os.path.join(input_dir, filename)
                base_name = os.path.splitext(filename)[0]
                output_path = os.path.join(output_dir, f"{base_name}.{target_format.lower()}")
                
                if filename.lower().endswith('.heic'):
                    # Convert HEIC using pyheif
                    image = convert_heic_to_image(input_path)
                    image.save(output_path, format=target_format, quality=100)
                else:
                    # Convert other formats using Pillow
                    with Image.open(input_path) as img:
                        if img.mode in ['RGBA', 'LA', 'P']:
                            img = img.convert('RGB')
                        img.save(output_path, format=target_format, quality=100)
                
                converted += 1
                pbar.update(1)
                pbar.set_postfix_str(f"{filename[:15]}...")
                
            except Exception as e:
                errors.append((filename, str(e)))
                pbar.update(1)
                pbar.set_postfix_str(f"Error: {filename[:15]}...", refresh=True)

    # Print summary
    print(f"\nSuccessfully converted {converted}/{len(all_files)} files")
    if errors:
        print("\nErrors occurred with these files:")
        for filename, error in errors:
            print(f" - {filename}: {error}")
    else:
        print("All files converted successfully!")
