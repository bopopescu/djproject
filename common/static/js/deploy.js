$(function () {
    $('#deploy_app').click(function () {
        deploy()
    })
    $('#check').click(function () {
        command(this.value)
    })
    $('#start').click(function () {
        command(this.value)
    })
    $('#restart').click(function () {
        command(this.value)
    })
    $('#stop').click(function () {
        command(this.value)
    })
})

function command(type) {
    $('button').prop('disabled', true)
    $('#messagecontainer').empty()

    var socket = new WebSocket("ws://" + window.location.host + "/deployjar/control/");
    console.log(socket);
    socket.onopen = function () {
        var chks = document.getElementsByName("instance")
        ints =[]
        for (i=0; i<chks.length; i++){
            if (chks[i].checked){
                id = chks[i].value;
                ints.push(id)
            }
        }

        data = {'ints':ints,'type':type}
        console.log(data)
        socket.send(JSON.stringify(data))
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