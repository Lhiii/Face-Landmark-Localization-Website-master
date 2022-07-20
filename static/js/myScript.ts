const file = document.getElementById("inputFile") as HTMLInputElement;
let fileInfo = document.getElementById("fileInfo");
file.addEventListener("change", function () {
    let arr = file.files[0].size / 1024

    fileInfo.innerText = `选中的图片有 ${arr.toFixed(2)}KB`
})