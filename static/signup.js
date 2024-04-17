$(document).ready(function() {
    $('#signup-form').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/signup',
            data: $('#signup-form').serialize(),
            success: function(response) {
                if (response.error) {
                    $('#message').html(response.error);
                    console.log(response);
                } else {
                    $('#message').html(response.success);
                    $('#signup-form')[0].reset();
                    console.log(response);
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        });
    });
});
