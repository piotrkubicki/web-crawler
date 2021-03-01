import requests
import re

from bs4 import BeautifulSoup
from typing import Dict, List, Set

from config import WEBSITE_URL


def extract_links_from_url(url: str) -> Set[str]:
    res = requests.get(url)
    print(res.text)
    page_content = BeautifulSoup(res.text, "html.parser")
    links = page_content.find_all("a")
    return {link["href"] for link in links}


def is_not_external_link(url: str, base_url: str = WEBSITE_URL) -> bool:
    result = re.search(base_url, url)
    if result:
        return True
    return False


def filter_external_links(links: List[str], base_url: str = WEBSITE_URL) -> List[str]:
    return [link for link in links if is_not_external_link(link, base_url)]


def create_map(
    url: str, links: List[str], base_url: str = WEBSITE_URL
) -> Dict[str, str]:
    if url == base_url:
        return {"index": links}
    return {url: links}


if __name__ == "__main__":
    links = extract_links_from_url(WEBSITE_URL)
    filtered_links = filter_external_links(links)
    page_map = create_map(WEBSITE_URL, filtered_links)
