document.getElementById("goAuthor").addEventListener("click", function(){goPage("author");});
document.getElementById("goPuzzle").addEventListener("click", function(){goPage("puzzle");});
document.getElementById("goAuthorPuzzle").addEventListener("click", function(){goPage("both");});
document.getElementById("goRanking").addEventListener("click", goRanking);
document.getElementById("goGraph").addEventListener("click", goGraph);

async function goPage(type) {
    var url = new URL("view/stat.html", location.href);
    var urlSearchParams = url.searchParams;

    var elementIds = {}
    if (type === "both") {
        elementIds["author"] = "inputAuthorNameWithPuzzle"
        elementIds["puzzle"] = "inputPuzzleNameWithAuthor"
    } else {
        elementIds[type] = (type === "author")? "inputAuthorName": "inputPuzzleName"
    }
    for (const key in elementIds) {
        const queryId = await getQueryId(elementIds[key], key)
        if (queryId === null) {
            return
        }
        urlSearchParams.set(key, queryId)
    }
    location.href = url;
};

async function getQueryId(elementId, type) {
    const name = document.getElementById(elementId).value;
    if (name.length === 0) {
        return null
    }
    const dataId = await getIdByName(name, type);
    if (dataId === null) {
        showAlert(name, type);
        return null
    }
    return  dataId
}

function goRanking() {
    location.href = "./view/ranking.html";
};

function goGraph() {
    location.href = "./view/graph.html";
};

function showAlert(name, type) {
    typeDisplay = (type == "author")? "作者": "パズル"
    alert("「" + name + "」という" + typeDisplay + "は見つかりませんでした。" )
}