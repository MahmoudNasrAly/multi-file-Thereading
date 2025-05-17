import os
import threading
import requests
import logging
from tqdm import tqdm
from time import sleep

class MultiFileDownloader:
    def __init__(self, urls, file_type, output_dir="downloads", retries=3):
        self.urls = urls
        self.file_type = file_type
        self.output_dir = os.path.join(output_dir, file_type)
        self.retries = retries
        os.makedirs(self.output_dir, exist_ok=True)
        self._setup_logger()

    def _setup_logger(self):
        self.logger = logging.getLogger("Downloader")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        fh = logging.FileHandler('download_log.txt')
        fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def download_file(self, url):
        filename = os.path.join(self.output_dir, url.split("/")[-1])
        attempt = 0

        while attempt < self.retries:
            try:
                self.logger.info(f"Downloading: {url} (Attempt {attempt + 1})")
                with requests.get(url, stream=True, timeout=10) as r:
                    r.raise_for_status()
                    total_size = int(r.headers.get('content-length', 0))
                    with open(filename, 'wb') as f, tqdm(
                        desc=filename,
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        unit_divisor=1024
                    ) as bar:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                                bar.update(len(chunk))
                self.logger.info(f"Download completed: {filename}")
                return
            except Exception as e:
                self.logger.warning(f"Error downloading {url}: {e}")
                attempt += 1
                sleep(2)

        self.logger.error(f"Failed after {self.retries} attempts: {url}")

    def start_downloads(self):
        threads = []
        for url in self.urls:
            thread = threading.Thread(target=self.download_file, args=(url,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        self.logger.info("All downloads complete.")

# --- User Interaction ---
if __name__ == "__main__":
    print("📥 Multi-Threaded Downloader")
    file_type = input("Enter file type you want to download (e.g. txt, pdf, csv): ").strip().lower()

    print("Paste the URLs (one per line). Type 'done' when finished:")
    urls = []
    while True:
        line = input("> ")
        if line.strip().lower() == "done":
            break
        if line.strip():
            urls.append(line.strip())

    if not urls:
        print("No URLs entered. Exiting.")
    else:
        downloader = MultiFileDownloader(urls=urls, file_type=file_type)
        downloader.start_downloads()
