function show() {
    var params = new URLSearchParams(location.search)
    var rankParams = {"category": "puzzle", "sort": "problem", "subsort": "liked", "order": "down", "number": 20, "condition": null, "criteria": null, "than": "null"}

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
    var data = await loadData(p.category)
    all_name = (p.category === "author")? "全作者": "全パズル"
    delete data[all_name]

    for (const key in data) {
        var d = data[key]
        var contents = {"problem": d.problem, "liked": d.liked, "variant": d.variant, "rank": 1}
        contents[p.category] = key
        contents["count"] = d.count
        contents["count_r"] = d.problem / d.count
        contents["liked_r"] = d.liked / d.problem
        contents["variant_r"] = d.variant / d.problem

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
                return (a[p.category] > b[p.category])
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
        d.liked_r = d.liked_r.toFixed(2)
        d.variant_r = d.variant_r.toFixed(2)
        d[countKey] = d.count
        d[rateKey] = d.count_r.toFixed(2)
    })
    var headers = [p.category, "problem", "liked", "liked_r", countKey, rateKey, "variant", "variant_r"]
    makeRankingTable(list, headers)
}

function makeRankingTable(list, headers) {
    var tableElement = document.createElement("table")

    var headerElement = document.createElement("thead")
    var trElement = document.createElement("tr")
    var thElement = document.createElement("th")
    thElement.innerText = "順位"
    trElement.appendChild(thElement)
    for (const key of headers) {
        var cellElement = document.createElement("td")
        cellElement.innerText = displayStr[key]
        trElement.appendChild(cellElement)
    }
    headerElement.append(trElement)
    tableElement.append(headerElement)

    var bodyElement = document.createElement("tbody")
    for (const data of list) {
        var rowElement = document.createElement("tr")
        var thElement = document.createElement("th")
        thElement.innerText = data.rank
        rowElement.appendChild(thElement)

        for (const key of headers) {
            var tdElement = document.createElement("td")
            tdElement.innerText = data[key]
            rowElement.appendChild(tdElement)
        }
        bodyElement.appendChild(rowElement)
    }
    tableElement.appendChild(bodyElement)
    document.getElementById("ranking").append(tableElement)
}

function setInput(rankParams){
    for (const key in rankParams) {
        document.getElementById(key).value = rankParams[key];
    }
}