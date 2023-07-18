from pathlib import Path

from PIL import Image
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def add_watermark(img_name,
                  base_path=None,
                  watermark_path=Path(settings.STATIC_ROOT, 'watermarks/python-logo.png'),
                  upload_to=Path(settings.MEDIA_ROOT, 'clients/avatars/images/')):
    if not base_path:
        base_path = Path(upload_to, img_name)

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

    watermark_position = (
        base_img.size[0] - watermark_img.size[0],
        base_img.size[1] - watermark_img.size[1]
    )
    base_img.paste(watermark_img, watermark_position, mask=watermark_img)

    base_img.save(base_path)


def send_mail_to_clients(clients: list[dict]):
    for client in clients:
        html_body = render_to_string(
            'email_templates/match_email.html',
            client,
        )
        msg = EmailMultiAlternatives(
            subject=f'Сайт знакомств',
            to=[client.get('email_to')]
        )
        msg.attach_alternative(html_body, 'text/html')
        msg.send()
