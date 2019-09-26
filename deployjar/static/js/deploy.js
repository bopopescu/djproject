$(function () {
    $('#deploy_app').click(function () {
        $('button').prop('disabled', true)
        $('#messagecontainer').empty()

        var socket = new WebSocket("ws://" + window.location.host + "/deployjar/exec_deployment/");
        console.log(socket);
        socket.onopen = function () {
            var hosts = document.getElementsByName("host");
            var ips;
            for (i=0; i<hosts.length; i++){
                if (hosts[i].checked){
                    if (!ips){
                        ips = hosts[i].value;
                    } else {
                        ips += "," + hosts[i].value;
                    }
                }
            }

            var jarurl = document.getElementById("jarurl").value
            var script=$("#script option:selected").attr("value")
            var user=$("#user option:selected").attr("value")
            var jardir = document.getElementById("jardir").value
            var port = document.getElementById("port").value

            data = ips + '#' + jarurl + '#' + script + '#' + user + '#' + jardir + '#' + port
            console.log(data)
            socket.send(data)
        };
        socket.onmessage = function (e) {
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
})