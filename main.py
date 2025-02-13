import requests
from bs4 import BeautifulSoup
import re
import os


def download_file(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as file:
        file.write(response.content)


def main():
    # Create a directory to store the downloads
    if not os.path.exists("mantis_radio_mixtapes"):
        os.makedirs("mantis_radio_mixtapes")

    # Fetch the webpage content
    url = "https://darkfloor.co.uk/mantisradio/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links that contain mixtape files
    mixtape_links = soup.find_all("a", href=re.compile(r"\.mp3$"))

    for link in mixtape_links:
        mixtape_url = link["href"]
        mixtape_name = os.path.basename(mixtape_url)

        print(f"Downloading: {mixtape_name}")
        download_file(mixtape_url, f"mantis_radio_mixtapes/{mixtape_name}")
        print(f"Downloaded: {mixtape_name}")


if __name__ == "__main__":
    main()
