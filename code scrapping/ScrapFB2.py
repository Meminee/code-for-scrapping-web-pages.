# imports here
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

# Specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Open the Facebook login page
driver.get("http://www.facebook.com")

# Target username and password fields
username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

# Enter username and password
username.clear()
username.send_keys("meminemini2@gmail.com")  # Replace with your username
password.clear()
password.send_keys("memine123456789")  # Replace with your password

# Target the login button and click it
button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

# Wait for the page to load
time.sleep(5)
images = []

# Iterate over both uploaded and tagged images respectively
for i in ["photos"]:
    # Navigate to the media page
    driver.get("https://web.facebook.com/groups/451286855424786/media/" + i)
    time.sleep(5)

    # Scroll down to load more images
    for j in range(0, 400):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

     # Target all the link elements on the page
    anchors = driver.find_elements(By.TAG_NAME, 'a')
    anchors = [a.get_attribute('href') for a in anchors]

    # Narrow down to image links only
    anchors = [a for a in anchors if str(a).startswith("https://web.facebook.com/photo/?fbid=")]

    print('Found ' + str(len(anchors)) + ' links to images')

    # Extract the image source from each link
    for a in anchors:
        driver.get(a)  # Navigate to the link
        time.sleep(5)  # Wait a bit
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        if img_elements:
            img_src = img_elements[-1].get_attribute("src")
            if img_src and img_src.startswith("https://"):
                images.append(img_src)
print('I scraped ' + str(len(images)) + ' images!')

# Create the directory for saving images
path = os.path.join(os.getcwd(), "VoursetBey3SeyaratPage")
os.makedirs(path, exist_ok=True)

# Function to download an image
def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Download images
for idx, image in enumerate(images):
    save_as = os.path.join(path, f"{idx}.jpg")
    download_image(image, save_as)

print(f"Downloaded {len(images)} images to {path}")
