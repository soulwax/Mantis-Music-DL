# File: main.py

import requests
from bs4 import BeautifulSoup
import re
import os
import json
import logging
import time
from urllib.parse import urljoin, urlparse
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("mantis_downloader.log"), logging.StreamHandler()],
)


class MantisDownloader:
    def __init__(self):
        self.base_url = "https://darkfloor.co.uk"
        self.download_dir = "output"
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.processed_urls = set()
        self.episode_urls = {}
        self.load_episode_urls()

    def generate_episode_urls(self):
        """Generate all possible episode URLs from 1 to 357"""
        for episode in range(1, 358):
            if str(episode) not in self.episode_urls:
                self.episode_urls[str(episode)] = (
                    f"{self.base_url}/mantisradio{episode}/"
                )
        self.save_episode_urls()

    def load_episode_urls(self):
        """Load known episode URLs from url.json if it exists"""
        if os.path.exists("url.json"):
            with open("url.json", "r") as f:
                self.episode_urls = json.load(f)
                logging.info(
                    f"Loaded {len(self.episode_urls)} episode URLs from url.json"
                )
        self.generate_episode_urls()

    def save_episode_urls(self):
        """Save discovered episode URLs to url.json"""
        with open("url.json", "w") as f:
            json.dump(self.episode_urls, f, indent=4)
        logging.info(f"Saved {len(self.episode_urls)} episode URLs to url.json")

    def get_page(self, url):
        """Get page content with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    logging.error(
                        f"Failed to get page {url} after {max_retries} attempts: {e}"
                    )
                    raise
                time.sleep(2**attempt)  # Exponential backoff
        return None

    def get_next_episode_url(self, soup):
        """Find next episode URL in navigation"""
        prev_link = soup.find("a", class_="prev")
        if prev_link and "href" in prev_link.attrs:
            return urljoin(self.base_url, prev_link["href"])
        return None

    def find_episode_number(self, url):
        """Extract episode number from URL"""
        match = re.search(r"mantisradio(\d+)", url.lower())
        return int(match.group(1)) if match else None

    def is_valid_audio_url(self, url):
        """Check if URL is a valid audio file"""
        if not url:
            return False
        parsed = urlparse(url)
        return any(
            parsed.path.lower().endswith(ext) for ext in [".mp3", ".wav", ".m4a"]
        )

    def download_file(self, url, filepath):
        """Download file with progress and retry logic"""
        if os.path.exists(filepath):
            logging.info(f"File already exists: {filepath}")
            return True

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, headers=self.headers, stream=True)
                response.raise_for_status()
                total_size = int(response.headers.get("content-length", 0))

                with open(filepath, "wb") as f:
                    if total_size == 0:
                        f.write(response.content)
                    else:
                        downloaded = 0
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                downloaded += len(chunk)
                                done = int(50 * downloaded / total_size)
                                print(
                                    f"\rDownloading: [{'=' * done}{' ' * (50-done)}] {downloaded}/{total_size} bytes",
                                    end="",
                                )

                print()  # New line after progress bar
                logging.info(f"Successfully downloaded: {filepath}")
                return True

            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    logging.error(
                        f"Failed to download {url} after {max_retries} attempts: {e}"
                    )
                    return False
                time.sleep(2**attempt)

        return False

    def find_audio_links(self, soup, episode_number):
        """Find all audio links in page using multiple detection methods"""
        audio_links = set()

        # Pattern variations for episode numbers
        ep_patterns = [
            str(episode_number).zfill(3),  # 001, 002, etc
            str(episode_number),  # 1, 2, etc
        ]

        # Common filename patterns
        name_patterns = [
            r"mantisradio{ep}\.mp3",
            r"MANTISRADIO{ep}\.mp3",
            r'mantis_radio_{ep}[^"\']*\.mp3',
            r'MANTIS{ep}[^"\']*\.mp3',
            r'MANTIS0*{ep}_[^"\']*\.mp3',  # Matches MANTIS001_12MAY07_STORMFIELD.mp3
        ]

        # Find download links
        download_links = soup.find_all(
            "a", class_=re.compile(r"download|Download", re.I)
        )
        for link in download_links:
            if "href" in link.attrs and link["href"].lower().endswith(".mp3"):
                audio_links.add(urljoin(self.base_url, link["href"]))

        # Search using all pattern combinations
        for ep in ep_patterns:
            for pattern in name_patterns:
                full_pattern = pattern.format(ep=ep)

                # Search in href attributes
                links = soup.find_all("a", href=re.compile(full_pattern, re.I))
                audio_links.update(link["href"] for link in links)

                # Search in text content
                text_content = soup.get_text()
                # Use raw string for the regex pattern
                found_links = re.findall(
                    rf'https?://[^\s<>"]+?/{full_pattern}', text_content, re.I
                )
                audio_links.update(found_links)

        # Also check for SoundCloud links
        soundcloud_links = soup.find_all(
            "a", href=re.compile(r"soundcloud\.com/.*mantisradio", re.I)
        )
        if soundcloud_links:
            logging.info(
                f"Found SoundCloud link for episode {episode_number} - could implement SoundCloud downloading if needed"
            )

        # Clean and validate URLs
        valid_links = []
        for url in audio_links:
            clean_url = urljoin(self.base_url, url)
            if self.is_valid_audio_url(clean_url):
                valid_links.append(clean_url)

        if not valid_links:
            # Try harder to find any MP3 links on the page
            all_links = soup.find_all("a", href=re.compile(r"\.mp3$", re.I))
            for link in all_links:
                url = urljoin(self.base_url, link["href"])
                if self.is_valid_audio_url(url):
                    valid_links.append(url)

        if valid_links:
            logging.info(
                f"Found {len(valid_links)} audio links for episode {episode_number}"
            )

        return valid_links

    def process_episode(self, url):
        """Process a single episode page"""
        if url in self.processed_urls:
            return None

        self.processed_urls.add(url)
        episode_number = self.find_episode_number(url)
        if not episode_number:
            logging.warning(f"Could not determine episode number for {url}")
            return None

        try:
            html_content = self.get_page(url)
            if not html_content:
                return None

            soup = BeautifulSoup(html_content, "html.parser")
            audio_links = self.find_audio_links(soup, episode_number)

            if not audio_links:
                logging.warning(f"No audio links found for episode {episode_number}")
                return None

            for audio_url in audio_links:
                filename = (
                    f"mantis_radio_{episode_number}_{os.path.basename(audio_url)}"
                )
                filepath = os.path.join(self.download_dir, filename)

                if self.download_file(audio_url, filepath):
                    self.episode_urls[str(episode_number)] = url
                    self.save_episode_urls()

            return self.get_next_episode_url(soup)

        except Exception as e:
            logging.error(f"Error processing episode {episode_number}: {e}")
            return None

    def run(self):
        """Main execution method"""
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            logging.info(f"Created download directory: {self.download_dir}")

        # Process episodes in reverse order (newest to oldest)
        for episode in range(357, 0, -1):
            current_url = self.episode_urls.get(str(episode))
            if not current_url:
                continue

            logging.info(f"Processing: {current_url}")
            try:
                self.process_episode(current_url)
                time.sleep(2)  # Be nice to the server
            except Exception as e:
                logging.error(f"Error processing episode {episode}: {e}")


def main():
    downloader = MantisDownloader()
    downloader.run()


if __name__ == "__main__":
    main()
