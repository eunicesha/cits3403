$(document).ready(function() {
    $('#signup-form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/signup',
            data: $('#signup-form').serialize(),
            success: function(response) {
                if (response.error) {
                    $('#Smessage').html(response.error);
                    console.log(response);
                } else {
                    $('#Smessage').html(response.success);
                    window.location.href = '/forum';
                    $('#signup-form')[0].reset();
                    console.log(response);
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        });
    });
    $('#login-form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/login',
            data: $('#login-form').serialize(),
            success: function(response) {
                if (response.error) {
                    $('#Lmessage').html(response.error);
                    console.log(response);
                } else if (response.success) {  
                    $('#Lmessage').html(response.success);
                    window.location.href = '/forum';
                    console.log(response);
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        });
    });
});
