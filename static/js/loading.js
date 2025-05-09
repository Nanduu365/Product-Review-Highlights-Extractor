// function load() {
//     console.log("hai")
//     fetch("highlights").then(async (template) => {document.body.innerHTML = await template.text();})
//    }
//    load();

function update() {
    var element = document.getElementById("myprogressBar");   
    let width = 1;
    var identity = setInterval(scene, 10);


    function scene() {
        fetch("/update_value").then(response => response.json())
        .then(data => {
            width = data.value;
            if (width >= 100) {
                clearInterval(identity);
            } else {
                element.style.width = width + '%';}
            })
        }
}