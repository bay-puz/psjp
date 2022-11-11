function setTweetUrl() {
    const message = document.getElementsByTagName("title")[0].innerText
    var url = getTweetUrl(message)
    var elements = document.getElementsByClassName("tweetLink")
    for(var element of elements) {
        element.href = url.href
    }
}
setTweetUrl()

function getStatLink(author_id, kind_id, text) {
    var urlStr = "./stat.html?"
    var params = new URLSearchParams()
    if (author_id) {
        params.set("author", author_id)
    }
    if (kind_id) {
        params.set("kind", kind_id)
    }
    urlStr += params.toString()

    var aElement = document.createElement("a")
    aElement.href = urlStr
    aElement.innerText = text
    aElement.target = "_blank"
    aElement.classList.add("statLink")
    return aElement
}

function getTweetUrl(message) {
    var url = new URL("https://twitter.com/intent/tweet");
    var params = new URLSearchParams();
    params.append("text", message);
    params.append("url", location.href);
    url.search = params.toString();
    return url
}