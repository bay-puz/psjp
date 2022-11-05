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

async function getIdByName(name, type) {
    dataType = (type == "puzzle")? "kind": "user"
    var data = await loadData(dataType)
    for (const key in data) {
        if (data[key].name === name) {
            return key;
        }
    }
    return null
}

async function getNameById(id, type) {
    dataType = (type == "puzzle")? "kind": "user"
    var data = await loadData(dataType)
    if ( id in data ) {
        return data[id].name
    }
    return null
}

function getPath() {
    if (location.pathname === "/psjp/" || location.pathname === "/psjp/index.html") {
        return "./data/"
    }
    return "../data/"
}

function initData() {
    var dif = {"problem": 0, "liked": 0, "variant": 0}
    return {"name": "", "problem": 0, "liked":0, "variant":0, "count": 0, "puzzle": {}, "author": {}, "difficulty": [dif, dif, dif, dif, dif, dif]}
}

const displayStr = {"puzzle": "パズル", "author": "作者", "liked": "いいね数", "problem": "問題数", "problem_r": "占有率", "puzzle_c": "人数",  "author_c": "種類", "liked_r": "平均いいね数", "puzzle_r": "人数平均", "author_r": "種類数平均", "variant": "変種", "variant_r": "変種率", "difficulty": "難易度"}
const displayCountStr = {"puzzle": "投稿したパズルの種類", "author": "投稿した作者の人数", "puzzle_r": "１種類当たり問題数", "author_r": "１人当たり問題数"}
const displayDifficultyStr = {1: "らくらく", 2: "おてごろ", 3: "たいへん", 4: "アゼン", 5: "ハバネロ"}