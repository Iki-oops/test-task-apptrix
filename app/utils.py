from PIL import Image
from django.conf import settings


def add_watermark(img_name,
                  base_path=None,
                  watermark_path=settings.STATIC_ROOT + 'watermarks/python-logo.png',
                  upload_to=settings.MEDIA_ROOT + 'clients/avatars/images/'):
    if not base_path:
        base_path = upload_to + img_name

    base_img = Image.open(base_path)
    watermark_img = Image.open(watermark_path)

    watermark_img = watermark_img.resize((174, 174))
    watermark_img = watermark_img.convert('RGBA')

    watermark_img.putalpha(174)

    data = watermark_img.getdata()
    new_data = []
    for item in data:
        if item[:3] == (0, 0, 0):
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)
    watermark_img.putdata(new_data)

    # transparent = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    watermark_position = (
        base_img.size[0] - watermark_img.size[0],
        base_img.size[1] - watermark_img.size[1]
    )
    base_img.paste(watermark_img, watermark_position, mask=watermark_img)

    # transparent.paste(base_img, (0, 0))
    # transparent.paste(watermark_img, watermark_position, mask=watermark_img)
    # watermarked_img_path = upload_to + ''.join(img_name.split('.')[:-1]) + '.png'
    # transparent.save(watermarked_img_path)
    base_img.save(base_path)
    # return watermarked_img_path
