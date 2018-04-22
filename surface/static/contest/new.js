function handleSelectChange() {
    localStorage.setItem("select_oj", $("#id_select").val());
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

function handleBadgeClick() {
    let tag_badge = $("#id_info");
    let remote_oj = tag_badge.data("remote_oj");
    let remote_id = tag_badge.data("remote_id");
}

function handleProblem(res) {
    let problem_info = $("#id_info");
    problem_info.attr("style", "");
    problem_info.attr("data-remote_oj", "");
    problem_info.attr("data-remote_id", "");
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
        problem_info.attr("data-remote_oj", res.data.remote_oj);
        problem_info.attr("data-remote_id", res.data.remote_id);
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

function handleProblemInfoClick() {
    let problem_badge = $("#id_info");
    if (problem_badge.attr("data-remote_oj") && problem_badge.attr("data-remote_id")) {
        let problem_not_exist = true;
        let problem_list_items = $("#id_problem_list .class_problem_item");
        for (let i = 0; i < problem_list_items.length; ++i) {
            if (problem_list_items[i].dataset.remote_oj === problem_badge.attr("data-remote_oj") &&
                problem_list_items[i].dataset.remote_id === problem_badge.attr("data-remote_id")) {
                problem_not_exist = false;
            }
        }
        let problem_list = $("#id_problem_list");
        if (problem_not_exist && problem_list_items.length < 30) {
            problem_list.append("<tr data-remote_oj='" + $(this).attr("data-remote_oj") + "' " +
                "data-remote_id='" + $(this).attr("data-remote_id") + "' " +
                "data-alias='" + $(this).html() + "' " +
                "class='class_problem_item'>\n" +
                "<td>" + $(this).attr("data-remote_oj") + "</td>\n" +
                "<td>" + $(this).attr("data-remote_id") + "</td>\n" +
                "<td>" + $(this).html() + "</td>\n" +
                "</tr>")
        }
    }
}

function handleFindButtonClick() {
    let problemObj = new Problem();
    let remote_oj = $("#id_select").val();
    let remote_id = $("#id_problem_id").val();
    problemObj.problem(remote_oj, remote_id, handleProblem);
}

function handleNewContest(res) {
    console.log(res);
    if (res.status === 0) {
        window.location.href = '/contest/' + res.data + '/';
    }
}

function handleSubmitButtonClick() {
    let problem_list_items = $("#id_problem_list .class_problem_item");
    let problem_list_data = [];
    for (let i = 0; i < problem_list_items.length; ++i) {
        problem_list_data.push({
            'remote_oj': problem_list_items[i].dataset.remote_oj,
            'remote_id': problem_list_items[i].dataset.remote_id,
            'alias': problem_list_items[i].dataset.alias
        })
    }
    let title_text = $("#id_title").val();
    if (title_text !== null && title_text !== "") {
        let post_data = {
            'title': title_text,
            'problems': JSON.stringify(problem_list_data)
        };
        console.log(post_data);
        let contestObj = new Contest();
        contestObj.contest_new(handleNewContest, post_data);
    }


}

$(document).ready(function () {
    $("#id_find_button").click(handleFindButtonClick);
    $("#id_submit_button").click(handleSubmitButtonClick);
    $("#id_info").click(handleProblemInfoClick);
    let remoteObj = new Remote();
    remoteObj.support(handleSupportList);
});