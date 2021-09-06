# -*- coding: utf-8 -*-
import argparse
import json
import re
import requests
from bs4 import BeautifulSoup
from sys import stderr
from time import sleep


PSJP_URL = 'https://puzsq.jp/main/index.php'
OLDEST_PROBLEM_ID = 2
MIN_PAGE_ID = 1
MAX_PAGE_ID = 10000


def get_psjp(page_id: int = 0):
    url = "{}?puzzle=0&author=0&page={}".format(PSJP_URL, page_id)

    try:
        r = requests.get(url, timeout=30)
    except Exception as e:
        print(e, file=stderr)
        print("error page: {}".format(page_id), file=stderr)
        return None

    return r.text


def get_id(problem_soup):
    href_text = problem_soup['href']
    PATTERN_ID = r'[0-9]+'
    matched = re.search(PATTERN_ID, href_text)
    if matched is None:
        return None
    return int(matched.group(0))


def get_liked(problem_soup):
    liked_find = problem_soup.find('span', class_='favorite')
    if liked_find is None:
        return None
    return int(liked_find.get_text().replace('❤', ''))


def get_puzzle(problem_soup):
    puzzle_find = problem_soup.find('a', class_='puz_kind')
    if puzzle_find is None:
        return (0, None)
    puzzle_text = puzzle_find.get_text()
    puzzle_str = 'その他' if puzzle_text == '' else puzzle_text

    PATTERN_PUZZLE_ID = r'(?<=puzzle=)-?[0-9]+'
    puzzle_id_re = re.search(PATTERN_PUZZLE_ID, puzzle_find['href'])
    if puzzle_id_re is None:
        return (0, None)
    puzzle_id = int(puzzle_id_re.group(0))

    return (puzzle_id, puzzle_str)


def get_author(problem_soup):
    author_find = problem_soup.find('a', class_='author')
    if author_find is None:
        return (0, None)
    PATTERN_AUTHOR = r'(?<=作：)[^<]+'
    author_re = re.search(PATTERN_AUTHOR, author_find.get_text())
    if author_re is None:
        return (0, None)

    PATTERN_AUTHOR_ID = r'(?<=author=)[0-9]+'
    author_id_re = re.search(PATTERN_AUTHOR_ID, author_find['href'])
    if author_id_re is None:
        return (0, None)
    author_id = int(author_id_re.group(0))

    return (author_id, author_re.group(0))


def get_date(problem_soup):
    date_find = problem_soup.find('span', class_='registered')
    if date_find is None:
        return None
    return date_find.get_text()


def get_variant(problem_soup):
    variant_find = problem_soup.find('span', class_='puz_variant')
    return 0 if variant_find is None else 1


def get_difficulty(problem_soup):
    difficulty_find = problem_soup.find('span', class_='difficulty')
    difficulty = re.search(r'[0-9]', difficulty_find.get_text()).group(0)
    return int(difficulty)


def problem_dict(problem_soup):
    problem_id = get_id(problem_soup)
    if problem_id is None:
        print("error: id=None, soup={}".format(problem_soup), file=stderr)
        return {}

    liked = get_liked(problem_soup)
    if liked is None:
        print("error: id={}, liked=None, soup={}".format(problem_id, problem_soup), file=stderr)
        return {}

    puzzle_id, puzzle_name = get_puzzle(problem_soup)
    author_id, author_name = get_author(problem_soup)
    date_str = get_date(problem_soup)
    variant_int = get_variant(problem_soup)
    difficulty_int = get_difficulty(problem_soup)

    if puzzle_name is None or author_name is None or date_str is None:
        print("warning: id={}, puzzle_name={}, author_name={}, created_at={}"\
            .format(problem_id, puzzle_name, author_namem, date_str), file=stderr)

    data = {
            "id": problem_id, \
            "liked": liked, \
            "author_id": author_id, \
            "author_name": author_name, \
            "puzzle_name": puzzle_name, \
            "puzzle_id": puzzle_id, \
            "variant": variant_int, \
            "created_at": date_str, \
            "difficulty": difficulty_int
            }
    return data


def loop():
    page_id = MIN_PAGE_ID
    while True:
        psjp_page = get_psjp(page_id)

        soup = BeautifulSoup(psjp_page, 'html.parser')
        problem_list = soup.body.find('div', id='puz_table').find_all('a', class_='puz_card_index')

        for p in problem_list:
            data = problem_dict(p)
            print(json.dumps(data))

            if data['id'] == OLDEST_PROBLEM_ID:
                return True

        page_id += 1
        if page_id > MAX_PAGE_ID:
            break
        sleep(5)


def main():
    parser = argparse.ArgumentParser(description='Puzzle Square JPからいいね数などを得る')
    args = parser.parse_args()

    loop()


if __name__ == '__main__':
    main()
