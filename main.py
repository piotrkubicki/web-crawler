import requests
import re
import logging
import logging.config
import yaml

from bs4 import BeautifulSoup
from typing import List
from threading import Thread
from queue import Queue

from config import WEBSITE_URL


mapping_queue = Queue(maxsize=0)


def set_logger():
    with open("logging.yaml") as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def extract_links_from_url(url: str) -> List[str]:
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


def save_result(links: List[str], url: str, path: str = "site_map") -> None:
    page_name = url.replace("https://", "").replace("/", "-")
    with open(f"{path}/{page_name}.html", "w") as f:
        f.write(f"<HTML>\n\t<h2>URL: {url}</h2>\n")
        for link in links:
            f.write(f"\t<div><a href={link}>{link}</a></div>\n")
        f.write("</HTML>\n")


def map_page(mapped_pages: List[str], mapping_queue: Queue) -> None:
    while True:
        url = mapping_queue.get(timeout=5)
        if url in mapped_pages:
            mapping_queue.task_done()
            continue
        logging.info(f"Extracting site {url}")
        links = extract_links_from_url(url)
        mapped_pages.append(url)
        save_result(links, url)
        logging.info("Result saved")

        for link in filter_external_links(links):
            if link not in mapped_pages:
                mapping_queue.put(link)
        mapping_queue.task_done()
        if mapping_queue.qsize() == 0:
            break


if __name__ == "__main__":
    set_logger()
    logging.info("WEB-CRAWLER started...")
    mapping_queue.put(WEBSITE_URL)
    mapped_pages = []
    for i in range(15):
        page_mapper_thread = Thread(
            target=map_page,
            args=(
                mapped_pages, mapping_queue
            ),
            daemon=True,
        )
        page_mapper_thread.start()
    mapping_queue.join()
    logging.info("WEB-CRAWLER completed successfully!")
