import click
from tessellate.generate_mosaic import generate_mosaic
from tessellate.convert_images import convert_images

@click.group()
def cli():
    pass

@cli.command()
@click.argument('input_image', type=click.Path(exists=True, dir_okay=False))
@click.argument('output_image', type=click.Path())
@click.argument('pool_path', type=str)
@click.option('--tile_size', default='30,30', help='Size of the tiles, e.g., 30,30')
@click.option('--depth', default=5, type=int, help='Depth of the mosaic')
def mosaic(input_image, output_image, pool_path, tile_size, depth):
    tile_size = tuple(map(int, tile_size.split(',')))
    # Print options nicely
    options = (
        "\nGenerating Mosaic with:\n"
        f"  Input Image : {input_image}\n"
        f"  Output Image: {output_image}\n"
        f"  Pool Path   : {pool_path}\n"
        f"  Tile Size   : {tile_size}\n"
        f"  Depth       : {depth}\n"
    )
    click.echo(options)
    generate_mosaic(
        input_image_path=input_image,
        output_image_path=output_image,
        pool_path=pool_path,
        tile_size=tile_size,
        depth=depth
    )

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True, file_okay=False))
@click.argument('output_dir', type=click.Path())
@click.option('--format', 'target_format', default='jpeg', help='Target image format (e.g., png, jpeg)')
def convert(input_dir, output_dir, target_format):
    convert_images(
        input_dir=input_dir,
        output_dir=output_dir,
        target_format=target_format
    )

if __name__ == '__main__':
    cli()
