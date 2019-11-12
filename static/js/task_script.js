$(function () {
    $('#a_task').addClass('active')
    $('#a_task_script').addClass('active')
    $('#ul_task').addClass('in')

    $('#file_content').hide()
    $('#save_file').prop('disabled', true)
    $('#del_file').prop('disabled', true)
    $('#add_file').prop('disabled', false)
    $('#task_script').jstree()
    $('#task_script').jstree().hide_icons()

    $('#task_script').on("changed.jstree", function (e, data) {
		var scritp_type = data.node.li_attr.name
        var type = data.node.li_attr.value
		var file_name = data.node.text
		info = {'type':scritp_type, 'file_name':file_name}
		if (type == 'file') {
		    $('button').prop('disabled', false)
            file_url = document.location.protocol + '//' + document.location.host + '/media/' + scritp_type + '/' + file_name
            p_text = '下载地址:  ' + '<a href=' + file_url + '>' + file_url + '</a>'
            $('#file_p').empty()
            $('#file_p').append(p_text)
		    $.ajax({
                url:"/common/open_script_file/",
                type:"POST",
                dataType:"Json",
                data:info,
                success:function(data){
                    $('.CodeMirror').remove()
                    show_content(data,scritp_type,file_name)
                }
            })
        }

	});

    $('#add_file').click(function () {
         window.open("/admin/deployjar/task/add/")
    })

})

function show_content(data,type,file_name) {
    var editor = CodeMirror.fromTextArea(document.getElementById("file_content"), {
        lineNumbers: true,     // 显示行数
        indentUnit: 4,         // 缩进单位为4
        styleActiveLine: true, // 当前行背景高亮
        matchBrackets: true,   // 括号匹配
        mode: 'shell',     // HMTL混合模式
        lineWrapping: true,    // 自动换行
        theme: 'ambiance',      // 使用monokai模版
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
        data = {'content':content,'type':type,'file_name':file_name}

        $.ajax({
            url:"/common/save_script_file/",
            type:"POST",
            dataType:"Json",
            data:data,
            success:function(data){
                $('button').prop('disabled', false)
                swal({
                    title: "保存成功！",
                });
            }
        })
    })

    $('#del_file').click(function () {
        data = {'type':type,'file_name':file_name}
        msg = '确定删除\"' + '\" shell 脚本文件: ' + '\"' + file_name + '\"?'

        swal({
            title: msg,
            text: "文件删除后无法恢复!",
            showCancelButton: true,
            cancelButtonText: "取消",
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确定",
            closeOnConfirm: false
        }, function () {
            $.ajax({
                url:"/common/del_script_file/",
                type:"POST",
                dataType:"Json",
                data:data,
                success:function(data){
                    swal({
                        title: "删除!",
                        text: "文件已经删除.",
                        confirmButtonText: "确定",
                        },
                        function(){
                            window.location.href = "/common/task_script/"
                        });
                }
            })
        });
    })
}