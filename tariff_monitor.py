import requests
import pandas as pd

def fetch_federal_register_updates(keyword="Egypt"):
    # Using the Federal Register API (free, no key needed)
    base_url = "https://www.federalregister.gov/api/v1/documents.json"
    
    params = {
        "conditions[term]": keyword,
        "conditions[type][]": "Notice",
        "per_page": 5,
        "order": "newest"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        return pd.DataFrame()
        
    data = response.json()
    
    results = []
    for doc in data.get("results", []):
        results.append({
            "Date": doc["publication_date"],
            "Title": doc["title"],
            "Link": doc["html_url"]
        })
    
    return pd.DataFrame(results)
