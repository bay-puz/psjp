# -*- coding: utf-8 -*- #
import json
from datetime import datetime
from matplotlib import pyplot


class PSJP:
    def __init__(self, data: dict):
        self.month = []
        len_month = self._month(data)
        self.problem = [0 for _ in range(len_month)]
        self.favorite = [0 for _ in range(len_month)]
        self.answered = [0 for _ in range(len_month)]
        self.favorite_p = [0 for _ in range(len_month)]
        self.answered_p = [0 for _ in range(len_month)]
        self._setup(data)

        self.answered_100 = [int(n / 100) for n in self.answered]
        self.favorite_10 = [int(n / 10) for n in self.favorite]

        self.day = [k for k in data.keys()]
        self.author = [d["user"]["authors"] for d in data.values()]
        self.solver = [d["user"]["solvers"] for d in data.values()]
        self.author_solver = [d["user"]["both"] for d in data.values()]

    def _month(self, data: dict):
        month_list = []
        for day in data.keys():
            date = datetime.fromisoformat(day)
            month = date.strftime("%y/%m")
            data[day]["month"] = month
            if month not in month_list:
                month_list.append(month)
        self.month = month_list
        return len(month_list)

    def _setup(self, data: dict):
        for d in data.values():
            index = self.month.index(d["month"])
            self.problem[index] += d["problem_n"]
            self.favorite[index] += d["favorite_n"]
            self.answered[index] += d["answered_n"]
            self.favorite_p[index] += d["problem"]["favorited"]
            self.answered_p[index] += d["problem"]["answered"]

    def get_user_stack(self):
        stack_0 = self.solver
        stack_1 = [stack_0[n] + self.author_solver[n] for n in range(len(stack_0))]
        stack_2 = [stack_1[n] + self.author[n] for n in range(len(stack_0))]
        return stack_0, stack_1, stack_2


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def plot(psjp: PSJP):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'

    def _set():
        pyplot.figure(figsize=[20, 7])
        pyplot.title("毎月の活動量")
        pyplot.xlabel("")
        pyplot.xticks(rotation=50)
        pyplot.ylabel("")
        pyplot.grid(axis="y", which="both", c="grey")
        pyplot.tick_params(width=0, which="both")
        pyplot.subplot().margins(0.01, 0.05)

    _set()
    pyplot.plot(psjp.month, psjp.problem, color="b", label="投稿数", zorder=3)
    pyplot.plot(psjp.month, psjp.favorite_10, color="orange", label="いいね数÷10", zorder=3)
    pyplot.plot(psjp.month, psjp.answered_100, color="g", label="解答登録数÷100", zorder=3)
    pyplot.legend()
    pyplot.savefig("graph/activity.png")


def main():
    data = load("data/activity.json")
    psjp = PSJP(data)
    plot(psjp)


if __name__ == '__main__':
    main()
