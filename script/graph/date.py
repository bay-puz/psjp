# -*- coding: utf-8 -*- #
import json
from datetime import datetime
from matplotlib import pyplot


class PSJP:
    def __init__(self, data: dict):
        def _dict(name: str):
            return {"name": name, "count": 0, "difficulty": [{"count": 0} for _ in range(6)]}
        self.hour = {}
        for h in range(24):
            self.hour[str(h)] = _dict(f"{h}時")
        self.day_week = {}
        day_week_name_list = ["日", "月", "火", "水", "木", "金", "土"]
        for d in range(7):
            self.day_week[str(d)] = _dict(day_week_name_list[d])
        self.month = {}

        def _add_data(time: datetime, difficulty: int):
            month_name = time.strftime("%y/%m")
            if month_name not in self.month:
                self.month[month_name] = _dict(month_name)

            self.hour[str(time.hour)]["count"] += 1
            self.day_week[str(time.weekday())]["count"] += 1
            self.month[month_name]["count"] += 1

            self.hour[str(time.hour)]["difficulty"][difficulty]["count"] += 1
            self.day_week[str(time.weekday())]["difficulty"][difficulty]["count"] += 1
            self.month[month_name]["difficulty"][difficulty]["count"] += 1

        for d in data.values():
            time = datetime.fromisoformat(d["registered"])
            difficulty = d["difficulty"]
            _add_data(time, difficulty)

    def get_dict(self, type: str):
        if type == "month":
            return self.month
        if type == "hour":
            return self.hour
        return self.day_week


def load(file: str):
    with open(file, encoding='utf8') as f:
        data_json = f.read()
        return json.loads(data_json)


def get_stacked_list(date_dict: dict, difficulty: int):
    name_list = []
    count_list = []
    for d in date_dict.values():
        name_list.append(d["name"])
        # グラフを難易度別に重ねて表示させる
        num = 0
        for i in range(difficulty + 1):
            num += d["difficulty"][i]["count"]
        count_list.append(num)
    return name_list, count_list


def plot(psjp: PSJP):
    pyplot.rcParams["font.family"] = 'MotoyaLMaru'

    difficultys = [{"n": 1, "s": "らくらく", "c": "b"}, {"n": 2, "s": "おてごろ", "c": "g"}, {"n": 3, "s": "たいへん", "c": "y"}, {"n": 4, "s": "アゼン", "c": "orange"}, {"n": 5, "s": "ハバネロ", "c": "r"}]
    difficultys.reverse()

    def _set(type: str):
        if type == "month":
            pyplot.figure(figsize=[20, 7])
            pyplot.title("毎月の投稿数（全期間）")
            pyplot.xlabel("年/月")
            pyplot.xticks(rotation=50)
        elif type == "hour":
            pyplot.figure(figsize=[14, 7])
            pyplot.title("各時刻の投稿数（全期間）")
            pyplot.xlabel(" ")
        else:
            pyplot.figure(figsize=[10, 7])
            pyplot.title("各曜日の投稿数（全期間）")
            pyplot.xlabel(" ")

        pyplot.ylabel("投稿数")
        pyplot.grid(axis="y", which="both", c="grey")
        pyplot.tick_params(width=0, which="both")
        pyplot.subplot().margins(0.01, 0.05)

    for type in ["month", "day-week", "hour"]:
        _set(type)
        for d in difficultys:
            x, y = get_stacked_list(psjp.get_dict(type), d["n"])
            pyplot.bar(x, y, color=d["c"], label=d["s"], zorder=3)
        pyplot.legend()
        pyplot.savefig(f"graph/date-{type}.png")


def main():
    data_problem = load("data/data.json")
    psjp = PSJP(data_problem)
    plot(psjp)


if __name__ == '__main__':
    main()
