import requests
from bs4 import BeautifulSoup
import os

# Function to download images
def download_image(url, folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        image_name = url.split("/")[-1]
        image_path = os.path.join(folder_path, image_name)
        with open(image_path, 'wb') as file:
            for chunk in response:
                file.write(chunk)
        print(f"Downloaded: {image_name}")
    else:
        print(f"Failed to download image from {url}")

# Function to fetch and parse a page
def fetch_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, "lxml")

# Main function to scrape images
def main():
    for i in range(1,27):
        print({i},"***************")
        base_url = "https://www.voursa.com"
        page_url = f"{base_url}/index.cfm?PN={i}&gct=1&sct=11&gv=13"
        soup = fetch_page(page_url)
    
        # Find all the links that lead to individual listing pages
        links = soup.find_all('a', href=True)
    
        for link in links:
            href = link['href']
            if 'annonces.cfm' in href:
                # Construct the full URL for the listing page
                listing_url = f"{base_url}{href}"
                print(f"Fetching listing page: {listing_url}")
            
                # Fetch the listing page and parse it
                listing_soup = fetch_page(listing_url)
            
                # Find the div with id 'photodiv' and extract all image URLs
                photodiv = listing_soup.find('div', {'id': 'photodiv'})
                if photodiv:
                    img_tags = photodiv.find_all('img')
                    for img in img_tags:
                        img_url = img.get('src')
                        if img_url:
                            if not img_url.startswith("http"):
                                img_url = f"{base_url}{img_url}"
                            print(f"Found larger image URL: {img_url}")
                            download_image(img_url, "Voursa")

# Call the main function
main()

    
