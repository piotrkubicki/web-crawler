import requests
import re
import logging

from bs4 import BeautifulSoup
from typing import List, Set

from config import WEBSITE_URL

logging.basicConfig(filename="main.log", level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())


def extract_links_from_url(url: str) -> Set[str]:
    res = requests.get(url)
    page_content = BeautifulSoup(res.text, "html.parser")
    links = page_content.find_all("a")
    return list(set(link["href"] for link in links))


def is_not_external_link(url: str, base_url: str = WEBSITE_URL) -> bool:
    result = re.search(base_url, url)
    if result:
        return True
    return False


def filter_external_links(links: List[str], base_url: str = WEBSITE_URL) -> List[str]:
    return [link for link in links if is_not_external_link(link, base_url)]


def map_page(url: str, mapped_pages: List[str] = []):
    logging.info(f"Extracting site {url}")
    links = extract_links_from_url(url)
    mapped_pages.append(url)
    save_map(links, url)
    logging.info("Result saved")

    for link in filter_external_links(links):
        if link not in mapped_pages:
            map_page(link, mapped_pages)
        else:
            logging.info(f"Skipping {link} already mapped")


def save_map(site_map, url):
    page_name = url.replace("https://", "").replace("/", "-")
    with open(f"site_map/{page_name}.html", "w") as f:
        f.write(f"<HTML>\n<h2>URL: {url}</h2>\n")
        for link in site_map:
            f.write(f"\t<div><a href={link}>{link}</a></div>\n")
        f.write("</HTML>\n")


if __name__ == "__main__":
    logging.info("WEB-CRAWLER started...")
    map_page(url=WEBSITE_URL)
    logging.info("WEB-CRAWLER completed successfully!")
