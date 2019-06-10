var password;
var pass2 = $("#new-password2");
var pass1 = $("#new-password1");
var update = $("#update");
var snackbar = $('#snackbar');
pass2.focus(function () {
    password = pass1.val();
});
pass2.keyup(function () {
    var p = pass2.val();
    if ((p === password) && (p.length > 7)) {
        update.prop("disabled", false);
    } else {
        update.prop("disabled", true);
    }
});
pass1.focus(function () {
    password = pass2.val();
});
pass1.keyup(function () {
    var p = pass1.val();
    if ((p === password) && (p.length > 7)) {
        update.prop("disabled", false);
    } else {
        update.prop("disabled", true);
    }
});
$(document).ready(function () {
    update.prop("disabled", "disabled");
});