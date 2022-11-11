async function showYesterday() {
    const dataDict = await loadData("yesterday.json")
    setData("day", dataDict["day"])
    setData("total_prob", dataDict["total"]["problem"])
    setData("total_fav", dataDict["total"]["favorite"])
    setData("total_ans", dataDict["total"]["answered"])
    setData("c_fav_prob", dataDict["count"]["favorite"]["problem"])
    setData("c_fav_auth", dataDict["count"]["favorite"]["author"])
    setData("c_ans_prob", dataDict["count"]["answered"]["problem"])
    setData("c_ans_auth", dataDict["count"]["answered"]["author"])
    setData("c_ans_sol", dataDict["count"]["answered"]["solver"])
    setData("top_prob_fav_c", dataDict["top"]["problem"]["favorite"]["count"])
    setData("top_prob_ans_c", dataDict["top"]["problem"]["answered"]["count"])
    setData("top_auth_fav_c", dataDict["top"]["author"]["favorite"]["count"])
    setData("top_auth_ans_c", dataDict["top"]["author"]["answered"]["count"])
    setData("top_sol_ans_c", dataDict["top"]["solver"]["answered"]["count"])

    setDataList("top_prob_fav", dataDict["top"]["problem"]["favorite"]["names"])
    setDataList("top_prob_ans", dataDict["top"]["problem"]["answered"]["names"])
    setDataList("top_auth_fav", dataDict["top"]["author"]["favorite"]["names"], true)
    setDataList("top_auth_ans", dataDict["top"]["author"]["answered"]["names"], true)
    setDataList("top_sol_ans", dataDict["top"]["solver"]["answered"]["names"], true)

    setTweetUrlsYesterday(dataDict)

}; showYesterday()

function setData(elementId, data) {
    var element = document.getElementById(elementId)
    element.innerText = data
}

function setDataList(elementId, list, user=false) {
    var element = document.getElementById(elementId)
    for (const data of list) {
        var dataElement = document.createElement("a")
        dataElement.classList.add("display")
        dataElement.target = "_blank"
        dataElement.innerText = data["name"]
        dataElement.href = data["url"]
        element.appendChild(dataElement)
        if (user) {
            var addElement = document.createElement("span")
            addElement.innerText = " さん"
            element.appendChild(addElement)
        }
        var br = document.createElement("br")
        element.appendChild(br)
    }
}

function setTweetUrlsYesterday(data) {
    const messagePrefix = "＼" + data["day"] + "のパズスク／\n"
    const messageSuffix = "#昨日のpuzsq "
    var messages = {}
    messages["tweetTotal"] = "📖投稿　　 " + data["total"]["problem"] + "問\n"
    messages["tweetTotal"] += "❤ いいね　 " + data["total"]["favorite"] + "問\n"
    messages["tweetTotal"] += "📝解答登録 " + data["total"]["answered"] + "問\n"

    messages["tweetCount"] = "❤ いいねされた問題📖 " + data["count"]["favorite"]["problem"] + "問\n"
    messages["tweetCount"] += "❤ いいねされた作者🧑‍🎨 " + data["count"]["favorite"]["author"] + "人\n"
    messages["tweetCount"] += "📝解答登録された問題📖 " + data["count"]["answered"]["problem"] + "問\n"
    messages["tweetCount"] += "📝解答登録された作者🧑‍🎨 " + data["count"]["answered"]["author"] + "人\n"
    messages["tweetCount"] += "📝解答登録した解き手🙆 " + data["count"]["answered"]["solver"] + "人\n"

    messages["tweetTopProblem"] = "❤ もっともいいねされた問題📖（" + data["top"]["problem"]["favorite"]["count"] + "回）\n"
    for (const name of data["top"]["problem"]["favorite"]["names"]) {
        messages["tweetTopProblem"] += name["name"] + " " + name["url"] + "\n"
    }
    messages["tweetTopProblem"] += "📝もっとも解答登録された問題📖（" + data["top"]["problem"]["answered"]["count"] + "回）\n"
    for (const name of data["top"]["problem"]["answered"]["names"]) {
        messages["tweetTopProblem"] += name["name"] + " " + name["url"] + "\n"
    }

    messages["tweetTopUser"] = "❤ もっともいいねされた作者🧑‍🎨（" + data["top"]["author"]["favorite"]["count"] + "回）\n"
    for (const name of data["top"]["author"]["favorite"]["names"]) {
        messages["tweetTopUser"] += "　" + name["name"] + " さん\n"
    }
    messages["tweetTopUser"] += "📝もっとも解答登録された作者🧑‍🎨（" + data["top"]["author"]["answered"]["count"] + "回）\n"
    for (const name of data["top"]["author"]["answered"]["names"]) {
        messages["tweetTopUser"] += "　" + name["name"] + " さん\n"
    }
    messages["tweetTopUser"] += "📝もっとも解答登録した解き手🙆（" + data["top"]["solver"]["answered"]["count"] + "回）\n"
    for (const name of data["top"]["solver"]["answered"]["names"]) {
        messages["tweetTopUser"] += "　" + name["name"] + " さん\n"
    }

    for (const key in messages) {
        var url = getTweetUrl(messagePrefix + messages[key] + messageSuffix)
        var tweetElement = document.getElementById(key)
        tweetElement.href = url.href
    }
}