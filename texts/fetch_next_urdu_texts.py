import requests
import json
import time

# API endpoint for Archive.org advanced search
API_URL = "https://archive.org/advancedsearch.php"

# Output file to store the next 10,000 results
OUTPUT_FILE = "urdu_texts_next_10000.json"

# Configuration
ITEMS_PER_PAGE = 1000
START_PAGE = 11  # Start from page 11 (after the first 10,000 results)
END_PAGE = 20    # End at page 20
MAX_RETRIES = 3
TIMEOUT = 30

# Query: Filter for texts in Urdu
QUERY = 'language:"Urdu" AND mediatype:"texts"'

def fetch_docs_page(query, page):
    params = {
        "q": QUERY,
        "fl[]": "identifier,title,year,publicdate,language",
        "sort[]": "downloads desc",
        "rows": ITEMS_PER_PAGE,
        "page": page,
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
                print(f"⚠️ HTTP error {resp.status_code} on attempt {attempt+1}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                wait_time *= 2
        except Exception as e:
            print(f"⚠️ Error: {e} on attempt {attempt+1}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2
    return None

def main():
    all_docs = []
    for page in range(START_PAGE, END_PAGE + 1):
        print(f"🔍 Fetching page {page} for query: {QUERY}")
        docs = fetch_docs_page(QUERY, page)
        if docs is None:
            print("❌ Failed to fetch documents on this page after repeated attempts. Exiting.")
            break
        if not docs:
            print("✅ No more documents found. Ending pagination.")
            break
        all_docs.extend(docs)
        time.sleep(1)  # Brief pause between pages

    print(f"✅ Total documents fetched: {len(all_docs)}")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_docs, f, ensure_ascii=False, indent=2)
    print(f"📁 Saved results to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
