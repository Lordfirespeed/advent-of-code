from pathlib import Path

import aiohttp
from bs4 import BeautifulSoup

from advent_of_code.api import fetch_problem_html
from advent_of_code.args import AdventOfCodeArgNamespace


async def get_problem_html_soup(args: AdventOfCodeArgNamespace, session: aiohttp.ClientSession) -> BeautifulSoup:
    html_cache_path = Path(args.problem_dir, "cache", "problem.html")
    if html_cache_path.exists():
        with open(html_cache_path) as html_cache_handle:
            return BeautifulSoup(html_cache_handle, features="html.parser")

    problem_html = await fetch_problem_html(session, args.problem_year, args.problem_day)
    html_cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(html_cache_path, "w") as html_cache_handle:
        html_cache_handle.write(problem_html)
        html_cache_handle.write("\n")
    return BeautifulSoup(problem_html, features="html.parser")


async def get_problem_title(args: AdventOfCodeArgNamespace, session: aiohttp.ClientSession) -> str:
    title_cache_path = Path(args.problem_dir, "cache", "title.txt")
    if title_cache_path.exists():
        with open(title_cache_path) as title_cache_handle:
            return title_cache_handle.readline().strip()

    soup = await get_problem_html_soup(args, session)
    title = scrape_problem_title(soup)
    title_cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(title_cache_path, "w") as title_cache_handle:
        title_cache_handle.write(title)
        title_cache_handle.write("\n")
    return title


def scrape_problem_title(problem_html_soup: BeautifulSoup) -> str:
    part_one_desc_article = problem_html_soup.find("article", class_="day-desc")
    title_h2 = part_one_desc_article.find("h2")
    title_with_decoration_and_day_number = title_h2.decode_contents()
    title_with_day_number = title_with_decoration_and_day_number.strip("- ")
    try:
        colon_index = title_with_day_number.index(":")
        return title_with_day_number[colon_index + 1:].lstrip()
    except ValueError:
        return title_with_day_number
