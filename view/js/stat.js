document.getElementById("changeSort").addEventListener("click", changeSort)

function changeSort() {
    const sort = document.getElementById("sort").value
    const order = document.getElementById("order").value
    const sort_sub = (sort === "problem")? "liked": "problem"
    setPage(sort, order, sort_sub)
}

async function setPage(sort, order, sort_sub) {
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
    data["liked_r"] = (data.liked / data.problem).toFixed(2)
    data["count_r"] = (data.problem / data.count).toFixed(2)
    data["variant_r"] = (data.variant / data.problem).toFixed(2)
    for (const key in data[anotherType]) {
        var d = data[anotherType][key]
        d["liked_r"] = (d.liked / d.problem).toFixed(2)
        d["problem_r"] = (d.problem / data.problem).toFixed(2)
        d["variant_r"] = (d.variant / d.problem).toFixed(2)
    }

    setInfo("display", displayStr[anotherType])
    setInfo("displayCount", displayCountStr[anotherType])
    setInfo("displayCountR", displayCountStr[anotherType + "_r"])
    for (const key of ["name", "problem", "liked", "liked_r", "count", "count_r", "variant", "variant_r"]) {
        setInfo(key, data[key])
    }
    var anotherTypeList = Object.values(data[anotherType]);

    const sorts = ["problem", "liked", "liked_r", "variant", "variant_r"]
    sort = sorts.includes(sort)? sort: "problem"
    sort_sub = sorts.includes(sort_sub)? sort_sub: "liked"
    const orderSign = (order == "up")? 1: -1

    anotherTypeList.sort((a,b) => {
        if (a[sort] === b[sort]) {
            return orderSign * (a[sort_sub] - b[sort_sub]);
        }
        return orderSign * (a[sort] - b[sort]);
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
    keys = ["problem", "problem_r", "liked", "liked_r", "variant", "variant_r"]
    var tableElement = document.createElement("table")

    var headerElement = document.createElement("thead")
    var trElement = document.createElement("tr")
    var thElement = document.createElement("th")
    thElement.innerText = displayStr[type]
    trElement.appendChild(thElement)
    for (const key of keys) {
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

        for (const key of keys) {
            var tdElement = document.createElement("td")
            tdElement.innerText = dict[data][key]
            rowElement.appendChild(tdElement)
        }
        bodyElement.appendChild(rowElement)
    }
    tableElement.appendChild(bodyElement)
    document.getElementById("table").innerHTML = tableElement.outerHTML
}