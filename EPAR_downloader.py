import requests
import logging
import time
import os
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    filename='Logfile.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

# HTTP headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}

def create_directory(directory_path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def download_file(url, file_path):
    """Download a file from the given URL and save it to the specified path."""
    try:
        response = requests.get(url, stream=True, headers=HEADERS)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            logging.info(f"Successfully downloaded: {file_path}")
        else:
            logging.error(f"Failed to download {url}. HTTP Status: {response.status_code}")
    except Exception as e:
        logging.error(f"Error while downloading {url}: {e}")

def main():
    print('WRITING PDF FILES...')
    
    # Set up directories
    current_dir = os.getcwd()
    download_dir = os.path.join(current_dir, 'Downloaded Labels')
    create_directory(download_dir)
    
    # Read URLs from the input file
    try:
        with open('Input.txt', 'r') as file:
            urls = [url.strip() for url in file if url.strip()]
    except FileNotFoundError:
        logging.error("Input.txt file not found. Please ensure it exists in the current directory.")
        return

    # Download files
    base_url = 'https://www.ema.europa.eu/en/documents/product-information/'
    endpoint = '-epar-product-information_en.pdf'
    
    for url in tqdm(urls, desc="Downloading files"):
        epar_name = url.split('/')[-1]
        constructed_url = f"{base_url}{epar_name}{endpoint}"
        output_file_path = os.path.join(download_dir, f"{epar_name}.pdf")
        
        download_file(constructed_url, output_file_path)
        time.sleep(2)  # Be polite to the server

if __name__ == "__main__":
    main()
