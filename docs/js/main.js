document.getElementById("goPuzzle").addEventListener("click", goPuzzlePage);
document.getElementById("goAuthor").addEventListener("click", goAuthorPage);
document.getElementById("goRanking").addEventListener("click", goRankingPage);
document.getElementById("goGraph").addEventListener("click", goGraphPage);

function goPuzzlePage() {
    const puzzleName = document.getElementById("inputPuzzleName").innerText;
    const puzzleId = getPuzzleId(puzzleName);
    var url = new URL("puzzle.html", location.href);
    url.search = "?puzzle=" + puzzleId;
    location.href = url;
};

function getPuzzleId(name) {
    return 1
};

function goAuthorPage() {
    const authorName = document.getElementById("inputAuthorName").innerText;
    const authorId = getAuthorId(authorName);
    var url = new URL("author.html", location.href);
    url.search = "?author=" + authorId;
    location.href = url;
};

function getAuthorId(name) {
    return 1
};

function goRankingPage() {
    location.href = "./ranking.html";
};

function goGraphPage() {
    location.href = "./graph.html";
};