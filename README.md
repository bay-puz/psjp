# psjp
[Puzzle Square JP](https://puzsq.jp/main/index.php)のデータを取得・公開する。

## crawl-psjp-data.py
パズル一覧のページから、問題のID、パズル名、いいね数などを取得し、JSON形式で出力する。

Puzzle Square JPの一覧ページには、各問題のIDの他に、作者名、パズル名、いいね数、変種かどうか、作成日時などが載っているため、それらをパースして取得する。

ページ毎にリクエストを投げるため、実行中に新しい問題が投稿されると、同じ問題が２回取得される。
プログラムの中ではチェックをしないので、実行後にIDを見て重複を取り除く必要がある。

### data/data.json
`crawl-psjp-data.py` で取得したデータをJSONの配列にしたもの。
