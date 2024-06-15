from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import requests
import time

# Configurer les options de Selenium pour utiliser le mode "headless"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

# Initialiser le driver Chrome
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

# Définir le dossier de sauvegarde des images
path = os.path.join(os.getcwd(), "Scrapping_Safka_Web_page")
os.makedirs(path, exist_ok=True)

midel=1
# Fonction pour télécharger les images d'une page
def download_images_from_page(url, start_index):
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    image_tags = soup.find_all('img')
    print("imag_tags",len(image_tags))
    image_urls = {img['src'] for img in image_tags if 'src' in img.attrs}
    print("imag_uls",len(image_urls))
    for i, img_url in enumerate(image_urls, start=start_index):
        global midel
        midel+=1
        try:
            img_data = requests.get(img_url).content
            img_path = os.path.join(path, f'image_{midel}.jpg')
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f'Image {midel} téléchargée : {img_url}')
        except Exception as e:
            print(f"Erreur lors du téléchargement de l'image {midel} : {e}")
print("Page 0")
# Télécharger les images de la première page
url = "https://www.safka.mr/?q=v1"
download_images_from_page(url, 1)

# Télécharger les images des pages suivantes
start_index = midel
print("midel....",midel)
for page_num in range(1, 409):  # Ajustez la plage selon vos besoins
    try:
        print("page_num...................",page_num)
        url = f"https://www.safka.mr/?q=v1&page={page_num}"
        download_images_from_page(url, start_index)
        start_index = midel
        #start_index += len(os.listdir(path)) - start_index + 1
        time.sleep(5)  # Attendez 5 secondes avant de télécharger la page suivante
    except Exception as e:
        print(f"Erreur lors de l'accès à la page {page_num} : {e}")
        time.sleep(10)  # Attendez 10 secondes avant de réessayer

# Fermer le driver
driver.quit()

print("Téléchargement des images terminé.")