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
CONBINE_SCRIPT="script/combine.py"

# PSJPのAPIからデータを取得してファイルに保存する
function api(){
    API="${PSJP_API_BASE}${1}"
    FILE="${2}"

    curl -s "${API}" -o "${FILE}"
}

# JSONを整形する
function readable(){
    FILE="${1}"
    jq . "${FILE}" > /tmp/jq.json
    mv /tmp/jq.json "${FILE}"
}

# 日本時間で行う
export TZ="Asia/Tokyo"

# 元データファイルがなければ作り、データは最古の日付から取る
if [ ! -f "${DATA_FILE}" ]; then
    echo "{}" > "${DATA_FILE}"
    DATE="2019-05-09"
else
    # UPDATE_FILEに書かれた日付を読みこむ
    if [ ! -f "${UPDATE_FILE}" ]; then
        echo "${UPDATE_FILE} doesn't exit" >&2
        exit 2
    fi
    DATE="$(date +%Y-%m-%d -d "$(cat "${UPDATE_FILE}")")"
fi

TIMESTAMP_TODAY="$(date +%s -d"today 00:00:00")"

# userとkindのデータを最新のものにする
echo "get user and kind"
api "${USER_API}" "${USER_FILE}"
api "${KIND_API}" "${KIND_FILE}"

while true; do
    # 今日以降のデータは使わない
    if [ "$(date +%s -d "${DATE} next day")" -ge "${TIMESTAMP_TODAY}" ]; then
        break
    fi
    # 前回の更新の次の日付から始める
    DATE="$(date +%Y-%m-%d -d "${DATE} next day")"

    # DATEのデータを取得する
    echo "get data at ${DATE}"
    api "${PROBLEM_API}/${DATE}" /tmp/p.json
    api "${FAVORITE_API}/${DATE}" /tmp/f.json
    api "${ANSWERED_API}/${DATE}" /tmp/a.json

    # 取得したデータを結合する
    echo "combine data at ${DATE}"
    /usr/bin/python3 "${CONBINE_SCRIPT}" -b "${DATA_FILE}" -p /tmp/p.json -f /tmp/f.json -a /tmp/a.json
    rm -f /tmp/p.json /tmp/f.json /tmp/a.json
done

# 取得した日付を記録
echo "${DATE}" > "${UPDATE_FILE}"

# JSONを見やすくする
readable "${DATA_FILE}"
readable "${USER_FILE}"
readable "${KIND_FILE}"
