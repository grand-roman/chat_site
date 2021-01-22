
$('document').ready(function() {
    $("#message_input_form").submit(function(event) {
        /* stop form from submitting normally */

        event.preventDefault();

        var $form = $(this),
        url = $form.attr('action');

        serialized_form = $form.serialize();

        request = $.ajax({
            type: "POST",
            url: url,
            data: serialized_form,
            success: function(data) {
                // $("#error_info").text('success');
            },
            error: function(data) {
                $("#error_info").text('error: ' + data.statusText);
            }
        });

        request.always(function () {
            $form.prop("disabled", false);
            $form[0].querySelector("#message_input").value = "";
        });

        return false;
    });
});

function search_message(text) {
     $.ajax({
            type: "GET",
            url: "/search",
            data: { text: text} ,
            success: function(data, el) {
                document.getElementById('search_result').innerHTML = data;
            },
            error: function() {
                console.log('Fail')
            }
        });
}

