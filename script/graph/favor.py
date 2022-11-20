# -*- coding: utf-8 -*- #
import json
from matplotlib import pyplot


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def get_fav_ans(data: dict, difficulty: int):
    fav_list = []
    ans_list = []
    fav_sum = 0
    ans_sum = 0
    for d in data.values():
        if d["difficulty"] != difficulty:
            continue
        fav_list.append(d["favorite_n"])
        ans_list.append(d["answered_n"])
        fav_sum += d["favorite_n"]
        ans_sum += d["answered_n"]
    return fav_list, ans_list


def plot(data):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure(figsize=[20, 10])
    pyplot.xlabel("解答登録数")
    pyplot.ylabel("いいね数")
    pyplot.title("問題別解答登録数/いいね数")

    difficultys = [{"n": 1, "s": "らくらく", "c": "b", "m": "o"}, {"n": 2, "s": "おてごろ", "c": "g", "m": "s"}, {"n": 3, "s": "たいへん", "c": "y", "m": "D"}, {"n": 4, "s": "アゼン", "c": "orange", "m": "^"}, {"n": 5, "s": "ハバネロ", "c": "r", "m": "*"}]
    for d in difficultys:
        fav, ans = get_fav_ans(data, d["n"])
        pyplot.scatter(ans, fav, s=6, c=d["c"], marker=d["m"], alpha=0.5)
    pyplot.legend([d["s"] for d in difficultys], loc="upper left")
    fig.savefig(f"graph/answered-favorite.png")


def main():
    data = load("data/data.json")
    plot(data)


if __name__ == '__main__':
    main()
