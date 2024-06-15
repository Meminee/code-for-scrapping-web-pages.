import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2

# Path to the folder containing the images
input_folder = "/home/memine/Bureau/RimAi scrap/Done clinning/Scapping_Safka_Web_page"
output_folder = "/home/memine/Bureau/RimAi scrap/Done clinning/the best3"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def calculate_sharpness(image):
    image_cv = np.array(image)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance / 1000.0  # Normalize sharpness

def calculate_color_vibrancy(image):
    image_cv = np.array(image)
    hsv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)
    vibrancy = np.std(hsv[:, :, 1]) / 128.0
    return vibrancy

def calculate_contrast(image):
    image_cv = np.array(image)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    contrast = (np.max(gray) - np.min(gray)) / (np.max(gray) + np.min(gray))
    return contrast

def calculate_noise(image):
    image_cv = np.array(image)
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    noise = np.std(gray)
    noise_score = 1 - (noise / 255.0)
    return noise_score

def calculate_quality_score(image):
    sharpness = calculate_sharpness(image)
    color_vibrancy = calculate_color_vibrancy(image)
    contrast = calculate_contrast(image)
    noise_score = calculate_noise(image)
    quality_score = (sharpness + color_vibrancy + contrast + noise_score) / 4.0
    return quality_score

# Function to rename, process, and calculate scores for images
def rename_process_and_score_images(input_folder, output_folder):
    files = os.listdir(input_folder)
    counter = 1
    scores = []

    for file in files:
        input_path = os.path.join(input_folder, file)
        image = Image.open(input_path)

        width, height = image.size
        new_width = int(width * 1.5)
        new_height = int(height * 1.5)
        image = image.resize((new_width, new_height))

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)

        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)

        # Reduce noise
        image = image.filter(ImageFilter.MedianFilter(size=3))

        # Enhance brightness
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)

        if image.mode == 'RGBA':
            image = image.convert('RGB')

        quality_score = calculate_quality_score(image)
        scores.append(quality_score)

        new_name = f"web{counter}.jpg"
        output_path = os.path.join(output_folder, new_name)
        image.save(output_path, "JPEG")

        counter += 1
        print(f"Processed: {file} -> {new_name} with Quality Score: {quality_score}")

    if scores:
        overall_score = sum(scores) / len(scores)
        print(f"Overall Score for Participant: {overall_score}")

# Call the function to rename, process, and score images
rename_process_and_score_images(input_folder, output_folder)
