from app.config import Configuration
import os
import uuid

conf = Configuration()

# Creation of the directory temp in order to don't see the uploaded image in the subset of available images
temp_dir = os.path.join(conf.image_folder_path, 'temp')

uploaded_image_id = 'uploaded_image' + str(uuid.uuid4()) + '.JPEG'
output_image_path = os.path.join(temp_dir, uploaded_image_id)


# Function to remove the image associated with the provided image_id
def remove_uploaded_image():
    
    if os.path.exists(output_image_path):
            os.remove(output_image_path)


def upload_image(contents):
    
    create_directory(temp_dir)
    
    # Saving the file
    with open(f"{output_image_path}", "wb") as f:
        f.write(contents)
    return os.path.join('temp', uploaded_image_id)


def create_directory(path):
    
    # Create the directory if it does not exist
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"Directory '{path}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{path}': {e}")


