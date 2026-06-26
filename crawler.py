import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

START_URL = "https://help.telebotstudio.com/"

visited = set()
queue = deque([START_URL])

domain = urlparse(START_URL).netloc

while queue:
    url = queue.popleft()

    if url in visited:
        continue

    try:
        print(f"[+] {url}")
        visited.add(url)

        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            continue

        soup = BeautifulSoup(r.text, "lxml")

        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])

            parsed = urlparse(link)

            if parsed.netloc != domain:
                continue

            link = parsed.scheme + "://" + parsed.netloc + parsed.path

            if link not in visited:
                queue.append(link)

    except Exception as e:
        print(e)

print(f"\nTotal Pages: {len(visited)}")

with open("urls.txt", "w", encoding="utf8") as f:
    for url in sorted(visited):
        f.write(url + "\n")

print("Saved to urls.txt")