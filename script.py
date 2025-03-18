import requests
import json
import time
import pandas as pd

# API endpoint for Archive.org advanced search
API_URL = "https://archive.org/advancedsearch.php"

# Input files
CSV_FILE = "Texts - ibteda_archive.csv"
OUTPUT_FILE = "urdu_texts_with_authors.json"

# Configuration
ITEMS_PER_PAGE = 50
MAX_RETRIES = 3
TIMEOUT = 30

# Load CSV with titles and authors
df = pd.read_csv(CSV_FILE)

# Ensure column names match expected ones
df.columns = [col.strip().lower() for col in df.columns]

title_col = 'title' if 'title' in df.columns else df.columns[0]
author_col = 'author' if 'author' in df.columns else df.columns[1]

titles = df[title_col].tolist()
authors = df[author_col].tolist()

def fetch_docs(title):
    query = f'title:"{title}" AND mediatype:"texts"'
    params = {
        "q": query,
        "fl[]": "identifier,title,year,publicdate,language",
        "sort[]": "downloads desc",
        "rows": ITEMS_PER_PAGE,
        "output": "json"
    }
    
    wait_time = 5
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(API_URL, params=params, timeout=TIMEOUT)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("response", {}).get("docs", [])
            else:
                print(f"⚠️ HTTP error {resp.status_code} for '{title}' on attempt {attempt+1}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2
        except Exception as e:
            print(f"⚠️ Error: {e} for '{title}' on attempt {attempt+1}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2
    return None

def fetch_download_url(identifier):
    metadata_url = f"https://archive.org/metadata/{identifier}"
    try:
        resp = requests.get(metadata_url, timeout=TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            if "files" in data:
                for file in data["files"]:
                    if file.get("format") == "Text PDF" or file.get("name", "").endswith(".pdf"):
                        return f"https://archive.org/download/{identifier}/{file['name']}"
        return "Unknown"
    except Exception as e:
        print(f"⚠️ Error fetching download URL for {identifier}: {e}")
        return "Unknown"

def append_to_json(data):
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []
    
    existing_data.append(data)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

def main():
    for title, author in zip(titles, authors):
        print(f"🔍 Searching for: {title}")
        docs = fetch_docs(title)
        if docs is None:
            print("❌ Failed to fetch document after repeated attempts. Skipping.")
            continue
        
        for doc in docs:
            identifier = doc.get("identifier", "Unknown")
            download_url = fetch_download_url(identifier)
            
            doc_entry = {
                "id": identifier,
                "title": doc.get("title", title),
                "year": doc.get("year", "Unknown"),
                "author": author,
                "thumbnail_url": f"https://archive.org/services/img/{identifier}",
                "read_url": f"https://archive.org/stream/{identifier}",
                "download_url": download_url
            }
            append_to_json(doc_entry)
        
        time.sleep(1)  # Brief pause between requests

    print(f"✅ Search completed.")

if __name__ == "__main__":
    main()