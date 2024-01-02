# -*- coding: utf-8 -*- #
import json
from matplotlib import pyplot


class PSJP:
    def __init__(self, data: dict, user: dict, kind: dict):
        self.user = user
        self.kind = kind
        self.author = {}
        self.puzzle = {}

        def _dict(name: str):
            return {"name": name, "count": 0, "difficulty": [{"count": 0} for _ in range(6)]}

        def _add_data(u_id: int, k_id: int, difficulty: int):
            if str(u_id) not in self.author:
                self.author[str(u_id)] = _dict(self.get_user_name(u_id))
            self.author[str(u_id)]["count"] += 1
            self.author[str(u_id)]["difficulty"][difficulty]["count"] += 1
            if str(k_id) not in self.puzzle:
                self.puzzle[str(k_id)] = _dict(self.get_kind_name(k_id))
            self.puzzle[str(k_id)]["count"] += 1
            self.puzzle[str(k_id)]["difficulty"][difficulty]["count"] += 1

        for d in data.values():
            _add_data(d["user"], d["kind"], d["difficulty"])

    def get_user_name(self, u_id: int):
        if not self.user[str(u_id)]:
            return "不明なユーザー"
        return self.user[str(u_id)]["name"]

    def get_kind_name(self, k_id: int):
        if not self.kind[str(k_id)]:
            return "不明なパズル"
        return self.kind[str(k_id)]["name"]

    def get_dict(self, type: str):
        if type == "author":
            return self.author
        return self.puzzle


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def get_list(data_dict: dict, difficulty: int = -1, stack: bool = False):
    def _sort(d):
        if stack:
            return int(d["count"])
        return int(d["difficulty"][difficulty]["count"])

    sorted_list = sorted(data_dict.values(), key=_sort)
    name_list = []
    count_list = []
    for d in sorted_list:
        name_list.append(d["name"])
        if stack:
            # グラフを難易度別に重ねて表示させる
            num = 0
            for i in range(difficulty + 1):
                num += d["difficulty"][i]["count"]
            count_list.append(num)
        else:
            count_list.append(d["difficulty"][difficulty]["count"])
    return name_list, count_list


def plot(psjp: PSJP):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'

    difficultys = [{"n": 1, "s": "らくらく", "c": "b"}, {"n": 2, "s": "おてごろ", "c": "g"}, {"n": 3, "s": "たいへん", "c": "y"}, {"n": 4, "s": "アゼン", "c": "orange"}, {"n": 5, "s": "ハバネロ", "c": "r"}]
    difficultys.reverse()

    def _set(type: str, difficulty: int = -1, difficulty_str: str = ""):
        category = "作者" if type == "author" else "パズル"
        if difficulty < 0:
            pyplot.figure(figsize=[8, 12])
            pyplot.title(f"{category}別問題数（上位{size}）")
            pyplot.subplots_adjust(left=0.28, right=0.95, bottom=0.05, top=0.95)
        else:
            pyplot.figure(figsize=[5, 8])
            pyplot.title(f"{category}別{difficulty_str}問題数（上位{size}）")
            pyplot.subplots_adjust(left=0.4, right=0.95, bottom=0.05, top=0.95)
        pyplot.xlabel("")
        pyplot.ylabel("")
        pyplot.tick_params(width=0, which="both")
        pyplot.minorticks_on()
        pyplot.grid(axis="x", which="both", c="grey", alpha=0.5)
        pyplot.subplot().margins(0.02, 0.01)

    for type in ["puzzle", "author"]:
        size = 50
        _set(type)
        for d in difficultys:
            name, count = get_list(psjp.get_dict(type), d["n"], stack=True)
            pyplot.barh(name[-1 * size:], count[-1 * size:], color=d["c"], label=d["s"], zorder=3)
        pyplot.legend()
        pyplot.savefig(f"graph/problem-by-{type}-difficulty-all.png")

        size = 20
        for d in difficultys:
            _set(type, d["n"], d["s"])
            name, count = get_list(psjp.get_dict(type), d["n"], stack=False)
            pyplot.barh(name[-1 * size:], count[-1 * size:], color=d["c"], zorder=3)
            pyplot.savefig(f"graph/problem-by-{type}-difficulty-{str(d['n'])}.png")


def main():
    data = load("data/data.json")
    user = load("data/user.json")
    kind = load("data/kind.json")
    psjp = PSJP(data, user, kind)
    plot(psjp)


if __name__ == '__main__':
    main()
