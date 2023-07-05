from pathlib import Path

import jsonargparse
import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger

from newsfeed import log_utils
from newsfeed.datatypes import BlogInfo

LINK_TO_XML_FILE = {
    "lastweekinai": "https://lastweekin.ai/feed",
    "mit": "https://news.mit.edu/rss/topic/artificial-intelligence2",
}


def save_metadata_info(blog_name: str) -> BeautifulSoup:
    blog_url = LINK_TO_XML_FILE[blog_name]

    response = requests.get(blog_url)
    xml_text = response.text
    path_xml_dir = Path("data/datasets") / blog_name
    path_xml_dir.mkdir(exist_ok=True, parents=True)
    with open(path_xml_dir / "metadata.xml", "w") as f:
        f.write(xml_text)

    parsed_xml = BeautifulSoup(xml_text, "xml")
    return parsed_xml


def get_articles(parsed_xml: BeautifulSoup) -> list[BlogInfo]:
    articles = []
    for item in parsed_xml.find_all("item"):
        raw_blog_text = item.find("content:encoded").text
        soup = BeautifulSoup(raw_blog_text, "html.parser")
        blog_text = soup.get_text()
        article_info = BlogInfo(
            title=item.title.text,
            description=item.description.text,
            published=pd.to_datetime(item.pubDate.text).date(),
            link=item.link.text,
            blog_text=blog_text,
        )
        articles.append(article_info)

    return articles


def save_articles(articles: list[BlogInfo], blog_name: str) -> None:
    save_dir = Path("data/datasets", blog_name, "articles")
    save_dir.mkdir(exist_ok=True, parents=True)
    for article in articles:
        save_path = save_dir / article.filename
        with open(save_path, "w") as f:
            f.write(article.json(indent=2))


def main(blog_name: str) -> None:
    logger.debug(f"Processing {blog_name}")
    parsed_xml = save_metadata_info(blog_name)
    articles = get_articles(parsed_xml)
    save_articles(articles, blog_name)
    logger.debug(f"Done processing {blog_name}")


def parse_args() -> jsonargparse.Namespace:
    parser = jsonargparse.ArgumentParser()
    parser.add_function_arguments(main)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    log_utils.configure_logger(log_level="DEBUG")
    main(**args)
