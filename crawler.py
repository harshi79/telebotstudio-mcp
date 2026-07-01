"""
Web crawler for fetching TeleBot Studio documentation pages.

Crawls the official documentation site starting from the root URL,
collects all internal links within the same domain, and saves the
list of discovered URLs to urls.txt.

Usage:
    python crawler.py

Output:
    urls.txt — one URL per line, sorted alphabetically
"""

from __future__ import annotations

import logging
import sys
from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)
logger = logging.getLogger("crawler")

DEFAULT_START_URL = "https://help.telebotstudio.com/"
DEFAULT_OUTPUT = "urls.txt"
DEFAULT_TIMEOUT = 20


def crawl(start_url: str, timeout: int = DEFAULT_TIMEOUT) -> list[str]:
    """
    Crawl the documentation site starting from the given URL.

    Args:
        start_url: The root URL to begin crawling from.
        timeout: HTTP request timeout in seconds.

    Returns:
        Sorted list of discovered URLs within the same domain.
    """
    visited: set[str] = set()
    queue: deque[str] = deque([start_url])
    domain = urlparse(start_url).netloc

    while queue:
        url = queue.popleft()

        if url in visited:
            continue

        try:
            logger.info("Crawling: %s", url)
            visited.add(url)

            response = requests.get(url, timeout=timeout)
            if response.status_code != 200:
                logger.warning("  Status %d for %s", response.status_code, url)
                continue

            soup = BeautifulSoup(response.text, "lxml")

            for a_tag in soup.find_all("a", href=True):
                link = urljoin(url, a_tag["href"])
                parsed = urlparse(link)

                # Stay within the same domain
                if parsed.netloc != domain:
                    continue

                # Normalize: strip query params and fragments
                normalized = parsed.scheme + "://" + parsed.netloc + parsed.path

                # Skip email protection links
                if "/l/email-protection" in normalized:
                    continue

                if normalized not in visited:
                    queue.append(normalized)

        except requests.Timeout:
            logger.warning("  Timeout: %s", url)
        except requests.ConnectionError:
            logger.warning("  Connection error: %s", url)
        except Exception as e:
            logger.error("  Error crawling %s: %s", url, e)

    return sorted(visited)


def main() -> None:
    start_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_START_URL
    output_file = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT

    logger.info("Starting crawl at: %s", start_url)

    urls = crawl(start_url)

    logger.info("Total pages discovered: %d", len(urls))

    with open(output_file, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")

    logger.info("URLs saved to %s", output_file)


if __name__ == "__main__":
    main()
