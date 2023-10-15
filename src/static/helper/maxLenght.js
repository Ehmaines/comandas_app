maxLengthFields.forEach(function (field) {
    field.addEventListener("input", function () {
        if (this.value.length > parseInt(this.getAttribute("maxlength"))) {
            this.value = this.value.slice(
                0,
                parseInt(this.getAttribute("maxlength"))
            );
        }
    });
});
