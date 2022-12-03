# -*- coding: utf-8 -*- #
import json
from datetime import datetime
from matplotlib import pyplot


class PSJP:
    def __init__(self, data: dict):
        def _month():
            month_list = []
            for day in data.keys():
                date = datetime.fromisoformat(day)
                month = date.strftime("%-y年%-m月")
                data[day]["month"] = month
                if month not in month_list:
                    month_list.append(month)
            return month_list

        self.month = _month()
        len_month = len(self.month)
        self.problem = [0 for _ in range(len_month)]
        self.favorite = [0 for _ in range(len_month)]
        self.answered = [0 for _ in range(len_month)]
        self.users_post = [set() for _ in range(len_month)]
        self.users_answer = [set() for _ in range(len_month)]
        self.problems_favorited = [set() for _ in range(len_month)]
        self.problems_answered = [set() for _ in range(len_month)]
        for d in data.values():
            index = self.month.index(d["month"])
            self.problem[index] += d["problem_n"]
            self.favorite[index] += d["favorite_n"]
            self.answered[index] += d["answered_n"]
            self.users_post[index] |= set(d["user"]["post"])
            self.users_answer[index] |= set(d["user"]["answer"])
            self.problems_favorited[index] |= set(d["problem"]["favorited"])
            self.problems_answered[index] |= set(d["problem"]["answered"])

    def get_user_stack(self):
        stack_0 = [len(self.users_answer[n] - self.users_post[n]) for n in range(len(self.month))]
        stack_1 = [stack_0[n] + len(self.users_answer[n] & self.users_post[n]) for n in range(len(self.month))]
        stack_2 = [stack_1[n] + len(self.users_post[n] - self.users_answer[n]) for n in range(len(self.month))]
        return stack_0, stack_1, stack_2

    def get_problem_stack(self):
        stack_0 = [len(self.problems_favorited[n]) for n in range(len(self.month))]
        stack_1 = [len(self.problems_answered[n] | self.problems_favorited[n]) for n in range(len(self.month))]
        return stack_0, stack_1


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def plot(psjp: PSJP):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'

    def _set():
        pyplot.figure(figsize=[20, 7])
        pyplot.xlabel("")
        pyplot.xticks(rotation=50)
        pyplot.ylabel("")
        pyplot.grid(axis="y", which="both", c="grey")
        pyplot.tick_params(width=0, which="both")
        pyplot.subplot().margins(0.01, 0.05)

    def _div(list, div: int):
        return [int(d / div) for d in list]

    _set()
    pyplot.title("毎月の活動量（全体）")
    pyplot.plot(psjp.month, psjp.problem, color="b", marker="*", label="投稿数", zorder=3)
    pyplot.plot(psjp.month, _div(psjp.favorite, 10), color="orange", marker="+", label="いいね数÷10", zorder=3)
    pyplot.plot(psjp.month, _div(psjp.answered, 100), color="g", marker=".", label="解答登録数÷100", zorder=3)
    pyplot.legend()
    pyplot.savefig("graph/activity-all.png")

    _set()
    pyplot.title("毎月の活動量（問題数）")
    pyplot.ylabel("ユニーク問題数")
    favorited, answered = psjp.get_problem_stack()
    pyplot.bar(psjp.month, answered, color="g", label="解答登録のみ", zorder=3)
    pyplot.bar(psjp.month, favorited, color="orange", label="いいねされた", zorder=3)
    pyplot.legend()
    pyplot.savefig("graph/activity-problems.png")

    _set()
    pyplot.title("毎月の活動量（ユーザー数）")
    pyplot.ylabel("ユニーク人数")
    solver, both, author = psjp.get_user_stack()
    pyplot.bar(psjp.month, author, color="b", label="投稿のみ", zorder=3)
    pyplot.bar(psjp.month, both, color="g", label="両方", zorder=3)
    pyplot.bar(psjp.month, solver, color="y", label="解答のみ", zorder=3)
    pyplot.legend()
    pyplot.savefig("graph/activity-users.png")


def main():
    data = load("data/activity.json")
    psjp = PSJP(data)
    plot(psjp)


if __name__ == '__main__':
    main()
