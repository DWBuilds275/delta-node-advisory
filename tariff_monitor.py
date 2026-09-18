import requests
import pandas as pd

def fetch_federal_register_updates(keyword="Egypt"):
    base_url = "https://www.federalregister.gov/api/v1/documents.json"
    
    # Broader search: match any of these terms
    params = {
        "conditions[term]": "Egypt tariff trade",
        "per_page": 10,
        "order": "newest"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        return pd.DataFrame()
        
    data = response.json()
    
    results = []
    for doc in data.get("results", []):
        results.append({
            "Date": doc.get("publication_date", "N/A"),
            "Type": doc.get("type", "N/A"),
            "Agency": ", ".join(doc.get("agencies", [{}])[0].get("name", "N/A") for _ in [0]) if doc.get("agencies") else "N/A",
            "Title": doc.get("title", "No title"),
            "Link": doc.get("html_url", "#")
        })
    
    return pd.DataFrame(results)
