function getFileName(o) {
    let pos = o.lastIndexOf("\\");
    return o.substring(pos + 1);
}

$("#id_file").change(function () {
    $("#id_file_label").html(getFileName($("#id_file").val()));
});

function reInitFrame() {
    var iframe = document.getElementById("id_frame");
    try {
        var bHeight = iframe.contentWindow.document.body.scrollHeight;
        var dHeight = iframe.contentWindow.document.documentElement.scrollHeight;
        var height = Math.min(bHeight, dHeight);
        iframe.height = height;
    } catch (ex) {
    }
}

var timer = null;
var submission_id = null;

function getColorVerdict(val, code) {
    console.log(val, code);
    switch (code) {
        case 0:
            return "<span class=\"badge badge-secondary\">" + val + "</span>";
        case 1:
            return "<span class=\"badge badge-success\">" + val + "</span>";
        case 2:
            return "<span class=\"badge badge-warning\">" + val + "</span>";
        case 3:
            return "<span class=\"badge badge-danger\">" + val + "</span>";
        case 4:
            return "<span class=\"badge badge-primary\">" + val + "</span>";
    }
}

function verdictCheck(val, code) {
    if (val) {
        return getColorVerdict(val, code);
    }
    return getColorVerdict("Pending", code);
}

function handleVerdict(res) {
    if (res.status === 0) {

        $("#id_result").html("");
        //     $("#id_verdict_ul").append("<dl> <dt>提交编号:</dt> <dd>" + res.data.id + "</dd></d;>");
        $("#id_result").html(verdictCheck(res.data.verdict, res.data.verdict_code));
        //     $("#id_verdict_ul").append("<dl> <dt>运行时间:</dt> <dd>" + res.data.execute_time + "</dd></d;>");
        //    $("#id_verdict_ul").append("<dl> <dt>运行内存:</dt> <dd>" + res.data.execute_memory + "</dd></d;>");
        //     $("#id_verdict_ul").append("<dl> <dt>爬取状态:</dt> <dd>" + res.data.status + "</dd></d;>");
        if (res.data.verdict_status === true) {
            clearInterval(timer);
        }
    } else {
        clearInterval(timer);
    }
}

function queryVerdict() {
    getVerdict(submission_id, handleVerdict);
}

function handleSubmitId(res) {
    $("#id_message").html("");
    if (res.status === 0) {
        submission_id = res.data;
        timer = setInterval(queryVerdict, 1000);
    } else {
        $("#id_message").html(res.status);
    }
}

function handleButtonClick() {
    let remote_oj = localStorage.getItem("remote_oj");
    let remote_id = localStorage.getItem("remote_id");
    let language = $("#id_language").val();
    var selectedFile = document.getElementById("id_file").files[0];
    var reader = new FileReader();
    reader.readAsText(selectedFile);
    reader.onload = function () {
        submitCode(remote_oj, remote_id, this.result, language, handleSubmitId);
    };
}

function handleProblemInfo(res, who = null) {
    $("#id_title").html(res.data.title);
    $("#id_ul").html();
    //$("#id_ul").append("<li class=\"list-group-item\">" + res.data.id + "</li>");
    $("#id_ul").append("<li class=\"list-group-item\">来源平台: <span class=\"badge badge-dark\">" + res.data.remote_oj + "</span></li>");
    $("#id_ul").append("<li class=\"list-group-item\">来源编号: <span class=\"badge badge-secondary\">" + res.data.remote_id + "</span></li>");
    $("#id_ul").append("<li class=\"list-group-item\">时间限制: <span class=\"badge badge-primary\">" + res.data.time_limit + "</span></li>");
    $("#id_ul").append("<li class=\"list-group-item\">内存限制: <span class=\"badge badge-success\">" + res.data.memory_limit + "</span></li>");
    $("#id_ul").append("<li class=\"list-group-item\">更新时间: <span class=\"badge badge-info\">" + moment(res.data.update_time).fromNow() + "</span></li>");
}

function handleLanguageChange() {
    let remote_oj = localStorage.getItem("remote_oj");
    let oj_language = $("#id_language").val();
    localStorage.setItem(remote_oj + "_prefer_language", oj_language);
}

function handleLanguageList(res) {
    res.data.forEach(function (language) {
        $("#id_language").append("<option value=\"" + language.oj_language + "\">" + language.oj_language_name + "</option>");
    });
    let remote_oj = localStorage.getItem("remote_oj");
    let oj_language = localStorage.getItem(remote_oj + "_prefer_language");
    if (oj_language) {
        $("#id_language").val(oj_language);
    }

}

$(document).ready(function () {
    $("#id_frame").attr("src", "/api/problem/" + localStorage.getItem("remote_oj") + "/" + localStorage.getItem("remote_id") + "/html/");
    window.setInterval("reInitFrame()", 200);
    getProblem(localStorage.getItem("remote_oj"), localStorage.getItem("remote_id"), handleProblemInfo);
    getLanguageList(localStorage.getItem("remote_oj"), handleLanguageList);
});
