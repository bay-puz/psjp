#! /bin/bash
set -eu

# PSJPのAPI
PSJP_API_BASE="https://puzsq.logicpuzzle.app/api"
PROBLEM_API="/problem/date"
FAVORITE_API="/favorite/date"
ANSWERED_API="/answered/date"
USER_API="/user"
KIND_API="/kind"

# ファイルとスクリプト
DATA_FILE="data/data.json"
USER_FILE="data/user.json"
KIND_FILE="data/kind.json"
UPDATE_FILE="data/update.txt"
CONBINE_SCRIPT="python/combine.py"

# PSJPに最初に投稿された日付
OLDEST_DATE="2019-05-10"

# 前日までの日付でデータを取得する
#TIMESTAMP_NOW="$(date +%s)
TIMESTAMP_NOW="$(date +%s -d"2019-05-12")" #テスト用に短くする

# PSJPのAPIからデータを取得してファイルに保存する
function api(){
    API="${PSJP_API_BASE}${1}"
    FILE="${2}"

    curl -s "${API}" -o "${FILE}"
}

function readable(){
    FILE="${1}"
    jq . -s "${FILE}" > /tmp/jq.json
    mv /tmp/jq.json "${FILE}"
}

# データファイルを初期化
echo "{}" > "${DATA_FILE}"

DATE="${OLDEST_DATE}"
while true; do
    echo "get data at ${DATE}"

    # DATEのデータを取得する
    api "${PROBLEM_API}/${DATE}" /tmp/p.json
    api "${FAVORITE_API}/${DATE}" /tmp/f.json
    api "${ANSWERED_API}/${DATE}" /tmp/a.json

    # 取得したデータを結合する
    /usr/bin/python3 "${CONBINE_SCRIPT}" -b "${DATA_FILE}" -p /tmp/p.json -f /tmp/f.json -a /tmp/a.json
    rm -f /tmp/p.json /tmp/f.json /tmp/a.json

    # 今日以降のデータは使わない
    if [ "$(date +%s -d "${DATE} next day")" -gt "${TIMESTAMP_NOW}" ]; then
        break
    fi
    DATE="$(date +%Y-%m-%d -d "${DATE} next day")"
done

# 取得した日付を記録
date +"%Y年%-m月%-d日" -d "${DATE}" > "${UPDATE_FILE}"

# userとkindのデータを最新に上書き
api "${USER_API}" "${USER_FILE}"
api "${KIND_API}" "${KIND_FILE}"

# JSONを見やすくする
readable "${DATA_FILE}"
readable "${USER_FILE}"
readable "${KIND_FILE}"