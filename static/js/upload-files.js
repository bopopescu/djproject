$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $("#upload_files").click(function () {
      $("#fileupload").click();
  });

  $('#li_template').addClass('active')
  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#fileupload").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      if (data.result.is_valid) {
        $("#gallery tbody").prepend(
           window.location.href = '/common/upload-files/'
        )
      }
    }
  });
});