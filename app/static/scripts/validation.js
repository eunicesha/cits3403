// username validation for signup
function validateNewUsername(username) {
  // if username hasn't been inputted
    if(username.length == 0) {
        displayText("Username is blank", "error");
    } else {
      // validating if username is unique
        fetch(url + "/api/" + username).then(function(response) {
            return(response.json());
        }).then(function(json) {
          // there exists a user with that username already
            if(json["response"] === true) {
                displayText("Username is taken try another one", "error");
            } else {
                clearText();
            }
        });
    }
}
// username validation for login
function validateUsername(username) {
  // no username has been inputted
    if(username.length == 0) {
        displayText("Username is blank", "error");
    } else {
        fetch(url + "/api/" + username).then(function(response) {
            return(response.json());
        }).then(function(json) {
          // there is not an account with that username
            if(json["response"] === false) {
                displayText("Username doesn't exist", "error");
            } else {
                clearText();
            }
        });
    }
}
// validates format and existence of email
function validateEmail(email) {
    if(email.length === 0) {
        displayText("Email can't be blank", "error");
    } else {
        if(isValidEmail(email)) {
            clearText();
        } else {
            displayText("Invalid email address", "error");
        }
    }
}
// checks if email is actually an email
function isValidEmail(email) {
    let re = /.+@.+\..+/g;
    return(re.test(String(email).toLowerCase()));
}

document.getElementById('username').addEventListener('blur', function() {
    validateNewUsername(this.value);
})