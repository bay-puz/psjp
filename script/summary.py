# -*- coding: utf-8 -*- #
import argparse
import json
from datetime import datetime
from typing import Tuple

import requests

PSJP_API_BASE = "https://puzsq.logicpuzzle.app/api"
PSJP_API_REGISTERED_LIST = ["problem", "favorite", "answered"]
PSJP_API_INFOMATION_LIST = ["user", "kind"]


class Puzsq:
    def __init__(self, date: datetime, problems: str = "") -> None:
        self.date = date
        self.problems = load_json(problems) if len(problems) > 0 else {}
        self._setup()

    def _setup(self) -> None:
        self.user_dict = get_api_info("user")
        self.kind_dict = get_api_info("kind")
        self.problem_dict = get_api_date("problem", self.date)
        self.favorite_dict = get_api_date("favorite", self.date)
        self.answered_dict = get_api_date("answered", self.date)

    def _count_register_dict(self, register_dict: dict) -> Tuple[dict, dict, dict]:
        problems = {}
        authors = {}
        solvers = {}
        for data in register_dict.values():
            pid = data["prob"]
            prob = self.get_problem_by_pid(pid)
            if len(prob) == 0:
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

    def get_summary(self) -> dict:
        summary = {}
        summary["day"] = self.date.strftime("%Y年%-m月%-d日")
        summary["total"] = {"problem": len(self.problem_dict),
                            "favorite": len(self.favorite_dict),
                            "answered": len(self.answered_dict)}

        problems_fav, authors_fav, _ = self._count_register_dict(self.favorite_dict)
        problems_ans, authors_ans, solvers_ans = self._count_register_dict(self.answered_dict)
        summary["detail"] = {}
        summary["detail"]["favorite"] = {"problem": len(problems_fav), "author": len(authors_fav)}
        summary["detail"]["answered"] = {"problem": len(problems_ans), "author": len(authors_ans), "solver": len(solvers_ans)}

        def _top(count_dict: dict) -> Tuple[int, list]:
            top_id = [-1]
            for cid, count in count_dict.items():
                if top_id[0] == -1 or count_dict[str(top_id[0])] < count:
                    top_id = [cid]
                elif count_dict[str(top_id[0])] == count:
                    top_id.append(cid)
            return (count_dict[str(top_id[0])], top_id)

        summary["top"] = {"problem": {}, "author": {}, "solver": {}}
        most_favorited_problems_c, ids = _top(problems_fav)
        most_favorited_problems = [self.get_problem_info(p) for p in ids]
        summary["top"]["problem"]["favorite"] = {"count": most_favorited_problems_c, "names": most_favorited_problems}
        most_answered_problems_c, ids = _top(problems_ans)
        most_answered_problems = [self.get_problem_info(p) for p in ids]
        summary["top"]["problem"]["answered"] = {"count": most_answered_problems_c, "names": most_answered_problems}
        most_favorited_authors_c, ids = _top(authors_fav)
        most_favorited_authors = [self.get_user_name(p) for p in ids]
        summary["top"]["author"]["favorite"] = {"count": most_favorited_authors_c, "names": most_favorited_authors}
        most_answered_authors_c, ids = _top(authors_ans)
        most_answered_authors = [self.get_user_name(p) for p in ids]
        summary["top"]["author"]["answered"] = {"count": most_answered_authors_c, "names": most_answered_authors}
        most_answer_solvers_c, ids = _top(solvers_ans)
        most_answer_solvers = [self.get_user_name(p) for p in ids]
        summary["top"]["solver"]["answered"] = {"count": most_answer_solvers_c, "names": most_answer_solvers}

        return summary

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


def show(data: Puzsq) -> None:
    summary = data.get_summary()
    print(f'＼{summary["day"]}のパズスク／')
    print(f'📖投稿数\t{summary["total"]["problem"]} 問')
    print(f'❤ いいね数\t{summary["total"]["favorite"]} 回')
    print(f'📝解答登録数\t{summary["total"]["answered"]} 回')
    print('')
    print(f'❤ いいねされた問題📖 {summary["detail"]["favorite"]["problem"]}問')
    print(f'❤ いいねされた作者🧑‍🎨 {summary["detail"]["favorite"]["author"]}人')
    print(f'📝解答登録された問題📖 {summary["detail"]["answered"]["problem"]}問')
    print(f'📝解答登録された作者🧑‍🎨 {summary["detail"]["answered"]["author"]}人')
    print(f'📝解答登録した解き手🙆 {summary["detail"]["answered"]["solver"]}人')
    print('')
    print(f'❤ もっともいいねされた問題📖（{summary["top"]["problem"]["favorite"]["count"]}回）')
    for name in summary["top"]["problem"]["favorite"]["names"]:
        print(f' {name}')
    print(f'📝もっとも解答登録された問題📖（{summary["top"]["problem"]["answered"]["count"]}回）')
    for name in summary["top"]["problem"]["answered"]["names"]:
        print(f' {name}')
    print('')
    users = [f"{n} さん" for n in summary["top"]["author"]["favorite"]["names"]]
    print(f'❤ もっともいいねされた作者🧑‍🎨（{summary["top"]["author"]["favorite"]["count"]}回） {"、".join(users)}')
    users = [f"{n} さん" for n in summary["top"]["author"]["answered"]["names"]]
    print(f'📝もっとも解答登録された作者🧑‍🎨（{summary["top"]["author"]["answered"]["count"]}回） {"、".join(users)}')
    users = [f"{n} さん" for n in summary["top"]["solver"]["answered"]["names"]]
    print(f'📝もっとも解答登録した解き手🙆（{summary["top"]["solver"]["answered"]["count"]}回） {"、".join(users)}')


def main():
    parser = argparse.ArgumentParser(description='指定した日のPuzzle Square JPのまとめを表示する')
    parser.add_argument("day", type=str, help="日付。例：2022-11-08")
    parser.add_argument("-p", metavar="problem_file", type=str, default="", help="問題データが載ったファイル（APIの代わりに使う）")
    args = parser.parse_args()

    date = datetime.strptime(args.day, "%Y-%m-%d")
    puzsq = Puzsq(date, problems=args.p)
    show(puzsq)


if __name__ == '__main__':
    main()
