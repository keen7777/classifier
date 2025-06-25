import wikipediaapi
import time
from pathlib import Path

# 初始化 Wikipedia API，设置合法 user-agent
wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='my-classifier-project/0.1 (keen@example.com)'  # 请替换为你的联系方式或项目说明
)

keywords = ["Life science", 
            "Medical Technology",
            "Health information exchange", 
            "Pharmaceutical industry",
            "pharmaceutical drug", 
            "GxP",
            "Medical imaging",
            "bio-medicine",
            "Robot-assisted surgery",
            "Assistive technologies",
            "healthcare software",
            "Good clinical practice"]
output_dir = Path("wiki_articles")
output_dir.mkdir(exist_ok=True)

def get_full_text(page):
    """
    递归获取页面全文，包括所有子章节内容，拼成一个完整字符串。
    """
    text = page.text or ""
    for section in page.sections:
        text += "\n\n" + section.title + "\n\n" + get_full_text(section)
    return text

for word in keywords:
    print(f"Fetching page: {word}")
    page = wiki.page(word)

    if not page.exists():
        print(f"⚠️ Page '{word}' not found.")
        continue

    full_text = get_full_text(page)
    filename = output_dir / f"{word.replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Title: {page.title}\n\n")
        f.write(full_text)

    print(f"✅ Saved full content to: {filename}\n")
    time.sleep(2)
