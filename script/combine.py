# -*- coding: utf-8 -*- #
import argparse
import json


def load(file: str) -> dict:
    with open(file, encoding='utf8') as f:
        return json.load(f)


def write(data: dict, file: str) -> None:
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f)


def combine(base: dict, problems: dict, favorites: dict, answered: dict) -> dict:
    fav_n = 'favorite_n'
    ans_n = 'answered_n'
    for p_id, problem in problems.items():
        if p_id in base:
            problem[fav_n] = base[str(p_id)][fav_n]
            problem[ans_n] = base[str(p_id)][ans_n]
        else:
            problem[fav_n] = 0
            problem[ans_n] = 0
        problem["id"] = p_id
        base[p_id] = problem

    for fav in favorites.values():
        p_id = str(fav['prob'])
        # 問題が削除されていることがあるのでチェックする
        if p_id not in base:
            continue
        base[p_id][fav_n] += 1

    for ans in answered.values():
        p_id = str(ans['prob'])
        # 問題が削除されていることがあるのでチェックする
        if p_id not in base:
            continue
        base[p_id][ans_n] += 1

    return base


def add_activity(activity: dict, problems: dict, favorites: dict, answered: dict, day: str) -> dict:
    def _init() -> dict:
        d = {"problem_n": 0, "favorite_n": 0, "answered_n": 0, "user": {}, "problem": {}}
        d["user"] = {"authors": 0, "solvers": 0, "both": 0}
        d["problem"] = {"answered": 0, "favorited": 0}
        return d

    today_dict = _init()
    today_dict["problem_n"] = len(problems)
    today_dict["favorite_n"] = len(favorites)
    today_dict["answered_n"] = len(answered)

    def _count(type: str, data: dict) -> dict:
        count = {}
        for d in data.values():
            name = d[type]
            if name not in count:
                count[name] = 0
            count[name] += 1
        return count

    favorited_p = _count("prob", favorites)
    answered_p = _count("prob", answered)
    today_dict["problem"]["favorited"] = len(favorited_p)
    today_dict["problem"]["answered"] = len(answered_p)

    authors = _count("user", problems)
    solvers = _count("user", answered)
    today_dict["user"]["authors"] = len(authors)
    today_dict["user"]["solvers"] = len(solvers)

    count_author_solver = 0
    for author in authors.keys():
        if author in solvers:
            count_author_solver += 1
    today_dict["user"]["both"] = count_author_solver

    activity[day] = today_dict
    return activity


def main():
    parser = argparse.ArgumentParser(description='日付を指定したデータを結合する')
    parser.add_argument("--base", metavar="base", type=str, default="data/data.json", help="問題データ")
    parser.add_argument("--activity", metavar="activity", type=str, default="data/activity.json", help="問題データ")
    parser.add_argument("-d", metavar="date", type=str, help="データの日付")
    parser.add_argument("-p", metavar="problem", type=str, help="追加のproblem")
    parser.add_argument("-f", metavar="favorite", type=str, help="追加のfavorite")
    parser.add_argument("-a", metavar="answered", type=str, help="追加のanswered")
    args = parser.parse_args()

    base = load(args.base)
    activity = load(args.activity)
    problems = load(args.p)
    favorites = load(args.f)
    answered = load(args.a)

    combined = combine(base, problems, favorites, answered)
    write(combined, args.base)

    combined_activity = add_activity(activity, problems, favorites, answered, args.d)
    write(combined_activity, args.activity)


if __name__ == '__main__':
    main()
