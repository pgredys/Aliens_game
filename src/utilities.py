import io

from PIL import Image


def image_transparent_bg(path):
    """ Takes an image and returns it with a transparent background."""

    img = Image.open(path)
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)

    image_file = io.BytesIO()
    img.save(image_file, format="PNG")
    image_file.seek(0)

    return image_file
