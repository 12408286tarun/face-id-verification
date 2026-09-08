from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
serpapi_key = os.getenv("SERPAPI_KEY")


def search_module(image_url):
    params = {
        "engine": "google_reverse_image",
        "image_url": image_url,
        "api_key": serpapi_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "image_results" in results and len(results["image_results"]) > 0:
        first_match = results["image_results"][0]
        return {
            "title": first_match.get("title", "N/A"),
            "url": first_match.get("link", "N/A"),
            "source": first_match.get("source", "N/A"),
            "snippet": first_match.get("snippet", "N/A")
        }
    else:
        return None

if __name__ == "__main__":
    test_image_url = "https://i.ibb.co/xt4ztWV9/simple-iamge.jpg"
    result = search_module(test_image_url)
    print("Search Result:", result)