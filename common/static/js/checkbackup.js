$(function () {
    $('#btn_check').click(function () {
        $('button').prop('disabled', true)
        $('#messagecontainer').empty()

        var socket = new WebSocket("ws://" + window.location.host + "/common/execcheck/");

        socket.onopen = function () {
            socket.send('onopen')
        };

        socket.onmessage = function (e) {
            console.log(e.data)
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

    $('#checkbackup').addClass('active')
})