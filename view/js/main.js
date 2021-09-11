document.getElementById("goPuzzle").addEventListener("click", function(){goPage("puzzle");});
document.getElementById("goAuthor").addEventListener("click", function(){goPage("author");});
document.getElementById("goRanking").addEventListener("click", goRanking);
document.getElementById("goGraph").addEventListener("click", goGraph);

async function goPage(type) {
    const elementId = type === "author" ? "inputAuthorName": "inputPuzzleName";
    const name = document.getElementById(elementId).value;
    if (! name) {
        return
    }
    const queryId = await getId(name, type);
    if (queryId === null) {
        showAlert(name, type);
        return
    }
    var url = new URL("view/stat.html", location.href);
    url.search = "?" + type + "=" + queryId;
    location.href = url;
};

function goRanking() {
    location.href = "./view/ranking.html";
};

function goGraph() {
    location.href = "./view/graph.html";
};

function showAlert(name, type) {
    if (type === "author") {
        alert("「" + name + "」という" + "作者は見つかりませんでした。" )
    } else {
        alert("「" + name + "」という" + "パズルは投稿されていません。" )
    }
}