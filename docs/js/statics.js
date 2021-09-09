async function setPage() {
    var urlParams = new URLSearchParams(location.search)
    var queryId = null
    var queryType = null
    for (const type of ["puzzle", "author"]) {
        if (urlParams.has(type)) {
            queryId = Number(urlParams.get(type))
            queryType = type
        }
    }

    const data = await loadData(queryType)
    const queryKey = getKey(queryId, data)

    setInfo("name", queryKey);
    setInfo("problem", data[queryKey]["problem"]);
    setInfo("liked", data[queryKey]["liked"]);
    var anotherType = queryType === "puzzle" ? "author": "puzzle"
    var anotherTypeName = queryType === "puzzle" ? "作者": "パズル"
    setInfo("kind", data[queryKey][anotherType])
    setInfo("anotherType", anotherTypeName)

}
setPage();

function getKey(id, data) {
    for (const key in data) {
        if (data[key].id === id) {
            return key
        }
    }
}

function setInfo(key, value) {
    var elements = document.getElementsByClassName(key)
    for(var element of elements) {
        element.innerText = value;
    }
}