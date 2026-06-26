import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

os.makedirs("docs", exist_ok=True)

with open("urls.txt", "r", encoding="utf-8") as f:
    urls = [u.strip() for u in f if u.strip()]

for url in urls:
    if url.endswith("/l/email-protection"):
        continue

    try:
        print("Downloading:", url)

        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            continue

        soup = BeautifulSoup(r.text, "lxml")

        # Remove unnecessary elements
        for tag in soup(["script", "style", "noscript", "footer", "header"]):
            tag.decompose()

        md = markdownify(str(soup), heading_style="ATX")

        name = url.rstrip("/").split("/")[-1]
        if not name:
            name = "index"

        if not name.endswith(".md"):
            name += ".md"

        with open(os.path.join("docs", name), "w", encoding="utf-8") as f:
            f.write(md)

    except Exception as e:
        print(e)

print("Done!")