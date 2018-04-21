function getBadge(id, val) {
    let badges = ['badge badge-primary',
        'badge badge-secondary',
        'badge badge-success',
        'badge badge-danger',
        'badge badge-warning',
        'badge badge-info',
        'badge badge-light',
        'badge badge-dark'];
    return "<span class=\"" + badges[id % 8] + "\">" + val + "</span>";
}

function handleContestList(res) {
    console.log(res);
    if (res.status === 0) {
        res.data.forEach(function (item) {
            let text = "<li class=\"list-group-item\">\n" +
                "<div class=\"media\">\n" +
                "<div class=\"media-body\">\n" +
                "<h5 class=\"mt-0\">" + item.id + " - " + item.title + "</h5>" +
                "<p>" + item.user + "</p>" +
                "<hr/>" +
                "<a class=\"btn btn-primary\" href=\"/contest/" + item.id + "/\">查看</a>\n" +
                "</div>\n" +
                "</div>\n" +
                "</li>";
            $("#id_contest_list").append(text);
        });

    }

}

$(document).ready(function () {
    let contestObj = new Contest();
    contestObj.contests(handleContestList);
});