$(function () {
    $('#a_task').addClass('active')
    $('#a_exec_task').addClass('active')
    $('#ul_task').addClass('in')

    $("#exec_tasks").click(function () {
        $('#btn_show_modal').click()
        var hosts = document.getElementsByName("host")
        ips =[]
        for (i=0; i<hosts.length; i++){
            if (hosts[i].checked){
                ip = hosts[i].value;
                ips.push(ip)
            }
        }

        var tasks = document.getElementsByName("task")
        tks =[]
        for (i=0; i<tasks.length; i++){
            if (tasks[i].checked){
                t_value = tasks[i].value;
                tks.push(t_value)
            }
        }

        data = {'ips':ips,'tks':tks}

        $('button').prop('disabled', true)
        $('#msgc').empty()

        var socket = new WebSocket("ws://" + window.location.host + "/common/exec_tasks/")
        socket.onopen = function () {
            socket.send(JSON.stringify(data))
        };
        socket.onmessage = function (e) {
            if (e.data){
                if(e.data == 'over'){
                    $('button').prop('disabled', false)
                }
                else{
                    $('#msgc').append(e.data+'<br/>');
                }
            }
        };
    })
})