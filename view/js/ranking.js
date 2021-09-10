function show() {
    var params = new URLSearchParams(location.search)
    if ( ! params.has("category") || ! params.has("sort")) {
        return
    }
    const category = params.get("category")
    const sort = params.get("sort")
    if ( ! category in ["author", "puzzle"] || ! sort in Object.keys(displayStr)) {
        return
    }
    var order = params.has("order")? params.get("order"): "down"
    var number = params.has("number")? params.get("number"): -1
    var sort_sub = params.has("subsort")? params.get("subsort"): category
    makeRanking(category, sort, sort_sub, order, number)
}
show()

async function makeRanking(category, sort, sort_sub, order, number) {
    var data = await loadData(category)
    var list = []
    var countKey = category + "_c"
    var rateKey = category + "_r"
    sort = (sort === "count")? countKey: sort
    for (const key in data) {
        var d = data[key]
        var contents = {"problem": d.problem, "liked": d.liked, "rank": 1}
        contents[category] = key
        contents[countKey] = d.count
        contents[rateKey] = d.problem / d.count
        contents["liked_r"] = d.liked / d.problem
        list.push(contents)
    }
    const orderSign = order == "up"? 1: -1
    list.sort(function (a,b) {
        if (a[sort] === b[sort]) {
            if (sort_sub === category) {
                return (a[sort_sub] > b[sort_sub])
            }
            return orderSign * (a[sort_sub] - b[sort_sub])
        }
        return orderSign * (a[sort] - b[sort])
    })
    var rank = 1
    for (let index = 1; index < list.length; index++) {
        if (list[index][sort] !== list[index-1][sort]) {
            rank = index + 1
            if (rank > number && number > 0) {
                list.splice(index)
                break;
            }
        }
        list[index]["rank"] = rank
    }
    list.forEach(function(d) {
        d["liked_r"] = d["liked_r"].toFixed(2)
        d[rateKey] = d[rateKey].toFixed(2)
    })
    var headers = [category, "problem", "liked", "liked_r", countKey, rateKey]
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