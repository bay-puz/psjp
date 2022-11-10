# -*- coding: utf-8 -*- #
import argparse
import json
from typing import Tuple
import requests
from datetime import datetime


PSJP_API_BASE = "https://puzsq.logicpuzzle.app/api"
PSJP_API_REGISTERED_LIST = ["problem", "favorite", "answered"]
PSJP_API_INFOMATION_LIST = ["user", "kind"]


class Puzsq:
    def __init__(self, date: datetime, problems: str="") -> None:
        self.date = date
        self.user_dict = get_api_info("user")
        self.kind_dict = get_api_info("kind")
        self.problem_dict = get_api_date("problem", date)
        self.problems = load_json(problems) if len(problems) > 0 else {}
        self.favorite_dict = get_api_date("favorite", date)
        self.answered_dict = get_api_date("answered", date)

        self.problems_fav, self.authors_fav, _ = self._count_register_dict(self.favorite_dict)
        self.problems_ans, self.authors_ans, self.solvers_ans = self._count_register_dict(self.answered_dict)

        self.most_favorited_problems = self._top(self.problems_fav)
        self.most_favorited_authors = self._top(self.authors_fav)
        self.most_answered_problems = self._top(self.problems_ans)
        self.most_answered_authors = self._top(self.authors_ans)

    def _count_register_dict(self, register_dict: dict) -> Tuple[dict, dict]:
        problems = {}
        authors = {}
        solvers = {}
        for data in register_dict.values():
            pid = data["prob"]
            prob = self.get_problem_by_pid(pid)
            if prob == {}:
                # 削除された問題は飛ばす
                continue
            if str(pid) not in problems:
                problems[str(pid)] = 0
            problems[str(pid)] += 1
            aid = prob["user"]
            if str(aid) not in authors:
                authors[str(aid)] = 0
            authors[str(aid)] += 1
            if "user" in data:
                sid = data["user"]
                if str(sid) not in solvers:
                    solvers[str(sid)] = 0
                solvers[str(sid)] += 1
        return (problems, authors, solvers)

    def _top(self, count_dict: dict) -> list:
        top_id = -1
        for cid, count in count_dict.items():
            if top_id == -1 or count_dict[str(top_id[0])] < count:
                top_id = [cid]
            elif count_dict[str(top_id[0])] == count:
               top_id.append(cid)
        return top_id

    def show(self) -> None:
        print(self.date.strftime("＼%Y年%-m月%-d日のパズスク／"))
        print(f"📖投稿数\t{len(self.problem_dict)} 問")
        print(f"❤ いいね数\t{len(self.favorite_dict)} 回")
        print(f"📝解答登録数\t{len(self.answered_dict)} 回")
        print("")
        print(f"❤ いいねされた問題📖\t{len(self.problems_fav)}問")
        print(f"❤ いいねされた作者🧑‍🎨\t{len(self.authors_fav)}人")
        print(f"📝解答登録された問題📖\t{len(self.problems_ans)}問")
        print(f"📝解答登録された作者🧑‍🎨\t{len(self.authors_ans)}人")
        print(f"📝解答登録した解き手🙆\t{len(self.solvers_ans)}人")
        print("")
        most_fav_p_c = self.problems_fav[str(self.most_favorited_problems[0])]
        print(f"❤ もっともいいねされた問題（{most_fav_p_c}回）")
        for pid in self.most_favorited_problems:
            print(f" {self.get_problem_info(pid)}")
        most_ans_p_c = self.problems_ans[str(self.most_answered_problems[0])]
        print(f"📝もっとも解答登録された問題（{most_ans_p_c}回）")
        for pid in self.most_answered_problems:
            print(f" {self.get_problem_info(pid)}")
        print("")
        most_fav_a = [f"{self.get_user_name(a)}さん" for a in self.most_favorited_authors]
        most_fav_a_c = self.authors_fav[str(self.most_favorited_authors[0])]
        print(f"❤ もっともいいねされた作者（{most_fav_a_c}回）... {'、'.join(most_fav_a)}")
        most_ans_a = [f"{self.get_user_name(a)}さん" for a in self.most_answered_authors]
        most_ans_a_c = self.authors_ans[str(self.most_answered_authors[0])]
        print(f"📝もっとも解答登録された作者（{most_ans_a_c}回）... {'、'.join(most_ans_a)}")

    def get_problem_by_pid(self, pid) -> dict:
        if str(pid) in self.problem_dict:
            return self.problem_dict[str(pid)]
        if str(pid) in self.problems:
            return self.problems[str(pid)]
        problem = get_api_prob(pid)
        self.problems[str(pid)] = problem
        return problem

    def get_user_name(self, uid: int) -> str:
        return self.user_dict[str(uid)]["name"]

    def get_kind_name(self, kid: int) -> str:
        return self.kind_dict[str(kid)]["name"]

    def get_problem_info(self, pid: int) -> str:
        url = f"https://puzsq.logicpuzzle.app/share/{pid}"
        prob = self.get_problem_by_pid(pid)
        if len(prob) == 0:
            return f"削除された問題 {url}"
        author = self.get_user_name(prob["user"])
        puzzle = self.get_kind_name(prob["kind"])
        variation = "（変種）" if prob["variation"] else ""
        return f'{puzzle}{variation} by {author} {url}'


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


def get_api_prob(pid: int) -> dict:
    api_url = f"{PSJP_API_BASE}/problem/prob/{str(pid)}"
    prob_dict = get_api(api_url)
    if len(prob_dict) == 0:
        # 削除された問題
        return {}
    return prob_dict[str(pid)]


def load_json(file: str) -> dict:
    with open(file) as f:
        return json.load(f)

def get_problem_str(prob: dict) -> str:
    variant = "（変種）" if prob["variation"] else ""
    url = f'https://puzsq.logicpuzzle.app/share/{prob["pid"]}'
    prob_str = f'{prob["puzzle"]}{variant} by {prob["author"]} {url}'
    return prob_str


def main():
    parser = argparse.ArgumentParser(description='指定した日のPuzzle Square JPのまとめを表示する')
    parser.add_argument("day", type=str, help="日付。例：2022-11-08")
    parser.add_argument("-p", metavar="problem_file", type=str, default="", help="問題データが載ったファイル（APIの代わりに使う）")
    args = parser.parse_args()

    date = datetime.strptime(args.day, "%Y-%m-%d")
    puzsq = Puzsq(date, problems=args.p)
    puzsq.show()


if __name__ == '__main__':
    main()