import requests
from bs4 import BeautifulSoup
import re
import os


def download_file(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as file:
        file.write(response.content)


def get_next_episode_url(soup):
    prev_link = soup.find("a", class_="prev")
    return prev_link["href"] if prev_link else None


def main():
    if not os.path.exists("mantis_radio_mixtapes"):
        os.makedirs("mantis_radio_mixtapes")

    current_url = "https://darkfloor.co.uk/mantisradio356/"
    episode = 356

    while current_url and episode >= 1:
        print(f"Processing Mantis Radio {episode}")
        response = requests.get(current_url)
        soup = BeautifulSoup(response.text, "html.parser")

        mixtape_links = soup.find_all("a", href=re.compile(r"\.mp3$"))

        for link in mixtape_links:
            mixtape_url = link["href"]
            mixtape_name = f"mantis_radio_{episode}_{os.path.basename(mixtape_url)}"

            print(f"Downloading: {mixtape_name}")
            download_file(mixtape_url, f"mantis_radio_mixtapes/{mixtape_name}")
            print(f"Downloaded: {mixtape_name}")

        current_url = get_next_episode_url(soup)
        episode -= 1


if __name__ == "__main__":
    main()
