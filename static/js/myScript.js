var file = document.getElementById("inputFile");
var fileInfo = document.getElementById("fileInfo");
file.addEventListener("change", function () {
    var arr = file.files[0].size / 1024;
    fileInfo.innerText = "\u9009\u4E2D\u7684\u56FE\u7247\u6709 " + arr.toFixed(2) + "KB";
});
