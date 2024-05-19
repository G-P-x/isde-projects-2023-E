import os
from PIL import Image, ImageEnhance
from app.config import Configuration

conf = Configuration()


def change_image_parameters(image_id: str, color: float, brightness: float, contrast: float, sharpness: float):
    params = {
        'Color': color / 10,
        'Brightness': brightness / 10,
        'Contrast': contrast / 10,
        'Sharpness': sharpness / 10
    }
    # if all parameters are equal to 1, return directly image_id without transformation
    if all(value == 1 for value in params.values()):
        return image_id

    input_image_path = os.path.join(conf.image_folder_path, image_id)
    transformed_image_id = f"{image_id.replace('_transformed', '').replace('.JPEG', '')}_transformed.JPEG"
    output_image_path = os.path.join(conf.image_folder_path, transformed_image_id)
    try:
        image = Image.open(input_image_path)
        for transform_name, value in params.items():
            enhancer = getattr(ImageEnhance, transform_name)(image)
            image = enhancer.enhance(value)
        image.save(output_image_path, format='JPEG')
    except Exception as e:
        print(f"Error during image transformation: {e}")
        return None

    return transformed_image_id
