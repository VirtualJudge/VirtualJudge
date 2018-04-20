function handleContestList(res) {
    console.log(res);
    if (res.status === 0) {
        res.data.forEach(function (item) {
            let text = "<li class=\"list-group-item\">\n" +
                "<div class=\"media\">\n" +
                "<div class=\"media-body\">\n" +
                "<h5 class=\"mt-0\">" + item.id + " - " + item.title + "</h5>\n" +
                "开始时间:<span class=\"badge badge-secondary\">" + moment(item.start_time).calendar() + "</span>\n" +
                "结束时间:<span class=\"badge badge-secondary\">" + moment(item.end_time).calendar() + "</span>" +
                "<br/> <br/>" +
                "<a class=\"btn btn-primary\" href=\"/contest/" + item.id + "/\">进入</a>\n" +
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