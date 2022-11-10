# -*- coding: utf-8 -*- #
import json
from datetime import date, datetime
from matplotlib import pyplot
DAY_RANGE = 30


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def count_latest_data(data: dict, days_back: int):
    day_list = [i for i in range(DAY_RANGE)]
    latest_count_list = [0 for _ in range(DAY_RANGE)]

    for d in data.values():
        created_date = datetime.fromisoformat(d["registered"]).date()
        days_delta = (date.today() - created_date).days - days_back

        if 0 <= days_delta and days_delta < DAY_RANGE:
            latest_count_list[days_delta] += 1

    return day_list, latest_count_list


def plot_latest_count(data: dict, last_year: bool):
    image_name = "last-year-puzzle-count.png" if last_year else "latest-puzzle-count.png"
    image_title_prefix = "１年前の" if last_year else ""
    days_back = 365 if last_year else 0

    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure(figsize=[8, 6])
    ax = pyplot.axes()
    ax.set_axisbelow(True)
    ax.tick_params(width=0, which="both")
    ax.invert_xaxis()
    pyplot.subplot().margins(0.01, 0.05)
    pyplot.grid(axis="y", which="both", c="grey")

    pyplot.title("{}直近{}日の投稿数".format(image_title_prefix, DAY_RANGE))
    pyplot.ylabel("投稿数")
    pyplot.xlabel("日前")

    x, y = count_latest_data(data, days_back)
    pyplot.bar(x, y, color="green")
    fig.savefig("graph/" + image_name)


def main():
    data_problem = load("data/data.json")
    plot_latest_count(data_problem, True)
    plot_latest_count(data_problem, False)

    return


if __name__ == '__main__':
    main()
