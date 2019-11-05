$(function () {
    $('#file_content').hide()
    $('button').prop('disabled', true)
    $('#config_file').jstree()
    $('#config_file').jstree().hide_icons()

    $('#config_file').on("changed.jstree", function (e, data) {
		var project = data.node.li_attr.name
        var type = data.node.li_attr.value
		var file_name = data.node.text
		info = {'project':project, 'file_name':file_name}

		if (type == 'file') {
		    $('button').prop('disabled', false)
            file_url = document.location.protocol + '//' + document.location.host + '/media/' + project + '/' + file_name
            p_text = '下载地址:  ' + '<a href=' + file_url + '>' + file_url + '</a>'
            $('#file_p').empty()
            $('#file_p').append(p_text)
		    $.ajax({
                url:"/common/open_file/",
                type:"POST",
                dataType:"Json",
                data:info,
                success:function(data){
                    $('.CodeMirror').remove()
                    show_content(data,project,file_name)
                }
            })
        }

	});

})

function show_content(data,project,file_name) {
    var editor = CodeMirror.fromTextArea(document.getElementById("file_content"), {
        lineNumbers: true,     // 显示行数
        indentUnit: 4,         // 缩进单位为4
        styleActiveLine: true, // 当前行背景高亮
        matchBrackets: true,   // 括号匹配
        mode: 'nginx',     // HMTL混合模式
        lineWrapping: true,    // 自动换行
        theme: 'monokai',      // 使用monokai模版
    });

    editor.setOption("extraKeys", {
        // Tab键换成4个空格
        Tab: function(cm) {
            var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
            cm.replaceSelection(spaces);
        },
        // F11键切换全屏
        "F11": function(cm) {
            cm.setOption("fullScreen", !cm.getOption("fullScreen"));
        },
        // Esc键退出全屏
        "Esc": function(cm) {
            if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
        }
    });
    editor.setValue(data.content)
    editor.setSize("100%", "100%")

    $('#save_file').click(function () {
        $('button').prop('disabled', true)
        content = editor.getValue()
        data = {'content':content,'project':project,'file_name':file_name}

        $.ajax({
            url:"/common/save_file/",
            type:"POST",
            dataType:"Json",
            data:data,
            success:function(data){
                $('button').prop('disabled', false)
                $('<div>').appendTo('body').addClass('alert alert-success').html('保存成功').show().delay(1500).fadeOut();
            }
        })
    })
}