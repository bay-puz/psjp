# PSJP

[Puzzle Square JP](https://puzsq.logicpuzzle.app/)(PSJP)のデータを取得・公開する。

## [Puzzle Sqaure Stat](https://bay-puz.github.io/psjp/)

GitHub Pagesを使ってページを公開している。
作者別・パズル別の問題数といいね数や、グラフ、ランキングが見られる。

## data/*.json

取得したデータと加工したデータ。
取得日は`data/update.txt`に書かれている。
データはPuzzle Square Statで閲覧できる。

## graph/

作成したグラフを置くディレクトリ。
グラフはPuzzle Square Statで閲覧できる。

## script/get-data.sh

PSJPのAPIを利用して、問題情報、いいね数、解答者数などを取得するスクリプト。
前回の更新以降の差分を取得して`data/data.json`を更新する。

## script/combine.py

APIで取得した1日ごとのデータを`data/data.json`にまとめるスクリプト。
`script/get-data.sh`の中で実行される。

## script/cut-data.py

取得したデータ(`data/data.json`)を、パズル別(`data/puzzle.json`)・作者別(`data/author.json`)に集計するスクリプト。

## script/graph/

グラフを作成するスクリプトを置くディレクトリ。

## .github/workflows/github-action.yml

データとグラフを更新するためのワークフローファイル。
APIで1日ずつのデータを取れるため、1日に1回定期実行する。

## view/*, index.html

Puzzle Square Statの画面を表示するためのスクリプト。
