$(document).ready(function() {
    // validate username using validation.js
    $("#username").blur(function() {
        validateNewUsername(this.value);
    });
    // validate email using validation.js
    $("#email").blur(function() {
        validateEmail(this.value);
    });
    // validates that password isn't blank
    $("#password").blur(function() {
        let $password2 = $("#password2").val();

        if(this.value.length === 0) {
            displayText("Enter password", "error");
        }
    });
    // validates that confirm password is the same and isn't blank
    $("#password2").blur(function() {
        let $password = $("#password").val();
        if(this.value.length === 0) {
            displayText("Confirm password", "error");
        }
        else if(this.value != $password) {
            displayText("Passwords don't match", "error");
        } else {
            clearText();
        }
    });
});
