# -*- coding: utf-8 -*- #
import json
from datetime import datetime
from matplotlib import pyplot


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def count_date(data: dict):
    month_count_list = []
    month_name_list = []
    day_week_count_list = [0 for _ in range(7)]
    day_week_name_list = ["日", "月", "火", "水", "木", "金", "土"]
    hour_count_list = [0 for _ in range(24)]
    hour_name_list = [h for h in range(24)]

    for d in data.values():
        created_at = d["registered"]
        time = datetime.fromisoformat(created_at)

        day_week_count_list[time.weekday()] += 1
        hour_count_list[time.hour] += 1

        month_name = time.strftime("%y/%m")
        if month_name in month_name_list:
            month_count_list[month_name_list.index(month_name)] += 1
        else:
            month_name_list.append(month_name)
            month_count_list.append(1)

    dict = {}
    dict["month"] = [month_name_list, month_count_list]
    dict["day"] = [day_week_name_list, day_week_count_list]
    dict["hour"] = [hour_name_list, hour_count_list]
    return dict


def plot_month(data: list):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure(figsize=[14, 7])
    ax = pyplot.axes()
    ax.set_axisbelow(True)
    ax.tick_params(width=0, which="both")
    pyplot.subplot().margins(0.01, 0.05)
    pyplot.grid(axis="y", which="both", c="grey")
    pyplot.xticks(rotation=50)

    pyplot.title("毎月の投稿数（全期間）")
    pyplot.xlabel("年/月")
    pyplot.ylabel("投稿数")

    pyplot.bar(data[0], data[1], color="green")
    fig.savefig("graph/date_month.png")


def plot_day_week(data: list):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure(figsize=[10, 7])
    ax = pyplot.axes()
    ax.set_axisbelow(True)
    ax.tick_params(width=0, which="both")
    pyplot.subplot().margins(0.01, 0.05)
    pyplot.grid(axis="y", which="both", c="grey")

    pyplot.title("各曜日の投稿数（全期間）")
    pyplot.xlabel(" ")
    pyplot.ylabel("投稿数")

    pyplot.bar(data[0], data[1], color="green")
    fig.savefig("graph/date_day_week.png")


def plot_hour(data: list):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'
    fig = pyplot.figure(figsize=[14, 7])
    ax = pyplot.axes()
    ax.set_axisbelow(True)
    ax.tick_params(width=0, which="both")
    pyplot.subplot().margins(0.01, 0.05)
    pyplot.grid(axis="y", which="both", c="grey")

    pyplot.title("各時間の投稿数（全期間）")
    pyplot.xlabel("時")
    pyplot.ylabel("投稿数")

    pyplot.bar(data[0], data[1], color="green")
    fig.savefig("graph/date_hour.png")


def main():
    data_problem = load("data/data.json")
    count = count_date(data_problem)
    plot_month(count["month"])
    plot_day_week(count["day"])
    plot_hour(count["hour"])
    return


if __name__ == '__main__':
    main()
