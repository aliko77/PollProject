"use strict";
$("button#upload-image").click(function () {
    $("#file-upload").click();
});

$("input#file-upload").change(function () {
    const file = this.files[0];
    if (!file) {
        return;
    }
    if (file.size > 2097152) {
        alert("Resim çok büyük!");
        this.value = null;
        return;
    }
    $("#upload-image").addClass("hidden");
    $("#pi-update-form button[type=\"submit\"]").removeClass("hidden");
    let reader = new FileReader();
    reader.onload = function (event) {
        $('#imgPreview').removeClass("hidden").find("img").attr('src', event.target.result);
    }
    reader.readAsDataURL(file);
});

$("#imgReset").click(function () {
    $("input#file-upload").val(null);
    $('#imgPreview').addClass("hidden").find("img").attr('src', null);
    $("#upload-image").removeClass("hidden");
    $("#pi-update-form button[type=\"submit\"]").addClass("hidden");
})