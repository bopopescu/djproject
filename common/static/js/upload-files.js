$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $("#upload_files").click(function () {
    $("#fileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
          "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td>" + '<td><a href="/common/remove_file/' + data.result.id + '/">移除</a></td>' + "</tr>"
        )
      }
    }
  });

  $('#update_files').click(function () {
        $('button').prop('disabled', true)
        $('#messagecontainer').empty()

        var socket = new WebSocket("ws://" + window.location.host + "/common/update_files/");

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
});