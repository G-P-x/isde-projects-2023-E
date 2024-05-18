from app.config import Configuration
import os

conf = Configuration()
image_id = "uploaded_image.JPEG"
image_path = Configuration.image_folder_path_img + image_id

# Function to remove the image associated with the provided image_id
def remove_uploaded_image():
    
    if os.path.exists(image_path):
            os.remove(image_path)
            print("Image removed successfully")
    else:
        print("Image not found at the provided path:", image_path)


def upload_image(contents):
    
    # Saving the file
    with open(f"{image_path}", "wb") as f:
        f.write(contents)
    return image_id