from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
import time
import requests
from bs4 import BeautifulSoup
import os

SLEEP_TIME = 3


def scrapePage(pageurl = 'https://www.pinterest.com/unfundedaccount/cyberfetish/'):
    """
    Retrieves the image urls of a given pinterest page
    Input: (str) url of a pinterest page to download images from
    OUtput: (set) a set of urls to each image src
    """
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome (no GUI)

    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Load the Pinterest page
        driver.get(pageurl)

        # Container to store seen image URLs to avoid duplicates
        image_urls = set()

        # Initial scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content to load
            time.sleep(SLEEP_TIME)  # Adjust the sleep time if needed

            # Refresh the list of image elements after scrolling
            
            images = driver.find_elements(By.TAG_NAME, 'img')
            for img in images:
                try:
                    img_url = img.get_attribute('src')
                    description = img.get_attribute('alt') or 'No description'
                    if img_url and img_url not in image_urls:
                        image_urls.add(img_url)
                        if len(image_urls)%100==0:
                                print("searched: " + str(len(image_urls)) + "images")
                            
                except Exception as e:
                    print(f"Error while extracting images: {e}")
                    continue

                finally:
                    pass

            # Calculate new scroll height and check if it has reached the bottom
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    except Exception as e:
        print(e)

    finally:
        # Quit the WebDriver
        driver.quit()

    return image_urls


def get_subpages(accounturl):
    """
    retrives the subpages from a pinterest account homepage
    input: (str) url to pinterest account homepage
    Output: (set) set of urls to subpages
    """

    # Send a request to fetch the HTML content of the homepage
    response = requests.get(accounturl)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> elements to extract href attributes
        links = soup.find_all('a', href=True)

        # Extract and filter subpages
        subpages = set()  # Use a set to avoid duplicates
        base_domain = urlparse(accounturl).netloc

        for link in links:
            href = link['href']
            # Convert relative URLs to absolute URLs
            full_url = urljoin(accounturl, href)
            # Filter subpages by checking if they belong to the same domain
            if urlparse(full_url).netloc == base_domain and full_url.startswith(accounturl) and full_url.endswith("/"):
                subpages.add(full_url)
                

        # Output the list of subpages
        for subpage in subpages:
            print(subpage)
    else:
        print(f"Failed to retrieve content from {accounturl}, status code: {response.status_code}")
    return subpages


def download_image(url, save_path):
    """
    downloads a given image file to the given directory
    inputs
    url: (str) image url
    save_path: (str) path to directory
    Output: None
    """
    try:
        
        # Send a GET request to the image URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Open the file in binary write mode and save the image content
            with open(save_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download image. HTTP status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_page (pageurl):
    """
    Downloads the contents of a given pinterest page
    Input: 
    """
    images = scrapePage(pageurl)
    for image in images:
        if not os.path.isdir("./downloads/" + pageurl.split("/")[-2]):
            os.makedirs("./downloads/" + pageurl.split("/")[-2])
        download_image(image, "./downloads/" + pageurl.split("/")[-2] +"/"+ image.split("/")[-1])
    print("successfully downloaded " + str(len(images)) + " images")


def download_account (accounturl):
    pages = sorted(list(get_subpages(accounturl)))
    for i in range(len(pages)):
        print("DOWNLOADING: " + pages[i])
        print(str(i) + " / " + str(len(pages)))
        print("+" * i)
        print("_" * len(pages))
        download_page(pages[i])


#script for user input
account = input("What is the name of the pinterest account you wish to download? ")
account_url = "https://www.pinterest.com/" + account + "/"
print("_"*30)
check="n"
while check not in "yY":
    print(account_url)
    check=input("Is this the account you are looking for? [y/n]")
    if check not in "yY":
        account_url = input("please give me the url of the account you wish to download: ")
        print("_"*30)
    else:
        print("proceeding to download")

download_account(account_url)