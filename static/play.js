$(document).ready(function() {
    $('#play').submit(function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/play',
            data: $('#play').serialize(),
            success: function(response) {
                if (response.error) {
                    $('#Pmessage').html(response.error);
                    console.log(response);
                } else {
                    $('#Pmessage').html(response.success);
                    console.log(response);
                }
            },
            error: function(xhr, status, error) {
                console.log(xhr.responseText);
            }
        });
    });
});
