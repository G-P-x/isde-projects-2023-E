import os
import uuid
import time
from PIL import Image, ImageEnhance
from app.config import Configuration

conf = Configuration()


def cleanup_old_transformed_images(max_age_in_seconds):
    current_time = time.time()

    for filename in os.listdir(conf.image_folder_path):
        file_path = os.path.join(conf.image_folder_path, filename)

        # Ensure the file is an image and it's a transformed image
        if not (filename.endswith('.JPEG') and 'transformed_image' in filename):
            continue

        # Get the modification time and delete the file if it's too old
        file_modification_time = os.path.getmtime(file_path)
        if current_time - file_modification_time > max_age_in_seconds:
            os.remove(file_path)


def change_image_parameters(image_id: str, color: float, brightness: float, contrast: float, sharpness: float):
    cleanup_old_transformed_images(max_age_in_seconds=3600)  # Delete any old transformed images previously created

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
    unique_id = str(uuid.uuid4())
    transformed_image_id = f"transformed_image_{unique_id}.JPEG"
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
