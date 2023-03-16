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

    const messages = getMessages(dataDict)
    setTweetUrlsYesterday(messages)
    setCopyButtons(messages)

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

function getMessages(data) {
    var messages = {}
    messages["title"] = "＼" + data["day"] + "のパズスク／\n"
    messages["tweetHashtag"] = "#昨日のpuzsq "
    messages["copyFooter"] = "もっと見る→" + location.href + "\n"
    messages["data"] = {}

    messages["data"]["Total"] = "📖投稿　　 " + data["total"]["problem"] + "問\n"
    messages["data"]["Total"] += "❤ いいね　 " + data["total"]["favorite"] + "回\n"
    messages["data"]["Total"] += "📝解答登録 " + data["total"]["answered"] + "回\n"

    messages["data"]["Count"] = "❤ いいねされた問題📖 " + data["count"]["favorite"]["problem"] + "問\n"
    messages["data"]["Count"] += "❤ いいねされた作者🧑‍🎨 " + data["count"]["favorite"]["author"] + "人\n"
    messages["data"]["Count"] += "📝解答登録された問題📖 " + data["count"]["answered"]["problem"] + "問\n"
    messages["data"]["Count"] += "📝解答登録された作者🧑‍🎨 " + data["count"]["answered"]["author"] + "人\n"
    messages["data"]["Count"] += "📝解答登録した解き手🙆 " + data["count"]["answered"]["solver"] + "人\n"

    messages["data"]["TopProblem"] = "❤ もっともいいねされた問題📖（" + data["top"]["problem"]["favorite"]["count"] + "回）\n"
    for (const name of data["top"]["problem"]["favorite"]["names"]) {
        messages["data"]["TopProblem"] += name["name"] + " " + name["url"] + "\n"
    }
    messages["data"]["TopProblem"] += "📝もっとも解答登録された問題📖（" + data["top"]["problem"]["answered"]["count"] + "回）\n"
    for (const name of data["top"]["problem"]["answered"]["names"]) {
        messages["data"]["TopProblem"] += name["name"] + " " + name["url"] + "\n"
    }

    messages["data"]["TopUser"] = "❤ もっともいいねされた作者🧑‍🎨（" + data["top"]["author"]["favorite"]["count"] + "回）\n"
    for (const name of data["top"]["author"]["favorite"]["names"]) {
        messages["data"]["TopUser"] += "　" + name["name"] + " さん\n"
    }
    messages["data"]["TopUser"] += "📝もっとも解答登録された作者🧑‍🎨（" + data["top"]["author"]["answered"]["count"] + "回）\n"
    for (const name of data["top"]["author"]["answered"]["names"]) {
        messages["data"]["TopUser"] += "　" + name["name"] + " さん\n"
    }
    messages["data"]["TopUser"] += "📝もっとも解答登録した解き手🙆（" + data["top"]["solver"]["answered"]["count"] + "問）\n"
    for (const name of data["top"]["solver"]["answered"]["names"]) {
        messages["data"]["TopUser"] += "　" + name["name"] + " さん\n"
    }
    return messages
}

function setTweetUrlsYesterday(messages) {
    for (const key in messages["data"]) {
        var url = getTweetUrl(messages["title"] + messages["data"][key] + messages["tweetHashtag"])
        var tweetElement = document.getElementById("tweet" + key)
        tweetElement.href = url.href
    }
}

function setCopyButtons(messages) {
    for (const key in messages["data"]) {
        document.getElementById("copy" + key).addEventListener("click", function(){showCopyMessage(key, messages)})
    }
}

function showCopyMessage(key, messages) {
    const message = messages["title"] + "\n" + messages["data"][key] + "\n" + messages["copyFooter"]
    alert(message)
}