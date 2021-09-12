async function setUpdatedTime() {
    var elements = document.getElementsByClassName("updatedTime")
    var date = await loadUpdatedTime();
    for (var element of elements) {
        element.innerText = date
    }
} setUpdatedTime();

function loadUpdatedTime() {
    const file = getPath() + "update.txt"
    return new Promise(function (resolve) {
        fetch(file).then(response=>response.text()).then(data=>resolve(data))
    });
}

function loadData(type) {
    const file = getPath() + type + ".json"
    return new Promise(function (resolve) {
        fetch(file).then(response=>response.json()).then(data=>resolve(data))
    });
}

async function getData(id, type) {
    var data = await loadData(type)
    for (const key in data) {
        if (data[key].id === id) {
            return data[key];
        }
    }
    return null
}

async function getId(name, type) {
    var data = await loadData(type)
    if ( name in data ) {
        return data[name].id
    }
    return null
}

function getPath() {
    if (location.pathname === "/psjp/" || location.pathname === "/psjp/index.html") {
        return "./data/"
    }
    return "../data/"
}

const displayStr = {"puzzle": "パズル", "author": "作者", "liked": "いいね数", "problem": "問題数", "problem_r": "占有率", "puzzle_c": "人数",  "author_c": "種類", "liked_r": "平均いいね数", "puzzle_r": "人数平均", "author_r": "種類数平均", "variant": "変種", "variant_r": "変種率"}
const displayCountStr = {"puzzle": "投稿したパズルの種類", "author": "投稿した作者の人数", "puzzle_r": "１種類当たり問題数", "author_r": "１人当たり問題数"}