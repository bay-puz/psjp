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

// 高速化のためファイルのfetchをしない
function getDataById(id, type, authorData, puzzleData) {
    if ( type === "kind"  || type === "puzzle" ){
        data = puzzleData
    } else if ( type === "user" || type === "author" ){
        data = authorData
    }
    for (const key in data) {
        if (data[key].id === id) {
            return data[key]
        }
    }
    return null
}

async function getNameData(type) {
    if ( type === "kind"  || type === "puzzle" ){
        file = "kind.json"
    } else if ( type === "user" || type === "author" ){
        file = "user.json"
    }
    return await loadData(file)
}

async function getIdByName(name, type) {
    data = await getNameData(type)
    for (const key in data) {
        if (data[key].name === name) {
            return key
        }
    }
    return null
}

// 高速化のためファイルのfetchをしない
function getNameById(id, type, userData, kindData) {
    if ( type === "kind"  || type === "puzzle" ){
        data = kindData
    } else if ( type === "user" || type === "author" ){
        data = userData
    }
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
    var dif = []
    for(var index=0; index<5; index++){
        dif.push({"number": index + 1, "problem_n": 0, "favorite_n": 0, "answered_n": 0, "variant_n": 0})
    }
    return {"name": "", "problem_n": 0, "favorite_n":0, "answered_n": 0, "variant_n":0, "count": 0, "puzzle": {}, "author": {}, "difficulty": dif}
}

const displayStr = {"kind": "パズル", "author": "作者", "favorite_n": "いいね数", "answered_n": "解答者数", "problem_n": "問題数", "problem_r": "占有率", "kind_c": "作者数",  "author_c": "パズル数", "favorite_r": "平均いいね数", "answered_r": "平均解答者数", "kind_r": "作者平均", "author_r": "パズル平均", "variant_n": "変種数", "variant_r": "変種率", "difficulty": "難易度"}
const displayCountStr = {"kind": "投稿したパズルの種類", "author": "投稿した作者の人数", "kind_r": "１種類当たり問題数", "author_r": "１人当たり問題数"}
const displayDifficultyStr = {1: "らくらく", 2: "おてごろ", 3: "たいへん", 4: "アゼン", 5: "ハバネロ"}