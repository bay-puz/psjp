# -*- coding: utf-8 -*- #
import argparse
import json


class PSJP:
    def __init__(self, users: dict, problems: dict) -> None:
        self.users = users
        self.problems = problems

    def get_user_name(self, u_id: int) -> str:
        user = str(u_id)
        if user not in self.users:
            return "存在しないユーザー"
        return self.users[user]["name"]

    def get_difficulty(self, p_id: int) -> int:
        prob = str(p_id)
        if prob not in self.problems:
            return 0
        return self.problems[prob]["difficulty"]


def load(file: str) -> dict:
    with open(file, encoding='utf8') as f:
        return json.load(f)


def write(data: dict, file: str) -> None:
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f)


def get_solvers_dict(answered: dict) -> dict:
    solvers = {}
    for ans in answered.values():
        u_id = str(ans['user'])
        if u_id not in solvers:
            solvers[u_id] = []
        solvers[u_id].append(ans['prob'])
    return solvers


def make_solver_item(u_id: int, psjp: PSJP) -> dict:
    user_name = psjp.get_user_name(u_id)
    difficulty = [{"answer_n": 0} for _ in range(6)]
    return {"name": user_name, "answer_n": 0, "difficulty": difficulty}


def combine_solvers(solvers: dict, new: dict, psjp: PSJP) -> dict:
    for u_id, p_ids in new.items():
        if u_id not in solvers:
            solvers[u_id] = make_solver_item(u_id, psjp)
        solvers[u_id]["answer_n"] += len(p_ids)
        for p_id in p_ids:
            difficulty = psjp.get_difficulty(p_id)
            solvers[u_id]["difficulty"][difficulty]["answer_n"] += 1
    return solvers


def main():
    parser = argparse.ArgumentParser(description='解答データを解答者データに結合する')
    parser.add_argument("-s", metavar="solvers", type=str, default="data/solvers.json", help="解答者データ")
    parser.add_argument("-d", metavar="data", type=str, default="data/data.json", help="問題データ")
    parser.add_argument("-u", metavar="users", type=str, default="data/user.json", help="ユーザーデータ")
    parser.add_argument("-a", metavar="answered", type=str, help="追加のanswered")
    args = parser.parse_args()

    solvers = load(args.s)
    answered = load(args.a)

    data = load(args.d)
    users = load(args.u)
    psjp = PSJP(users, data)

    new_solvers = get_solvers_dict(answered)
    combined_solvers = combine_solvers(solvers, new_solvers, psjp)
    write(combined_solvers, args.s)


if __name__ == '__main__':
    main()
