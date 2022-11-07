document.getElementById("changeSort").addEventListener("click", changeSort)

function changeSort() {
    const sort = document.getElementById("sort").value
    const order = document.getElementById("order").value
    setPage(sort, order)
}

async function setPage(sort, order) {
    var urlParams = new URLSearchParams(location.search)

    // 以前のURLも使えるようにする
    if (urlParams.has("puzzle")) {
        urlParams.set("kind", urlParams.get("puzzle"))
        urlParams.delete("puzzle")
        location.search = urlParams
    }

    if (! urlParams.has("author") && ! urlParams.has("kind")) {
        location.href = "../"
        return
    }
    var data = {}
    var is_both = false
    var anotherType = null;
    if (urlParams.has("author") && urlParams.has("kind")) {
        const kindId = Number(urlParams.get("kind"))
        const kindName = await getNameById(kindId, "kind")
        const authorId = Number(urlParams.get("author"))
        var dataAuthor = await getData(authorId, "author")
        if (! dataAuthor) {
            dataAuthor = initData()
            dataAuthor.name = await getNameById(authorId, "author")
        }
        if (kindId === 0) {
            data = dataAuthor
            anotherType = "kind"
        } else {
            is_both = true
            data = dataAuthor.kind[kindId]
        }
        if (! data){
            data = initData()
        }
        data.name = dataAuthor.name + " - " + kindName
    } else {
        if (urlParams.has("author")) {
            anotherType = "kind"
            const authorId = Number(urlParams.get("author"))
            data = await getData(authorId, "author")
            if (! data) {
                data = initData()
                data.name = await getNameById(authorId, "user")
            }
        } else {
            anotherType = "author"
            const kindId = Number(urlParams.get("kind"))
            data = await getData(kindId, "puzzle")
            if (! data) {
                data = initData()
                data.name = await getNameById(kindId, "kind")
            }
        }
    }
    setTitle(data.name)
    setPsjpLink(urlParams)
    setTweetUrl()

    data["favorite_r"] = (data.favorite_n / data.problem_n).toFixed(2)
    data["answered_r"] = (data.answered_n / data.problem_n).toFixed(2)
    data["count_r"] = (data.problem_n / data.count).toFixed(2)
    data["variant_r"] = (data.variant_n / data.problem_n).toFixed(2)
    for (let index = 1; index <= 5; index++) {
        data.difficulty[index]["problem_r"] = (data.difficulty[index].problem_n / data.problem_n).toFixed(2)
        data.difficulty[index]["favorite_r"] = (data.difficulty[index].favorite_n / data.difficulty[index].problem_n).toFixed(2)
        data.difficulty[index]["answered_r"] = (data.difficulty[index].answered_n / data.difficulty[index].problem_n).toFixed(2)
        data.difficulty[index]["variant_r"] = (data.difficulty[index].variant_n / data.difficulty[index].problem_n).toFixed(2)
    }

    keys = ["name", "problem_n", "favorite_n", "favorite_r", "answered_n", "answered_r", "count", "count_r", "variant_n", "variant_r"]
    for (const key of keys) {
        setInfo(key, data[key])
    }

    var difficultyList = Object.values(data.difficulty).slice(1);
    for (let index = 0; index < 5; index++) {
        difficultyList[index]["difficulty"] = displayDifficultyStr[index+1]
    }
    makeTable("difficultyTable", "difficulty", difficultyList)

    if (is_both) {
        hideElements("notBoth")
    } else {
        setInfo("display", displayStr[anotherType])
        setInfo("displayCount", displayCountStr[anotherType])
        setInfo("displayCountR", displayCountStr[anotherType + "_r"])

        for (const key in data[anotherType]) {
            var d = data[anotherType][key]
            const authorId = (anotherType === "kind")? data.id: d.id
            const kindId = (anotherType === "author")? data.id: d.id
            d[anotherType] = getStatLink(authorId, kindId, d.name).outerHTML
            d["favorite_r"] = (d.favorite_n / d.problem_n).toFixed(2)
            d["answered_r"] = (d.answered_n / d.problem_n).toFixed(2)
            d["problem_r"] = (d.problem_n / data.problem_n).toFixed(2)
            d["variant_r"] = (d.variant_n / d.problem_n).toFixed(2)
        }

        const sorts = ["problem_n", "favorite_n", "favorite_r", "answered_n", "answered_r", "variant_n", "variant_r"]
        sort = sorts.includes(sort)? sort: "problem_n"
        const orderSign = (order == "up")? 1: -1

        var anotherTypeList = Object.values(data[anotherType]);
        anotherTypeList.sort((a,b) => {
            return orderSign * (a[sort] - b[sort]);
        })
        makeTable("anotherTable", anotherType, anotherTypeList)
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
        var url = new URL("https://puzsq.logicpuzzle.app")
        url.search = params.toString()
        element.href = url.href
    }
}

function hideElements(className) {
    const elements = document.getElementsByClassName(className)
    for(var element of elements) {
        element.classList.add("hidden");
    }
}

function makeTable(elementId, header, dataList) {
    keys = ["problem_n", "problem_r", "favorite_n", "favorite_r", "answered_n", "answered_r", "variant_n", "variant_r"]
    var tableElement = document.createElement("table")

    var theadElement = document.createElement("thead")
    var trElement = document.createElement("tr")
    var thElement = document.createElement("th")
    thElement.innerText = displayStr[header]
    trElement.appendChild(thElement)
    for (const key of keys) {
        var cellElement = document.createElement("td")
        cellElement.innerText = displayStr[key]
        trElement.appendChild(cellElement)
    }
    theadElement.append(trElement)
    tableElement.append(theadElement)

    var bodyElement = document.createElement("tbody")
    dataList.forEach(data => {
        var rowElement = document.createElement("tr")
        var thElement = document.createElement("th")
        thElement.innerHTML = data[header]
        rowElement.appendChild(thElement)
        for (const key of keys) {
            var tdElement = document.createElement("td")
            tdElement.innerText = data[key]
            rowElement.appendChild(tdElement)
        }
        bodyElement.appendChild(rowElement)
    });
    tableElement.appendChild(bodyElement)
    document.getElementById(elementId).innerHTML = tableElement.outerHTML
}