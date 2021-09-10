document.getElementById("goPuzzle").addEventListener("click", function(){goPage("puzzle");});
document.getElementById("goAuthor").addEventListener("click", function(){goPage("author");});
document.getElementById("goRanking").addEventListener("click", goRanking);
document.getElementById("goGraph").addEventListener("click", goGraph);

async function goPage(type) {
    const elementId = type === "author" ? "inputAuthorName": "inputPuzzleName";
    const name = document.getElementById(elementId).value;
    const queryId = await getId(name, type);
    var url = new URL("docs/statics.html", location.href);
    url.search = "?" + type + "=" + queryId;
    location.href = url;
};

function goRanking() {
    location.href = "./docs/ranking.html";
};

function goGraph() {
    location.href = "./docs/graph.html";
};