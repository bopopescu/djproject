$(function () {
    $('#deploy_app').click(function () {
        deploy()
    })
    $('#check').click(function () {
        command(this.value,this.name)
    })
    $('#start').click(function () {
        command(this.value,this.name)
    })
    $('#restart').click(function () {
        command(this.value,this.name)
    })
    $('#stop').click(function () {
        command(this.value,this.name)
    })
})

function command(type,name) {
    $('button').prop('disabled', true)
    $('#messagecontainer').empty()

    var socket = new WebSocket("ws://" + window.location.host + "/deployjar/control/");
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

        data = ips + '#' + name + '#' + type
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
}

function deploy() {
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
        var appname = document.getElementById("deploy_app").name
        // var script=$("#script option:selected").attr("value")
        // var user=$("#user option:selected").attr("value")
        // var jardir = document.getElementById("jardir").value
        // var port = document.getElementById("port").value

        // data = ips + '#' + jarurl + '#' + script + '#' + user + '#' + jardir + '#' + port
        data = ips + '#' + jarurl + '#' + appname
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
}