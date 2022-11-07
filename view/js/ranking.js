function show() {
    var params = new URLSearchParams(location.search)

    // 以前のURLも使えるようにする
    if (params.get("category") === "puzzle") {
        oldParam = true
        params.set("category", "kind")
        location.search = params
    }

    var rankParams = {"category": "kind", "sort": "problem_n", "subsort": "favorite_n", "order": "down", "number": 20, "condition": null, "criteria": null, "than": "null"}
    for (const key in rankParams) {
        if (params.has(key)) {
            if (key === "number" || key === "criteria") {
                rankParams[key] = Number(params.get(key))
            } else {
                rankParams[key] = params.get(key)
            }
        }
    }
    makeRanking(rankParams)
    setInput(rankParams)
}
show()

async function makeRanking(p) {
    var list = []
    var data = await getAllData(p.category)
    delete data[0]

    for (const key in data) {
        var d = data[key]
        var contents = {"name": key, "problem_n": d.problem_n, "favorite_n": d.favorite_n, "answered_n": d.answered_n, "variant_n": d.variant_n, "rank": 1}
        const authorId = (p.category === "author")? d.id: 0
        const kindId = (p.category === "kind")? d.id: 0
        contents[p.category] = getStatLink(authorId, kindId, d.name).outerHTML
        contents["count"] = d.count
        contents["count_r"] = d.problem_n / d.count
        contents["favorite_r"] = d.favorite_n / d.problem_n
        contents["answered_r"] = d.answered_n / d.problem_n
        contents["variant_r"] = d.variant_n / d.problem_n

        if (p.condition && p.than) {
            if (p.than === "large" && !(p.criteria < contents[p.condition])) {
                continue
            }
            if (p.than === "small" &&  !(p.criteria > contents[p.condition])) {
                continue
            }
        }
        list.push(contents)
    }

    const orderSign = (p.order == "up")? 1: -1
    list.sort(function (a,b) {
        if (a[p.sort] === b[p.sort]) {
            if (p.subsort === "name") {
                return (a[p.subsort] > b[p.subsort])
            }
            return orderSign * (a[p.subsort] - b[p.subsort])
        }
        return orderSign * (a[p.sort] - b[p.sort])
    })
    var rank = 1

    for (let index = 1; index < list.length; index++) {
        if (list[index][p.sort] !== list[index-1][p.sort]) {
            rank = index + 1
            if (rank > p.number && p.number > 0) {
                list.splice(index)
                break;
            }
        }
        list[index]["rank"] = rank
    }
    const countKey = p.category + "_c"
    const rateKey = p.category + "_r"
    list.forEach(function(d) {
        d.favorite_r = d.favorite_r.toFixed(2)
        d.answered_r = d.answered_r.toFixed(2)
        d.variant_r = d.variant_r.toFixed(2)
        d[countKey] = d.count
        d[rateKey] = d.count_r.toFixed(2)
    })
    var headers = ["problem_n", "favorite_n", "favorite_r", "answered_n", "answered_r", countKey, rateKey, "variant_n", "variant_r"]
    makeRankingTable(p.category, headers, list)
}

function makeRankingTable(header, keys, dataList) {
    var tableElement = document.createElement("table")

    var headerElement = document.createElement("thead")
    var trElement = document.createElement("tr")
    var thElement = document.createElement("th")
    thElement.innerText = "順位"
    trElement.appendChild(thElement)
    var thElement = document.createElement("th")
    thElement.innerText = displayStr[header]
    trElement.appendChild(thElement)
    for (const key of keys) {
        var cellElement = document.createElement("td")
        cellElement.innerText = displayStr[key]
        trElement.appendChild(cellElement)
    }
    headerElement.append(trElement)
    tableElement.append(headerElement)

    var bodyElement = document.createElement("tbody")
    dataList.forEach(data => {
        var rowElement = document.createElement("tr")
        var thElement = document.createElement("th")
        thElement.innerText = data.rank
        rowElement.appendChild(thElement)
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
    document.getElementById("ranking").append(tableElement)
}

function setInput(rankParams){
    for (const key in rankParams) {
        document.getElementById(key).value = rankParams[key];
    }
}