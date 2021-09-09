function loadData(type) {
    const file = "../data/" + type + ".json"
    return new Promise(function (resolve) {
        fetch(file).then(response=>response.json()).then(data=>resolve(data))
    });
}
