
export function update_messages() {
    var scroller = document.getElementById('scroller')

     if (scroller == null || scroller.clientHeight + scroller.scrollTop >= scroller.scrollHeight - 1) {
         $.ajax({
                type: "GET",
                url: "/chat_box",
                success: function(data, el) {
                    document.getElementById('message_list').innerHTML = data;
                    var scroller = document.getElementById('scroller');
                    scroller.scrollTop = scroller.scrollHeight - scroller.clientHeight;
                },
                error: function() {
                    console.log('Fail')
                }
            });
     }
}


const interval = setInterval(update_messages, 200);


export function update_flooders() {
 $.ajax({
        type: "GET",
        url: "/flooders",
        success: function(data, el) {
            document.getElementById('flooders_list').innerHTML = data;
        },
        error: function() {
            console.log('Fail')
        }
    });
}


const flooders_interval = setInterval(update_flooders, 200);
