$(document).ready(function() {
    // validates username using validation.js
    $("#username").blur(function() {
        validateUsername(this.value);
    });
    // checks if a password was entered
    $("#password").blur(function() {
        if(this.value.length === 0) {
            displayText("Enter password", "error");
        } else {
            clearText();
        }
    });
});
