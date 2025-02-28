# Mantis Music Playlist Downloader

This is a simple script that downloads all the songs from a Mantis Music playlist. It uses the Mantis Music API to get the song URLs and then downloads them using yt-dlp.

## Requirements

- Python 3
- yt-dlp

You can use the `install.ps1` script to install python (as miniconda3) and yt-dlp on Windows.
For Linux/macOS, you can use the `install.sh` script to install yt-dlp.

## Workflow

1. Isolate your work environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate # Linux/macOS 
    venv\Scripts\activate # Windows
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the script:

    ```bash
    python3 main.py
    ```

    The script will ask for the playlist URL and the download location.

4. Deactivate the virtual environment when you are done:

    ```bash
    deactivate
    ```

## License

GPL-3.0
