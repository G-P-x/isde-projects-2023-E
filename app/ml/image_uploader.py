from app.config import Configuration


def upload_image(contents):
    image_id = "uploaded_image.JPEG"
    image_path = Configuration.image_folder_path_img + image_id
    # Saving the file
    with open(f"{image_path}", "wb") as f:
        f.write(contents)
    return image_id
