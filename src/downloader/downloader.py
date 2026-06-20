import json
from pathlib import Path

import requests

from downloader.constants import (
    BASE_URL,
    ITEMS_ENDPOINT,
    REQUEST_TIMEOUT,
    OUTPUT_DIRECTORY,
    CATEGORIES,
)


def download_category(category: str):
    print(f"Downloading category: {category}")

    response = requests.get(
        f"{BASE_URL}{ITEMS_ENDPOINT}",
        params={"category": category},
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    data = response.json()

    print(f"Downloaded {len(data)} items for category: {category}")

    return data


def save_json(data, filename: str):
    print(f"Saving data to {filename}.json")

    output_path = Path(OUTPUT_DIRECTORY)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / f"{filename}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print(f"Data saved to {file_path}")


def download_all():
    print("Starting download of all categories...")

    for category in CATEGORIES:
        data = download_category(category)
        save_json(data, category)

    print("Download completed.")


def main():
    print("==========================")
    print(" STALZONE Downloader")
    print("==========================")

    download_all()


if __name__ == "__main__":
    main()