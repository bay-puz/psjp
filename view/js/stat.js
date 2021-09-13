document.getElementById("changeSort").addEventListener("click", changeSort)

function changeSort() {
    const sort = document.getElementById("sort").value
    const order = document.getElementById("order").value
    const sort_sub = (sort === "problem")? "liked": "problem"
    setPage(sort, order, sort_sub)
}

async function setPage(sort, order, sort_sub) {
    var urlParams = new URLSearchParams(location.search)
    if (! urlParams.has("author") && ! urlParams.has("puzzle")) {
        location.href = "../"
        return
    }
    var data = {}
    var is_both = false
    var queryType = null; var anotherType = null;
    if (urlParams.has("author") && urlParams.has("puzzle")) {
        is_both = true
        const dataAuthor = await getData(Number(urlParams.get("author")), "author")
        const puzzleName = await getName(Number(urlParams.get("puzzle")), "puzzle")
        data = dataAuthor.puzzle[puzzleName]
        if (! data){
            data = initData()
        }
        data.name = dataAuthor.name + " - " + puzzleName
    } else {
        if (urlParams.has("author")) {
            queryType = "author"
            anotherType = "puzzle"
        } else {
            queryType = "puzzle"
            anotherType = "author"
        }
        const queryId = Number(urlParams.get(queryType))
        data = await getData(queryId, queryType)
    }
    if (!data) {
        location.href = "../"
        return
    }

    setTitle(data.name)
    setPsjpLink(urlParams)
    setTweetUrl()

    data["liked_r"] = (data.liked / data.problem).toFixed(2)
    data["count_r"] = (data.problem / data.count).toFixed(2)
    data["variant_r"] = (data.variant / data.problem).toFixed(2)
    data["difficulty_r"] = [null, 0, 0, 0, 0, 0]
    for (let index = 1; index <= 5; index++) {
        data.difficulty_r[index] = (data.difficulty[index] / data.problem).toFixed(2)
    }

    keys = ["name", "problem", "liked", "liked_r", "count", "count_r", "variant", "variant_r"]
    for (const key of keys) {
        setInfo(key, data[key])
    }
    for (let index = 1; index <= 5; index++) {
        setInfo("difficulty" + index.toString(), data.difficulty[index])
        setInfo("difficulty" + index.toString() + "_r", data.difficulty_r[index])
    }

    if (is_both) {
        hiddenElements("notBoth")
    } else {
        setInfo("display", displayStr[anotherType])
        setInfo("displayCount", displayCountStr[anotherType])
        setInfo("displayCountR", displayCountStr[anotherType + "_r"])

        for (const key in data[anotherType]) {
            var d = data[anotherType][key]
            d["liked_r"] = (d.liked / d.problem).toFixed(2)
            d["problem_r"] = (d.problem / data.problem).toFixed(2)
            d["variant_r"] = (d.variant / d.problem).toFixed(2)
        }

        const sorts = ["problem", "liked", "liked_r", "variant", "variant_r"]
        sort = sorts.includes(sort)? sort: "problem"
        sort_sub = sorts.includes(sort_sub)? sort_sub: "liked"
        const orderSign = (order == "up")? 1: -1

        var anotherTypeList = Object.values(data[anotherType]);
        anotherTypeList.sort((a,b) => {
            if (a[sort] === b[sort]) {
                return orderSign * (a[sort_sub] - b[sort_sub]);
            }
            return orderSign * (a[sort] - b[sort]);
        })
        makeTable(anotherTypeList, anotherType)
    }
}
setPage();

function setInfo(key, value) {
    var elements = document.getElementsByClassName(key)
    for(var element of elements) {
        element.innerText = value;
    }
}

function setTitle(name) {
    var elements = document.getElementsByTagName("title")
    for(var element of elements) {
        element.innerText = element.innerText.replace("Details", name);
    }
}

function setPsjpLink(params) {
    var elements = document.getElementsByClassName("psjpLink")
    for(var element of elements) {
        var url = new URL("https://puzsq.jp/main/index.php")
        url.search = params.toString()
        element.href = url.href
    }
}

function hiddenElements(className) {
    const elements = document.getElementsByClassName(className)
    for(var element of elements) {
        element.classList.add("hidden");
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