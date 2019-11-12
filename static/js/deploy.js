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

    $("#all_ckb").click(function(){
        if ($('input[name="SelectAll"]').is(':checked')) {
            $('input[name="instance"]').prop('checked', true);//全选
　　　　}
　　　　else {
　　　　    $('input[name="instance"]').prop('checked', false);//取消全选
　　　　}
    })

    $('#deploy').addClass('active')
})

function ch_all_chk() {
    chbs = document.getElementsByName('instance').length
    chks = $("input[name='instance']:checked").length
    if(chbs == chks){
        $('#all_ckb').prop('checked', true)
    }
    else{
        $('#all_ckb').prop('checked', false)
    }
}

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
        var chks = document.getElementsByName("instance")
        ints =[]
        for (i=0; i<chks.length; i++){
            if (chks[i].checked){
                id = chks[i].value;
                ints.push(id)
            }
        }
        var jarurl = document.getElementById("jarurl").value
        data = {'ints':ints,'jarurl':jarurl}
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