import os
import json
from PIL import Image
import easyocr
import fitz  # PyMuPDF

def extract_text_from_images(images_dir):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])  # You can specify other languages as well

    concatenated_text = ""
    for filename in os.listdir(images_dir):
        if filename.endswith(".png"):
            image_path = os.path.join(images_dir, filename)
            # Perform OCR on the image
            result = reader.readtext(image_path)
            text = " ".join([entry[1] for entry in result])
            concatenated_text += text + " "

    return concatenated_text.strip()

def convert_xps_to_images(xps_file, output_folder):
    try:
        doc = fitz.open(xps_file)

        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Iterate over each page in the XPS
        for page_number in range(len(doc)):
            # Get the page
            page = doc.load_page(page_number)

            # Render the page as an image
            pix = page.get_pixmap()

            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Save the image to the output folder
            output_image_path = os.path.join(output_folder, f"page{page_number + 1}.png")
            img.save(output_image_path)

        print("Conversion successful!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def process_xps_files(xps_directory):
    output_data = []
    for filename in os.listdir(xps_directory):
        if filename.endswith(".xps"):
            xps_file_path = os.path.join(xps_directory, filename)
            images_output_folder = os.path.join(xps_directory, f"{os.path.splitext(filename)[0]}_images")
            # Convert XPS to images
            success = convert_xps_to_images(xps_file_path, images_output_folder)
            if success:
                # Extract text from images
                text = extract_text_from_images(images_output_folder)
                output_data.append({
                    "filename": filename,
                    "pageno": "NA",
                    "text": text
                })

    return output_data

def save_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Specify the directory containing XPS files
xps_directory = "sample data"
# Process XPS files
output_data = process_xps_files(xps_directory)
# Specify the output JSON file
output_json_file = "output_data/output.json"
# Ensure the output directory exists
output_dir = os.path.dirname(output_json_file)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Save the data to JSON file
save_to_json(output_data, output_json_file)
