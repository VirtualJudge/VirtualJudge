function handleSupport(res) {
    let remotes = "";
    res.data.forEach(function (oj_name) {
        remotes += "<option value=\"" + oj_name + "\">" + oj_name + "</option>";
    });
    localStorage.setItem('supports', remotes);
    localStorage.setItem('set_supports_times', moment().format());
    return remotes;
}

function getRemotes() {
    if (localStorage.getItem('supports') === null || localStorage.getItem('set_supports_times') === null || moment().subtract(1, 'hours').isAfter(localStorage.getItem('set_supports_times'))) {
        let remoteObj = new Remote();
        remoteObj.support(handleSupport);
    }
    return localStorage.getItem('supports');

}

// 上面函数有BUG

function getRemoteItem() {
    return "<div class=\"form-row id_pid_item\">\n" +
        "<div class=\"form-group col-md-3\">\n" +
        "<select class=\"class_supports form-control class_oid\">\n" +
        getRemotes() +
        "</select>\n" +
        "\n" +
        "</div>\n" +
        "<div class=\"form-group col-md-2\">\n" +
        "<input type=\"text\" class=\"form-control class_pid\" placeholder=\"源编号\">\n" +
        "</div>\n" +
        "<div class=\"form-group col-md-4\">\n" +
        "<input type=\"text\" class=\"form-control class_alias\" placeholder=\"重命名\">\n" +
        "</div>\n" +
        "<div class=\"form-group col-md-3\">\n" +
        "<span class=\"badge class_link\"></span>\n" +
        "</div>\n" +
        "</div>\n";
}


function handlePidChange() {
    let this_tr = $(this).parent().parent();
    let problemObj = new Problem();
    problemObj.problem(this_tr.find('.class_oid').val(), this_tr.find('.class_pid').val(), this_tr.find('.class_link'), void(0));
}

$('#id_add_pid').click(function () {
    if ($("#id_pid_list").children().length < 30) {
        $("#id_pid_list").append(getRemoteItem());
        if (localStorage.getItem('select_oj')) {
            $("#id_pid_list").children(":last-child").find('.class_oid').val(localStorage.getItem('select_oj'));
        }
        //$('.class_pid').unbind('blur');
        // $('.class_pid').bind('blur', handlePidChange);
        $(document).on('change', '.class_oid', handleSelectChange);
        $("#id_delete_pid").disabled = false
    } else {
        $(this).disabled = true
    }
});

function handleSelectChange() {
    localStorage.setItem("select_oj", $(this).val());
}

$("#id_delete_pid").click(function () {
    let tag_pid_list = $("#id_pid_list");
    if (tag_pid_list.children().length > 0) {
        tag_pid_list.children("div:last-child").remove();
        $("#id_add_pid").disabled = false
    } else {
        $(this).disabled = true
    }
});
$(document).ready(function () {
    let start_time_tag = $("#id_start_time");
    let end_time_tag = $("#id_end_time");
    start_time_tag.val(moment().add(1, 'h').format("YYYY-MM-DDTLT"));
    end_time_tag.val(moment().add(6, 'h').format("YYYY-MM-DDTLT"));

    let remoteObj = new Remote();
    remoteObj.support(handleSupport);
});

function handleNewContest(res) {
    console.log(res);
    if (res.status === 0) {
        window.location.href = '/contests/';
    } else {
        alert(res.data);
    }
}

$("#id_button").click(function () {
    let error_message = "";
    let title = $("#id_title").val();
    let start_time = $("#id_start_time").val();
    let end_time = $("#id_end_time").val();
    let problems = [];
    $("#id_pid_list").children('div').each(function (i) {
        problems.push({
            'remote_oj': $(this).find('.class_oid').val(),
            'remote_id': $(this).find('.class_pid').val()
        })
    });
    for (let i = 0; i < problems.length; ++i) {
        if (problems[i].remote_id === null || problems[i].remote_oj === null) {
            error_message += "remote_oj or remote_id can not none\n"
        }
    }
    console.log(title);
    console.log(start_time);
    console.log(end_time);
    console.log(problems);
    if (error_message) {
        alert(error_message);
    } else {
        let contestObj = new Contest();
        contestObj.contest({
            'title': title,
            'start_time': start_time,
            'end_time': end_time,
            'problems': JSON.stringify(problems)
        }, handleNewContest);
    }
});
