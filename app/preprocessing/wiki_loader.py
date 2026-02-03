import requests
import urllib.parse

def fetch_wikipedia(query: str):
    try:
        encoded_query = urllib.parse.quote(query)
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"

        headers = {
            "User-Agent": "AgenticAIResearchBot/1.0 (student project)"
        }

        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            print(f"⚠️ Wikipedia HTTP {response.status_code}")
            return None

        data = response.json()

        # Some pages exist but have no summary
        if not data.get("extract"):
            print("⚠️ No extract found in response")
            return None

        print("✅ Wikipedia data found for", query)

        return {
            "source": "wikipedia",
            "text": data["extract"]
        }

    except Exception as e:
        print("❌ Wikipedia fetch error:", e)
        return None
