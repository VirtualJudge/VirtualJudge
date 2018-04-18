function handleSelectChange() {
    localStorage.setItem("select_oj", $("#id_select").val());
}

function handleProblemList(res) {
    $('#id_list').html("");
    res.data.forEach(function (data) {
        let item = "<tr data-remote_oj=\"" + data.remote_oj + "\" data-remote_id=\"" + data.remote_id + "\">";
        item += '<td>' + data.remote_oj + '</td>';
        item += '<td>' + data.remote_id + '</td>';
        item += '<td>' + data.title + '</td>';
        item += '<td>' + moment(data.update_time).calendar() + '</td>';
        item += '</tr>';
        $('#id_list').append(item);
    });
    $("tr").bind('click', handleTrClick);
}

function handleSupportList(res) {
    let select_list = $("#id_select");
    select_list.html();
    res.data.forEach(function (oj_name) {
        select_list.append("<option value=\"" + oj_name + "\">" + oj_name + "</option>");
    });
    if (localStorage.getItem("select_oj")) {
        select_list.val(localStorage.getItem("select_oj"));
    }
}

function handleInfoClick() {
    let problem_info = $("#id_info");
    let remote_oj = problem_info.attr("remote_oj");
    let remote_id = problem_info.attr("remote_id");
    if (remote_oj && remote_id) {
        localStorage.setItem("remote_oj", remote_oj);
        localStorage.setItem("remote_id", remote_id);
        window.location.href = '/problem/';
    }
}

function handleTrClick() {
    let remote_oj = $(this).attr("data-remote_oj");
    let remote_id = $(this).attr("data-remote_id");
    if (remote_oj && remote_id) {
        localStorage.setItem("remote_oj", remote_oj);
        localStorage.setItem("remote_id", remote_id);
        window.location.href = '/problem/';
    }
}

function handleProblem(res) {
    let problem_info = $("#id_info");
    problem_info.attr("style", "");
    problem_info.attr("remote_oj", "");
    problem_info.attr("remote_id", "");
    if (res.data.request_status === 0) {
        problem_info.attr("class", "badge badge-info");
        problem_info.html("题目等待中");
    } else if (res.data.request_status === 1) {
        problem_info.html("题目正在准备");
        problem_info.attr("class", "badge badge-primary");
    } else if (res.data.request_status === 2) {
        problem_info.html(res.data.title);
        problem_info.attr("class", "badge badge-success");
        problem_info.attr("style", "cursor:pointer;");
        problem_info.attr("remote_oj", res.data.remote_oj);
        problem_info.attr("remote_id", res.data.remote_id);
    } else if (res.data.request_status === 3) {
        problem_info.html("网络错误");
        problem_info.attr("class", "badge badge-warning");
    } else if (res.data.request_status === 4) {
        problem_info.html("题目不存在");
        problem_info.attr("class", "badge badge-danger");
    } else if (res.data.request_status === 5) {
        problem_info.html("系统繁忙，稍后重试");
        problem_info.attr("class", "badge badge-warning");
    } else if (res.data.request_status === 6) {
        problem_info.html("这个系统不被支持");
        problem_info.attr("class", "badge badge-danger");
    } else if (res.data.request_status === 7) {
        problem_info.html("网页内容解析错误");
        problem_info.attr("class", "badge badge-warning");
    }
}

function handleButtonClick() {
    let problemObj = new Problem();
    let remote_oj = $("#id_select").val();
    let remote_id = $("#id_problem_id").val();
    problemObj.problem(remote_oj, remote_id, handleProblem);

}

$("#id_button").click(handleButtonClick);
$(document).ready(function () {
    let problemObj = new Problem();
    let remoteObj = new Remote();
    problemObj.problems(handleProblemList);
    remoteObj.support(handleSupportList);
});


