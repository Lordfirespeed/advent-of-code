from urllib.parse import urljoin

import aiohttp

api_host = "https://adventofcode.com"


def advent_of_code_session(session_token: str) -> aiohttp.ClientSession:
    return aiohttp.ClientSession(cookies={"session": session_token})


async def fetch_problem_input(session: aiohttp.ClientSession, year: int, day: int) -> str:
    async with session.get(urljoin(api_host, f"{year}/day/{day}/input")) as response:
        response.raise_for_status()
        return await response.text()


async def fetch_problem_html(session: aiohttp.ClientSession, year: int, day: int) -> str:
    async with session.get(urljoin(api_host, f"{year}/day/{day}")) as response:
        response.raise_for_status()
        return await response.text()
