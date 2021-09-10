function loadData(type) {
    const file = "../data/" + type + ".json"
    return new Promise(function (resolve) {
        fetch(file).then(response=>response.json()).then(data=>resolve(data))
    });
}

async function getData(id, type) {
    var data = await loadData(type)
    for (const key in data) {
        if (data[key].id === id) {
            var ret = data[key];
            ret.name = key
            return ret
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
