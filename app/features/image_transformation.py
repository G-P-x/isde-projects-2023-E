import os
from PIL import Image, ImageEnhance
from app.config import Configuration

conf = Configuration()


def change_image_parameters(image_id: str, color: float, brightness: float, contrast: float, sharpness: float):
    # Define enhancement parameters by normalizing the input values
    params = {
        'Color': color / 10,
        'Brightness': brightness / 10,
        'Contrast': contrast / 10,
        'Sharpness': sharpness / 10
    }

    # If all parameters are set to 1, return the original image ID without transformation
    if all(value == 1 for value in params.values()):
        return image_id

    # Define the path for the temp directory
    temp_dir = os.path.join(conf.image_folder_path, 'temp')
    create_directory(temp_dir)

    # Construct the input and output image paths
    input_image_path = os.path.join(conf.image_folder_path, image_id)
    transformed_image_id = "transformed_image.JPEG"
    output_image_path = os.path.join(temp_dir, transformed_image_id)

    try:
        # Open the input image
        image = Image.open(input_image_path)
        # Apply the transformations
        for transform_name, value in params.items():
            enhancer = getattr(ImageEnhance, transform_name)(image)
            image = enhancer.enhance(value)
        # Save the transformed image to the output path
        image.save(output_image_path, format='JPEG')
    except Exception as e:
        print(f"Error during image transformation: {e}")
        return None

    # Return the relative path of the transformed image
    return os.path.join('temp', transformed_image_id)


def create_directory(path):
    # Create the directory if it does not exist
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Directory '{path}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{path}': {e}")
