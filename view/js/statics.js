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

    setInfo("display", displayStr[anotherType])
    setInfo("displayCount", displayCountStr[anotherType])
    for (const key of ["name", "problem", "liked", "count"]) {
        setInfo(key, data[key])
    }
    var anotherTypeList = Object.values(data[anotherType]);
    anotherTypeList.sort((a,b) => {
        if (a["problem"] === b["problem"]) {
            return (b["liked"] - a["liked"]);
        }
        return (b["problem"] - a["problem"]);
    })
    makeTable(anotherTypeList, anotherType)
}
setPage();


function setInfo(key, value) {
    var elements = document.getElementsByClassName(key)
    for(var element of elements) {
        element.innerText = value;
    }
}

function makeTable(dict, type) {
    var tableElement = document.createElement("table")

    var headerElement = document.createElement("thead")
    var trElement = document.createElement("tr")
    var thElement = document.createElement("th")
    thElement.innerText = displayStr[type]
    trElement.appendChild(thElement)
    for (const key of ["problem", "liked"]) {
        var cellElement = document.createElement("td")
        cellElement.innerText = displayStr[key]
        trElement.appendChild(cellElement)
    }
    headerElement.append(trElement)
    tableElement.append(headerElement)

    var bodyElement = document.createElement("tbody")
    for (const data in dict) {
        var rowElement = document.createElement("tr")
        var thElement = document.createElement("th")
        thElement.innerText = dict[data]["name"]
        rowElement.appendChild(thElement)

        for (const key of ["problem", "liked"]) {
            var tdElement = document.createElement("td")
            tdElement.innerText = dict[data][key]
            rowElement.appendChild(tdElement)
        }
        bodyElement.appendChild(rowElement)
    }
    tableElement.appendChild(bodyElement)
    document.getElementById("table").append(tableElement)
}