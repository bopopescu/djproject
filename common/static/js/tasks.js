$(function () {
    $("#tasks").click(function () {
        $.ajax({
            type: "POST",
            url: "/api/get/groupUsers",
            contentType: "application/json",
            data: JSON.stringify(groupId),
        })
    })
})