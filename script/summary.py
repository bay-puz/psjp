# -*- coding: utf-8 -*- #
import argparse
import requests
from datetime import datetime


PSJP_API_BASE = "https://puzsq.logicpuzzle.app/api"
PSJP_API_REGISTERED_LIST = ["problem", "favorite", "answered"]
PSJP_API_INFOMATION_LIST = ["user", "kind"]


class Summary:
    def __init__(self, date: datetime) -> None:
        self.date = date
        self.problem_n = 0
        self.favorite_n = 0
        self.answered_n = 0
        self.problem_most_favorite = {"pid": 0, "count": 0}
        self.problem_most_answered = {"pid": 0, "count": 0}
    
    def show(self) -> None:
        print(self.date.strftime("＼%Y年%-m月%-d日のパズスク／"))
        print(f"📖問題数\t{self.problem_n} 問")
        print(f"❤ いいね数\t{self.favorite_n} 回")
        print(f"📝解答登録数\t{self.answered_n} 回")
        print("")

        most_favorite_p = get_problem_str(self.problem_most_favorite["pid"])
        print(f'❤ もっともいいねされた問題（{self.problem_most_favorite["count"]}回）...{most_favorite_p}')
        most_answered_p = get_problem_str(self.problem_most_answered["pid"])
        print(f'📝もっとも解答登録された問題（{self.problem_most_answered["count"]}回）...{most_answered_p}')


def get_api(url: str) -> dict:
    r = requests.get(url)
    return r.json()


def get_api_date(type: str, date: datetime) -> dict:
    if type not in PSJP_API_REGISTERED_LIST:
        return {}
    date_str = date.strftime("%Y-%m-%d")
    api_url = f"{PSJP_API_BASE}/{type}/date/{date_str}"
    return get_api(api_url)


def get_api_info(type: str) -> dict:
    if type not in PSJP_API_INFOMATION_LIST:
        return {}
    api_url = f"{PSJP_API_BASE}/{type}"
    return get_api(api_url)


def get_problem_info(pid: int) -> dict:
    api_url = f"{PSJP_API_BASE}/problem/prob/{str(pid)}"
    prob_dict = get_api(api_url)
    pid = list(prob_dict)[0]
    prob = prob_dict[str(pid)]
    author = get_user_info(prob["user"])
    puzzle = get_kind_info(prob["kind"])
    return {"pid": pid, "puzzle": puzzle["name"], "author": author["name"], "variation": prob["variation"]}


def get_problem_str(pid: int) -> str:
    prob = get_problem_info(pid)
    variant = "（変種）" if prob["variation"] else ""
    url = f'https://puzsq.logicpuzzle.app/share/{prob["pid"]}'
    prob_str = f'{prob["puzzle"]}{variant} by {prob["author"]} {url}'
    return prob_str


def get_user_info(uid: int) -> dict:
    user_dict = get_api_info("user")
    return user_dict[str(uid)]


def get_kind_info(kid: int) -> dict:
    kind_dict = get_api_info("kind")
    return kind_dict[str(kid)]


def get_summary(date: datetime) -> Summary:
    problem_dict = get_api_date("problem", date)
    favorite_dict = get_api_date("favorite", date)
    answered_dict = get_api_date("answered", date)

    summary = Summary(date)
    summary.problem_n = len(problem_dict)
    summary.favorite_n = len(favorite_dict)
    summary.answered_n = len(answered_dict)

    def _top(data: dict, key: str) -> dict:
        count = {}
        for d in data.values():
            value = d[key]
            if value not in count:
                count[value] = 0
            count[value] += 1 
        max_v = list(count)[0]
        for v, c in count.items():
            max_v = v if c > count[max_v] else max_v
        return {"pid": max_v, "count": count[max_v]}

    summary.problem_most_favorite = _top(favorite_dict, "prob")
    summary.problem_most_answered = _top(answered_dict, "prob")

    return summary


def main():
    parser = argparse.ArgumentParser(description='指定した日のPuzzle Square JPのまとめを表示する')
    parser.add_argument("day", type=str, help="日付。例：2022-11-08")
    parser.add_argument("--json", type=bool, default=False, help="JSON形式で表示する")
    args = parser.parse_args()

    day = datetime.strptime(args.day, "%Y-%m-%d")
    summary = get_summary(day)
    summary.show()


if __name__ == '__main__':
    main()