import requests
import pandas as pd


def fetch_federal_register_updates(keyword="Egypt"):
    base_url = "https://www.federalregister.gov/api/v1/documents.json"

    params = {
        "conditions[term]": keyword,
        "conditions[type][]": "NOTICE",
        "per_page": 15,
        "order": "newest",
        "fields[]": [
            "publication_date",
            "type",
            "agencies",
            "title",
            "html_url"
        ]
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()

    results = []
    for doc in data.get("results", []):
        # Extract first agency name if available
        agency_name = "N/A"
        if doc.get("agencies"):
            agency_name = doc["agencies"][0].get("name", "N/A")

        # Only include results that mention Egypt (case-insensitive) in title or agency
        title = doc.get("title", "")
        if "egypt" not in title.lower() and "egypt" not in agency_name.lower():
            # If Egypt isn't in title, check if the term contains "egypt"
            # Only filter out if the search term specifically requires Egypt
            if "egypt" in keyword.lower():
                continue

        results.append({
            "Date": doc.get("publication_date", "N/A"),
            "Type": doc.get("type", "N/A").title(),
            "Agency": agency_name,
            "Title": title,
            "Link": doc.get("html_url", "#")
        })

    return pd.DataFrame(results)
