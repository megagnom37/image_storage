import click
import httpx
import os
from io import BytesIO
from PIL import Image as PILImage

from server.models import Image


@click.group()
@click.option('--port', '-p', default=9999)
@click.option('--host', '-h', default="0.0.0.0")
@click.pass_context
def cli(ctx, host, port):
    ctx.obj = {'address': f'http://{host}:{port}'}


@cli.command(
    name='images',
    help='Get list of images in storage')
@click.pass_context
def images(ctx):
    r = httpx.get(f"{ctx.obj['address']}/images")
    for i, data in enumerate(r.json()):
        print(f'image [{i}]: {Image(**data)}')


@cli.command(
    name='upload',
    help='Upload image to storage with tags')
@click.option('--file', '-f', default=None)
@click.option('--tags', '-t', default=None, multiple=True)
@click.pass_context
def upload_image(ctx, file, tags):
    if not file:
        raise FileExistsError('Please provide file name by --file or -f')

    if not os.path.exists(file):
        raise FileNotFoundError('Please provide correct file path')
    
    if not tags:
        tags = ''
    else:
        tags = ','.join(tags)

    files = {'image': open(file, 'rb')}
    data = {'image_tags': tags}
    r = httpx.post(f"{ctx.obj['address']}/add_image", files=files, data=data)
    print(r.json())


@cli.command(
    name='get',
    help='Download image from storage to host by id')
@click.option('--image_id', '-id', default=None)
@click.option('--output', '-o', default='./')
@click.pass_context
def get_image(ctx, image_id, output):
    if not image_id:
        raise ValueError('Please provide image_id by --image_id or -id')

    params = {'image_id': image_id}
    r = httpx.get(f"{ctx.obj['address']}/get_image", params=params)

    image = PILImage.open(BytesIO(r.content))
    file_name = f'{output}/{image_id}.{image.format}'
    image.save(file_name, image.format)


@cli.command(
    name='tagged_images',
    help='Get list of images filtered by tags')
@click.option('--tags', '-t', default=None, multiple=True)
@click.pass_context
def get_images_by_tags(ctx, tags):
    if not tags:
        tags = []
    else:
        tags = list(tags)

    params = {'tags': tags}
    r = httpx.get(f"{ctx.obj['address']}/images_by_tags", params=params)
    for i, data in enumerate(r.json()):
        print(f'image [{i}]: {Image(**data)}')


if __name__ == '__main__':
    cli()
