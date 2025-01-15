import requests
import json
import os
import time

API_URL = "https://archive.org/advancedsearch.php"
METADATA_URL = "https://archive.org/metadata/{identifier}"
OUTPUT_FILE = "minimal_urdu_texts.json"
TIMEOUT = 30
ITEMS_PER_PAGE = 1000
MAX_RETRIES = 3

def main():
    """
    Fetch the top 10,000 most viewed Urdu texts from the Internet Archive, starting from the beginning.
    """
    if not os.path.exists(OUTPUT_FILE):
        print(f"Creating {OUTPUT_FILE}...")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    fetch_texts()

    print("✅ Data collection complete.")

def fetch_texts():
    """
    Fetch and store texts with minimal fields: identifier, title, year, thumbnail_url, read_url, and download_url.
    """
    page = 1
    while True:
        print(f"  Querying page {page}...")
        docs = fetch_docs_page(page)

        if docs is None:
            print("  Stopping due to repeated failures.")
            break
        if not docs:
            print("  No more results.")
            break

        for doc in docs:
            record = build_record(doc)
            if record:
                append_record(record)

        page += 1
        if page > 10:  # Limit to 10 pages (10,000 items)
            break

        time.sleep(1)

def fetch_docs_page(page):
    """
    Fetch a single page of results sorted by views in descending order.
    """
    query = "language:urdu AND mediatype:texts"
    params = {
        "q": query,
        "fl[]": "identifier,title,date",
        "sort[]": "downloads desc",  # Sort by downloads in descending order
        "rows": 1000,
        "page": page,
        "output": "json"
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(API_URL, params=params, timeout=TIMEOUT)
            if response.status_code != 200:
                print(f"  HTTP error {response.status_code}, retrying...")
                time.sleep(5)
                continue

            data = response.json()
            return data.get("response", {}).get("docs", [])
        except Exception as e:
            print(f"  Error: {e}, retrying...")
            time.sleep(5)

    return None

def build_record(entry):
    """
    Build a single record with minimal metadata.
    """
    try:
        identifier = entry.get("identifier", "").strip()
        title = entry.get("title", "Untitled").strip()
        if isinstance(title, list):
            title = ", ".join(title)

        year = entry.get("date", "Unknown").strip()
        if isinstance(year, list):
            year = ", ".join(year)

        # Fetch metadata to get the download link
        download_filename = get_pdf_filename(identifier)

        return {
            "id": identifier,
            "title": title,
            "year": year,
            "thumbnail_url": f"https://archive.org/services/img/{identifier}",
            "read_url": f"https://archive.org/stream/{identifier}",
            "download_url": f"https://archive.org/download/{identifier}/{download_filename}"
        }
    except Exception as e:
        print(f"  Failed to build record for {entry.get('identifier', 'Unknown')}: {e}")
        return None

def get_pdf_filename(identifier):
    """
    Retrieve the correct filename for downloading the book.
    """
    try:
        response = requests.get(METADATA_URL.format(identifier=identifier), timeout=TIMEOUT)
        if response.status_code == 200:
            files = response.json().get("files", [])
            for file in files:
                if file.get("name", "").endswith(".pdf"):
                    return file["name"]
    except Exception as e:
        print(f"  Metadata retrieval failed for {identifier}: {e}")

    return f"{identifier}.pdf"

def append_record(record):
    """
    Append a record to the output JSON file.
    """
    try:
        with open(OUTPUT_FILE, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(record)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.truncate()
    except Exception as e:
        print(f"  Failed to append record: {e}")

if __name__ == "__main__":
    main()
