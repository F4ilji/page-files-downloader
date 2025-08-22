import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import sys
import questionary

DOWNLOAD_FOLDER = "downloaded_files"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def find_files_on_page(base_url):
    """
    Analyzes a given URL to find links to files and groups them by extension.

    Args:
        base_url (str): The URL of the page to scan.

    Returns:
        dict: A dictionary where keys are file extensions (e.g., '.pdf')
              and values are lists of full URLs for those files.
              Returns None if the page cannot be accessed or an error occurs.
    """
    print(f"Analyzing page: {base_url}...")
    try:
        response = requests.get(base_url, headers=HEADERS, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', href=True)
        files_by_extension = {}
        parsed_base_url = urlparse(base_url)

        for link in links:
            href = link['href']
            full_url = urljoin(base_url, href)
            parsed_full_url = urlparse(full_url)

            # Ensure the link belongs to the same domain
            if parsed_full_url.netloc != parsed_base_url.netloc:
                continue

            path = parsed_full_url.path
            _, extension = os.path.splitext(path)

            # Check for a valid file extension (typically 2-5 characters long)
            if 2 <= len(extension) <= 5:
                extension = extension.lower()
                if extension not in files_by_extension:
                    files_by_extension[extension] = set()
                files_by_extension[extension].add(full_url)

        # Convert sets to lists for consistent ordering
        for ext in files_by_extension:
            files_by_extension[ext] = list(files_by_extension[ext])

        return files_by_extension

    except requests.exceptions.RequestException as e:
        print(f"Error accessing page '{base_url}': {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred while analyzing the page: {e}", file=sys.stderr)
        return None

def download_files(urls_to_download):
    """
    Downloads a list of files from their URLs into the DOWNLOAD_FOLDER.

    Args:
        urls_to_download (list): A list of file URLs to download.
    """
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    print(f"\nStarting download. Files will be saved to the '{DOWNLOAD_FOLDER}' folder.")

    for file_url in urls_to_download:
        try:
            print(f"Downloading: {file_url}")
            # Use stream=True to handle large files efficiently
            file_response = requests.get(file_url, stream=True, headers=HEADERS, timeout=30)
            file_response.raise_for_status()

            file_name = os.path.basename(urlparse(file_url).path)
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

            with open(file_path, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f" -> File '{file_name}' downloaded successfully.")
        except requests.exceptions.RequestException as e:
            print(f" ! Error downloading file '{file_url}': {e}", file=sys.stderr)
        except Exception as e:
            print(f" ! An unexpected error occurred while processing '{file_url}': {e}", file=sys.stderr)

def main():
    """
    Main function to run the file downloader script.
    """
    try:
        base_url = questionary.text("Enter the URL of the page to analyze:").ask()
        if not base_url:
            print("URL cannot be empty. Exiting.")
            sys.exit(1)

        base_url = base_url.strip()

        found_files = find_files_on_page(base_url)

        if not found_files:
            print("No file links found on the page or an error occurred.")
            sys.exit(0)

        # Create choices for the user, showing file counts
        choices = sorted(
            [
                f"{ext} ({len(urls)} files)"
                for ext, urls in found_files.items()
            ],
            key=lambda x: x.split(' ')[0] # Sort by extension
        )

        selected_choices = questionary.checkbox(
            'Select extensions to download (arrows - navigate, space - select, enter - confirm):',
            choices=choices
        ).ask()

        if not selected_choices:
            print("You did not select anything. Exiting.")
            sys.exit(0)

        # Gather all URLs from the selected extensions
        urls_to_download = []
        for choice in selected_choices:
            selected_ext = choice.split(' ')[0]
            urls_to_download.extend(found_files[selected_ext])

        # Remove duplicates just in case
        urls_to_download = list(set(urls_to_download))

        download_files(urls_to_download)
        print("\nProcess completed.")

    except (KeyboardInterrupt, TypeError):
        print("\nOperation interrupted by the user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nA critical error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
