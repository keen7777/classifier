# fetch_titles.py
import requests

def get_category_titles(category, cmcontinue=None):
    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{category}",
        "cmlimit": "500",
        "format": "json"
    }
    if cmcontinue:
        params["cmcontinue"] = cmcontinue

    resp = S.get(URL, params=params).json()
    titles = [m["title"] for m in resp["query"]["categorymembers"]]
    cont = resp.get("continue", {}).get("cmcontinue")
    return titles, cont

def grab_all_titles(category):
    all_titles = []
    cont = None
    while True:
        titles, cont = get_category_titles(category, cont)
        all_titles.extend(titles)
        if not cont:
            break
    return set(all_titles)

if __name__ == "__main__":
    categories = ["Pharmaceuticals", "Clinical research", "Biotechnology", "Drug safety"]
    matched = set()
    for cat in categories:
        titles = grab_all_titles(cat)
        matched |= titles
        print(f"{cat}: {len(titles)} pages")
    with open("wiki_med_titles.txt", "w", encoding="utf-8") as f:
        for t in sorted(matched):
            f.write(t + "\n")
    print(f"Total distinct titles: {len(matched)}")
