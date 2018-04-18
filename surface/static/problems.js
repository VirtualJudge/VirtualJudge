function handleSelectChange() {
    localStorage.setItem("select_oj", $("#id_select").val());
}

function handleProblemList(res) {
    $('#id_list').html("");
    res.data.forEach(function (data) {
        let item = "<tr remote_oj=\"" + data.remote_oj + "\" remote_id=\"" + data.remote_id + "\">";
        item += '<td>' + data.id + '</td>';
        item += '<td>' + data.remote_oj + '</td>';
        item += '<td>' + data.remote_id + '</td>';
        item += '<td>' + data.title + '</td>';
        item += '<td>' + moment(data.update_time).calendar() + '</td>';
        item += '</tr>';
        $('#id_list').append(item);
    });
    $(document).on('click', 'tr', handleTrClick);
}

function handleSupportList(res) {
    res.data.forEach(function (oj_name) {
        $("#id_select").append("<option value=\"" + oj_name + "\">" + oj_name + "</option>");
        if (localStorage.getItem("select_oj")) {
            $("#id_select").val(localStorage.getItem("select_oj"));
        }
    })
}

function handleInfoClick() {
    var remote_oj = $("#id_info").attr("remote_oj");
    var remote_id = $("#id_info").attr("remote_id");
    if (remote_oj && remote_id) {
        localStorage.setItem("remote_oj", remote_oj);
        localStorage.setItem("remote_id", remote_id);
        window.location.href = '/problem/';
    }
}

function handleTrClick() {
    var remote_oj = $(this).attr("remote_oj");
    var remote_id = $(this).attr("remote_id");
    if (remote_oj && remote_id) {
        localStorage.setItem("remote_oj", remote_oj);
        localStorage.setItem("remote_id", remote_id);
        window.location.href = '/problem/';
    }
}

function handleProblem(res) {
    $("#id_info").attr("style", "");
    $("#id_info").attr("remote_oj", "");
    $("#id_info").attr("remote_id", "");
    if (res.data.request_status === 0) {
        $("#id_info").attr("class", "badge badge-info");
        $("#id_info").html("题目等待中");
    } else if (res.data.request_status === 1) {
        $("#id_info").html("题目正在准备");
        $("#id_info").attr("class", "badge badge-primary");
    } else if (res.data.request_status === 2) {
        $("#id_info").html(res.data.title);
        $("#id_info").attr("class", "badge badge-success");
        $("#id_info").attr("style", "cursor:pointer;");
        $("#id_info").attr("remote_oj", res.data.remote_oj);
        $("#id_info").attr("remote_id", res.data.remote_id);
    } else if (res.data.request_status === 3) {
        $("#id_info").html("网络错误");
        $("#id_info").attr("class", "badge badge-warning");
    } else if (res.data.request_status === 4) {
        $("#id_info").html("题目不存在");
        $("#id_info").attr("class", "badge badge-danger");
    } else if (res.data.request_status === 5) {
        $("#id_info").html("系统繁忙，稍后重试");
        $("#id_info").attr("class", "badge badge-warning");
    } else if (res.data.request_status === 6) {
        $("#id_info").html("这个系统不被支持");
        $("#id_info").attr("class", "badge badge-danger");
    } else if (res.data.request_status === 7) {
        $("#id_info").html("网页内容解析错误");
        $("#id_info").attr("class", "badge badge-warning");
    }
}

function handleButtonClick() {
    getProblem($("#id_select").val(), $("#id_problem_id").val(), handleProblem);

}

$("#id_button").click(handleButtonClick);
$(document).ready(function () {
    getProblemList(handleProblemList);
    getSupport(handleSupportList);
});


