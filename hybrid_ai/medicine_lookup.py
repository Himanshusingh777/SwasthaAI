import os
import requests
import json

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'medicines_db.json')

try:
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        LOCAL_MED_DB = json.load(f)
except:
    LOCAL_MED_DB = {}

SERPAPI_KEY = os.getenv('SERPAPI_API_KEY')

def fetch_medicine_live(name):
    if not SERPAPI_KEY:
        return None
    params = {
        "engine": "google",
        "q": f"{name} medicine uses price India",
        "hl": "en",
        "api_key": SERPAPI_KEY,
    }
    resp = requests.get("https://serpapi.com/search.json", params=params, timeout=10)
    if resp.status_code != 200:
        return None
    data = resp.json()
    try:
        organic = data.get('organic_results', [])
        if organic:
            top = organic[0]
            snippet = top.get('snippet') or top.get('title') or ""
            price_hint = "—"
            if 'shopping_results' in data and data['shopping_results']:
                price_hint = data['shopping_results'][0].get('price') or "—"
            elif 'knowledge_graph' in data:
                kg = data['knowledge_graph']
                price_hint = kg.get('price', "—") if isinstance(kg, dict) else "—"
            return {
                "name": name,
                "description_en": snippet,
                "description_hi": None,
                "price_hint": price_hint,
                "source": "serpapi",
                "raw": top
            }
    except Exception as e:
        print("SerpAPI parsing error:", e)
    return None

def fetch_medicine(name):
    key = name.strip().lower()
    live = fetch_medicine_live(name)
    if live:
        return live
    if key in LOCAL_MED_DB:
        med = LOCAL_MED_DB[key]
        return {
            "name": med.get("name"),
            "description_en": med.get("description", {}).get("english"),
            "description_hi": med.get("description", {}).get("hindi"),
            "price_hint": med.get("price_hint"),
            "similar": med.get("similarMedicines", [])
        }
    for k,v in LOCAL_MED_DB.items():
        if key in k or key in v.get('name','').lower():
            return {
                "name": v.get("name"),
                "description_en": v.get("description", {}).get("english"),
                "description_hi": v.get("description", {}).get("hindi"),
                "price_hint": v.get("price_hint"),
                "similar": v.get("similarMedicines", [])
            }
    return None
