import photomosaic as pm
import numpy as np
from skimage.io import imread, imsave
from skimage.color import rgba2rgb

def generate_mosaic(input_image_path, output_image_path, pool_path, tile_size=(30, 30), depth=5):
    # breakpoint()
    image = imread(input_image_path)
    if image.shape[-1] == 4:  # Check for RGBA
        image = rgba2rgb(image)  # Convert to RGB

    pool = pm.make_pool(f"{pool_path}/*")
    mos = pm.basic_mosaic(image, pool, tile_size, depth=depth)
    imsave(output_image_path, (mos * 255).astype(np.uint8))