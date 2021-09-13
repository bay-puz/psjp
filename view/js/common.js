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