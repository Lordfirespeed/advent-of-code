from bs4 import BeautifulSoup


def scrape_problem_title(problem_html_soup: BeautifulSoup) -> str:
    part_one_desc_article = problem_html_soup.find("article", class_="day-desc")
    title_h2 = part_one_desc_article.find("h2")
    title_with_decoration_and_day_number = title_h2.decode_contents()
    title_with_day_number = title_with_decoration_and_day_number.strip("- ")
    try:
        colon_index = title_with_day_number.index(":")
        return title_with_day_number[colon_index+1:].lstrip()
    except ValueError:
        return title_with_day_number
