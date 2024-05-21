# Changelog

All notable changes to this project will be documented in this file.

## [1.0] - 2024-05-20
### Added
- Added option to display the histogram of the selected image.
- Added `histogram_select.html` page to select an image.
- Added "image_histogram" GET and POST in the main.
- Added `histogram_form.py` class.
- Added `histogram.js` file to create the histogram on the html.
- Added `histogram_output.html` page to view the histogram.

- Added `classification_select_image.html` page to upload a user image.
- Added "image_from_PC" GET and POST in the main
- Added `image_uploader.py` to upload an image from the PC and remove it after classification.
- Added `classification_output_from_upload.html` page to display user image classification.

- Added buttons to download classification results in each `classification_output..html`.
- Added `downloadPlot.js` file to download the classification plot.
- Added `downloadScores.js` file to download the classification JSON.

- Added functionality to edit color, brightness, contrast, and sharpness.
- Added `image_transformation.py` to modify the parameters of an image based on the values selected by the user.

### Modified
- Modified `base.html` to include selection fields for testing the newly implemented features.
- Modified `classification_select.html` to allow user image uploads.
- Modified `classification_select.html` to adjust image parameters.
- Modified `classification_output.html` to include the option to download results.
- Modified `classification_output_from_upload.html` to include the option to download results.
- Modified the `request_classification` function in the main to accept image modification parameters set through the HTML page.
- Modified `config.py` to set the image saving path.
- Modified `requirements.txt` to include the `opencv-python` library.
- Modified `.gitingore` to avoid files that shouldn't be versioned.
- Modified `main.py` adding the remove_uploaded_image function into the get of image_histogram and into the get of image_from_PC
- Modified `image_uploader.py` removing the print