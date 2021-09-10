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