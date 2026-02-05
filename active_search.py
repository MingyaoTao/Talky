# 202602 search tool
# this will determine whether we need to search
# perform the search, and 

import requests
import webbrowser
from bs4 import BeautifulSoup

def smart_search(query):
    # 1. Level 1: Try the invisible, lightweight way first
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        # Check if we got blocked by Cloudflare
        if "detected" in response.text or "Cloudflare" in response.text or response.status_code != 200:
            raise Exception("Blocked by bot detection")
            
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract snippets (Google's results text)
        results = [div.get_text() for div in soup.find_all("div", class_="VwiC3b")][:3]
        return "\n".join(results)

    except Exception as e:
        # 2. Level 2: The "Headed" Fallback
        # This opens the user's actual browser (Chrome/Edge/Safari)
        print(f"⚠️ Lightweight search blocked. Opening your browser for: {query}")
        webbrowser.open(url)
        return "I had to open your browser to see the results. Please look at the search page that just popped up."

# Usage
# search_data = smart_search("2018 Honda Clarity maintenance code 0 and 1")