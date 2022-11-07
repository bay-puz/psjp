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

function loadData(file) {
    file = getPath() + file
    return new Promise(function (resolve) {
        fetch(file).then(response=>response.json()).then(data=>resolve(data))
    });
}

async function getAllData(type) {
    if ( type === "kind"  || type === "puzzle" ){
        file = "puzzle.json"
    } else if ( type === "user" || type === "author" ){
        file = "author.json"
    }
    return await loadData(file)
}

async function getData(id, type) {
    if ( type === "kind"  || type === "puzzle" ){
        file = "puzzle.json"
    } else if ( type === "user" || type === "author" ){
        file = "author.json"
    }
    var data = await loadData(file)
    for (const key in data) {
        if (data[key].id === id) {
            return data[key];
        }
    }
    return null
}

async function getIdByName(name, type) {
    if ( type === "kind"  || type === "puzzle" ){
        file = "kind.json"
    } else if ( type === "user" || type === "author" ){
        file = "user.json"
    }
    var data = await loadData(file)
    for (const key in data) {
        if (data[key].name === name) {
            return key;
        }
    }
    return null
}

async function getNameById(id, type) {
    if ( type === "kind"  || type === "puzzle" ){
        file = "kind.json"
    } else if ( type === "user" || type === "author" ){
        file = "user.json"
    }
    var data = await loadData(file)
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
    var dif = {"problem_n": 0, "favorite_n": 0, "answered_n": 0, "variant_n": 0}
    return {"name": "", "problem_n": 0, "favorite_n":0, "answered_n": 0, "variant_n":0, "count": 0, "puzzle": {}, "author": {}, "difficulty": [dif, dif, dif, dif, dif, dif]}
}

const displayStr = {"kind": "パズル", "author": "作者", "favorite_n": "いいね数", "answered_n": "解答者数", "problem_n": "問題数", "problem_r": "占有率", "kind_c": "人数",  "author_c": "種類", "favorite_r": "平均いいね数", "answered_r": "平均解答者数", "kind_r": "人数平均", "author_r": "種類数平均", "variant_n": "変種数", "variant_r": "変種率", "difficulty": "難易度"}
const displayCountStr = {"kind": "投稿したパズルの種類", "author": "投稿した作者の人数", "kind_r": "１種類当たり問題数", "author_r": "１人当たり問題数"}
const displayDifficultyStr = {1: "らくらく", 2: "おてごろ", 3: "たいへん", 4: "アゼン", 5: "ハバネロ"}