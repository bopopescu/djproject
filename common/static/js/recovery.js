$(function () {
    $('#recovery').click(function () {
        var filename = $('#backup option:selected').val()
        // console.log(filename)
        $('button').prop('disabled', true)
        $('#messagecontainer').empty()

        var socket = new WebSocket("ws://" + window.location.host + "/dbmanager/recovery/");
        // console.log(socket);
        socket.onopen = function () {
            socket.send(filename)
        };
        socket.onmessage = function (e) {
            // console.log(e.data)
            if (e.data){
                if(e.data == 'over'){
                    $('button').prop('disabled', false)
                }
                else{
                    $('#messagecontainer').append(e.data+'<br/>');
                }
            }
        };
     })
    $('#dbmanager').addClass('active')
})