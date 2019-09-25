$(function () {
    $('#deploy_app').click(function () {
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

            data = ips + '#' + jarurl + '#' + script + '#' + user
            // console.log(data)
            socket.send(data)
        };
        socket.onmessage = function (e) {
            // console.log('message: ' + e.data);
            if (e.data){
                $('#messagecontainer').append(e.data+'<br/>');
            }
        };
    })
})