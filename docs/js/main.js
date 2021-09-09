document.getElementById("goPuzzle").addEventListener("click", function(){goPage("puzzle");});
document.getElementById("goAuthor").addEventListener("click", function(){goPage("author");});
document.getElementById("goRanking").addEventListener("click", goRanking);
document.getElementById("goGraph").addEventListener("click", goGraph);

function goPage(type) {
    const elementId = type === "author" ? "inputAuthorName": "inputPuzzleName";
    const name = document.getElementById(elementId).value;
    const queryId = getId(name, type);
    var url = new URL("statics.html", location.href);
    url.search = "?" + type + "=" + queryId;
    location.href = url;
};

function getId(name, type) {
    return name
};

function goRanking() {
    location.href = "./ranking.html";
};

function goGraph() {
    location.href = "./graph.html";
};