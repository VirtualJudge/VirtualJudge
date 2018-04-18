function getColorVerdict(val, code) {
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
    return " ";
}

function spaceCheck(val) {
    if (val) {
        return val;
    } else {
        return " ";
    }
}

function handleSubmissionItemClick() {
    console.log($(this).attr('sid'))
}

function handleStatusList(res) {
    res.data.forEach(function (item) {

        $("#id_list").append("<tr class=\"submission_list_item\" sid=" + item.id + ">" +
            "<td>" + item.id + "</td>" +
            "<td>" + item.remote_oj + "</td>" +
            "<td>" + item.remote_id + "</td>" +
            "<td>" + item.user + "</td>" +
            "<td>" + verdictCheck(item.verdict, item.verdict_code) + "</td>" +
            "<td>" + spaceCheck(item.language_name) + "</td>" +
            "<td>" + spaceCheck(item.execute_time) + "</td>" +
            "<td>" + spaceCheck(item.execute_memory) + "</td>" +
            "<td>" + moment(item.create_time).calendar() + "</td>" +
            "</tr>"
        )
    });
    $(document).on('click', '.submission_list_item', handleSubmissionItemClick);
}

function loadStatusList() {
    getStatusList(handleStatusList);
}

$(document).ready(function () {
    loadStatusList();
    // setInterval(loadStatusList, 5000);
})
