document.getElementById("goAuthor").addEventListener("click", function(){goStatPage("author");});
document.getElementById("goPuzzle").addEventListener("click", function(){goStatPage("kind");});
document.getElementById("goAuthorPuzzle").addEventListener("click", function(){goStatPage("both");});
document.getElementById("goGraph").addEventListener("click", function(){goPage("graph");});
document.getElementById("goRanking").addEventListener("click", function(){goPage("ranking");});
document.getElementById("goYesterday").addEventListener("click", function(){goPage("yesterday");});

async function goStatPage(type) {
    var url = new URL("view/stat.html", location.href);
    var urlSearchParams = url.searchParams;

    var elementIds = {}
    if (type === "both") {
        elementIds["author"] = "inputAuthorNameWithPuzzle"
        elementIds["kind"] = "inputPuzzleNameWithAuthor"
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

function goPage(page) {
    location.href = "./view/" + page + ".html";
};

function showAlert(name, type) {
    typeDisplay = (type == "author")? "作者": "パズル"
    alert("「" + name + "」という" + typeDisplay + "は見つかりませんでした。" )
}