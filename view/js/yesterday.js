async function showYesterday() {
    const dataDict = await loadData("yesterday.json")
    setData("day", dataDict["day"])
    setData("total_prob", dataDict["total"]["problem"])
    setData("total_fav", dataDict["total"]["favorite"])
    setData("total_ans", dataDict["total"]["answered"])
    setData("c_fav_prob", dataDict["count"]["favorite"]["problem"])
    setData("c_fav_auth", dataDict["count"]["favorite"]["author"])
    setData("c_ans_prob", dataDict["count"]["answered"]["problem"])
    setData("c_ans_auth", dataDict["count"]["answered"]["author"])
    setData("c_ans_sol", dataDict["count"]["answered"]["solver"])
    setData("top_prob_fav_c", dataDict["top"]["problem"]["favorite"]["count"])
    setData("top_prob_ans_c", dataDict["top"]["problem"]["answered"]["count"])
    setData("top_auth_fav_c", dataDict["top"]["author"]["favorite"]["count"])
    setData("top_auth_ans_c", dataDict["top"]["author"]["answered"]["count"])
    setData("top_sol_ans_c", dataDict["top"]["solver"]["answered"]["count"])

    setDataList("top_prob_fav", dataDict["top"]["problem"]["favorite"]["names"])
    setDataList("top_prob_ans", dataDict["top"]["problem"]["answered"]["names"])
    setDataList("top_auth_fav", dataDict["top"]["author"]["favorite"]["names"], true)
    setDataList("top_auth_ans", dataDict["top"]["author"]["answered"]["names"], true)
    setDataList("top_sol_ans", dataDict["top"]["solver"]["answered"]["names"], true)


}; showYesterday()

function setData(elementId, data) {
    var element = document.getElementById(elementId)
    element.innerText = data
}

function setDataList(elementId, list, user=false) {
    var element = document.getElementById(elementId)
    for (const data of list) {
        var dataElement = document.createElement("a")
        dataElement.classList.add("display")
        dataElement.target = "_blank"
        dataElement.innerText = data["name"]
        dataElement.href = data["url"]
        element.appendChild(dataElement)
        if (user) {
            var addElement = document.createElement("span")
            addElement.innerText = " さん"
            element.appendChild(addElement)
        }
        var br = document.createElement("br")
        element.appendChild(br)
    }
}