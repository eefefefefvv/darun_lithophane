function upload() {
    let fileInput = document.getElementById('photo');
    if(fileInput.files.length === 0) {
        alert("Выберите файл!");
        return;
    }
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        let url = URL.createObjectURL(blob);
        let link = document.createElement("a");
        link.href = url;
        link.download = "result.stl";
        link.innerText = "Скачать STL";
        document.getElementById("result").innerHTML = '';
        document.getElementById("result").appendChild(link);
    })
    .catch(err => console.error(err));
}
