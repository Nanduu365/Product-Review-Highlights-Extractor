// function load() {
//     console.log("hai")
//     fetch("highlights").then(async (template) => {document.body.innerHTML = await template.text();})
//    }
//    load();

function update() {
    var element = document.getElementById("myprogressBar");   
    var container = document.getElementById("progress_container");   
    let width = 1;
    var identity = setInterval(scene, 1500);
    // element.style.display = 'block';
    container.style.display = 'block';


    function scene() {
        fetch("/update_value").then(response => response.json())
        .then(data => {
            width = data.value;
            if (width >= 100) {
                clearInterval(identity);
                // Redirect to another page
                window.location.href = '/highlights';
            } 
            else {
                element.style.width = width + '%';
                element.innerHTML = width + '%';}
            })
        }
}

if (window.location.pathname === '/loading') {
    update();
}