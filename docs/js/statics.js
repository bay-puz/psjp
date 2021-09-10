async function setPage() {
    var urlParams = new URLSearchParams(location.search)
    var queryId = null; var queryType = null; anotherType = null;
    for (const type of ["puzzle", "author"]) {
        if (urlParams.has(type)) {
            queryId = Number(urlParams.get(type))
            queryType = type
        } else {
            anotherType = type
        }
    }
    if (! queryType || ! anotherType ) {
        location.href = "../"
    }
    const data = await getData(queryId, queryType)
    if (! data) {
        location.href = "../"
    }

    data["count"] = data[anotherType].length
    data["display"] = displayName[anotherType]
    for (const key of ["name", "problem", "liked", "count", "display"]) {
        setInfo(key, data[key])
    }
    makeTable(data[anotherType])
}
setPage();

const displayName = {"puzzle": "パズル", "author": "作者"}

function setInfo(key, value) {
    var elements = document.getElementsByClassName(key)
    for(var element of elements) {
        element.innerText = value;
    }
}

function makeTable(list) {
    var tableElement = document.createElement("table")
    for (const contents of list) {
        var rowElement = tableElement.insertRow(-1);
        rowElement.innerText = contents
    }
    document.getElementById("table").append(tableElement)
}