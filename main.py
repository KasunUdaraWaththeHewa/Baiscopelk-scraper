import os
import requests
from bs4 import BeautifulSoup

baseURL = "https://www.baiscope.lk/"
tv_series_url_slug_base = "prison-break"
episodes_per_season = [22,22,13,22,9]
starting_season = 1

def setup():
    print("Setting up...")
    for season_index, total_episodes in enumerate(episodes_per_season):
        current_season = starting_season + season_index
        for episode in range(1, total_episodes + 1):
            # Format season and episode into the URL slug
            tv_series_url_slug = f"{tv_series_url_slug_base}-s{current_season:02d}-e{episode:02d}-sinhala-subtitles"
            scrape_and_download(baseURL, tv_series_url_slug, current_season, episode)


def scrape_and_download(baseURL, tv_series_url_slug, season, episode):
    # Construct the URL for the episode page
    url = f"{baseURL}{tv_series_url_slug}"
    print(f"Fetching page: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the download button
    download_button = soup.find("a", class_="dlm-buttons-button")
    if not download_button:
        print(f"Download button not found for Season {season}, Episode {episode}.")
        return

    # Get the download link
    download_link = download_button.get("href")
    if not download_link.startswith("http"):
        download_link = baseURL + download_link.lstrip("/")

    print(f"Download link found: {download_link}")

    # Fetch the subtitle file
    try:
        subtitle_response = requests.get(download_link, stream=True)
        subtitle_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the file: {e}")
        return

    # Save the subtitle file
    file_name = f"{tv_series_url_slug_base}_S{season:02d}_E{episode:02d}_Sinhala_Subtitles.srt"
    save_subtitle_file(file_name, subtitle_response)


def save_subtitle_file(file_name, response):
    # Create a directory for subtitles if it doesn't exist
    os.makedirs("subtitles", exist_ok=True)
    file_path = os.path.join("subtitles", file_name)

    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)

    print(f"Subtitle file saved: {file_path}")


if __name__ == "__main__":
    setup()
