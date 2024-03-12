import os
from PIL import Image, ImageEnhance

from app.config import Configuration

conf = Configuration()


def change_sharpness(image_id: str, value: float):
    if value != 1:
        input_image_path = os.path.join(conf.image_folder_path, image_id)
        image = Image.open(input_image_path)
        sharped_image = ImageEnhance.Sharpness(image).enhance(value)
        sharped_image_id = image_id.replace(image_id, "sharped_image.JPEG")
        output_image_path = os.path.join(conf.image_folder_path, sharped_image_id)
        sharped_image.save(output_image_path, format="JPEG")  # create a sharped copy of the original image
        # In this way, we avoid modifying the original image.
        return sharped_image_id
    else:
        return image_id
