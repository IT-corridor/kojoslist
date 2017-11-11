/* *
 * Upload File
 */
document.getElementById("uploadBtn").onchange = function () {
    document.getElementById("uploadFile").value = this.value;
};

/* *
 * Date Time Function
 */
$(function () {
    $('.my-datetimepicker').datetimepicker();
});
