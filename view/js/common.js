function setTweetUrl() {
    var url = new URL("https://twitter.com/intent/tweet");
    var params = new URLSearchParams();
    const message = document.getElementsByTagName("title")[0].innerText
    params.append("text", message);
    params.append("url", location.href);
    url.search = params.toString();
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