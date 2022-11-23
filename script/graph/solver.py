import json
from matplotlib import pyplot


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def solvers_answer(data: dict, difficulty: int, stack: bool = False):
    name_list = []
    answer_n_list = []

    def _sort(d):
        if stack:
            return int(d["answer_n"])
        return (int(d["difficulty"][difficulty]["answer_n"]))

    sorted_list = sorted(data.values(), key=_sort)
    for d in sorted_list:
        name_list.append(d["name"])
        if stack:
            # グラフを難易度別に重ねて表示させる
            num = 0
            for i in range(difficulty + 1):
                num += d["difficulty"][i]["answer_n"]
            answer_n_list.append(num)
        else:
            answer_n_list.append(d["difficulty"][difficulty]["answer_n"])

    return name_list, answer_n_list


def plot_solvers_answer(data: dict):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    size = 50
    difficultys = [{"n": 0, "s": "不明", "c": "grey"}, {"n": 1, "s": "らくらく", "c": "b"}, {"n": 2, "s": "おてごろ", "c": "g"}, {"n": 3, "s": "たいへん", "c": "y"}, {"n": 4, "s": "アゼン", "c": "orange"}, {"n": 5, "s": "ハバネロ", "c": "r"}]
    difficultys.reverse()

    def set_plot():
        ax = pyplot.axes()
        ax.set_axisbelow(True)
        ax.tick_params(width=0, which="both")
        pyplot.xlabel("解答数")
        pyplot.ylabel("")
        pyplot.xscale("linear")
        pyplot.yscale("linear")
        pyplot.minorticks_on()
        pyplot.grid(axis="x", which="both", c="grey", alpha=0.5)
        pyplot.subplots_adjust(left=0.28, right=0.95, bottom=0.05, top=0.95)
        pyplot.subplot().margins(0.02, 0.01)

    fig = pyplot.figure(figsize=[8, 12])
    set_plot()
    pyplot.title("ユーザー別解答数（上位" + str(size) + "人）")
    for d in difficultys:
        name, answer = solvers_answer(data, d["n"], stack=True)
        pyplot.barh(name[-1 * size:], answer[-1 * size:], fc=d["c"], label=d["s"])
    pyplot.legend()
    fig.savefig("graph/solvers-answer.png")

    size = 20
    for d in difficultys:
        if d["n"] == 0:
            continue
        fig = pyplot.figure(figsize=[5, 8])
        set_plot()
        pyplot.title(f"ユーザー別{d['s']}解答数（上位{str(size)}人）")
        name, answer = solvers_answer(data, d["n"])
        pyplot.barh(name[-1 * size:], answer[-1 * size:], fc=d["c"], label=d["s"])
        fig.savefig(f"graph/solvers-answer-{d['n']}.png")


def main():
    data = load("data/solvers.json")
    plot_solvers_answer(data)


if __name__ == '__main__':
    main()
