# -*- coding: utf-8 -*- #
import argparse
import json

def load(file: str) -> dict:
     with open(file, encoding='utf8') as f:
        return json.load(f)

def write(data: dict, file: str) -> None:
     with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f)

def main():
    parser = argparse.ArgumentParser(description='日付を指定したデータを結合する')
    parser.add_argument("-b", metavar="base", type=str, default="data/data.json", help="元データ")
    parser.add_argument("-p", metavar="problem", type=str, help="追加のproblem")
    parser.add_argument("-f", metavar="favorite", type=str, help="追加のfavorite")
    parser.add_argument("-a", metavar="answered", type=str, help="追加のanswered")
    args = parser.parse_args()

    base = load(args.b)
    problems = load(args.p)
    favorites = load(args.f)
    answered = load(args.a)
    
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

    write(base, args.b)


if __name__ == '__main__':
    main()
