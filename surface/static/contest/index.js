function getItemStatus(status_id) {
    if (status_id === 0) {
        return "<span class='badge badge-success'>Passed</span>"
    } else if (status_id === 1) {
        return "<span class='badge badge-secondary'>Tried</span>"
    } else {
        return "<span class='badge badge-default'></span>"
    }
}

function handleProblemList(res) {
    if (res.status === 0) {
        res.data.forEach(function (item) {
            let text = "<tr>\n" +
                "<td>" + getItemStatus(item.status) + "</td>\n" +
                "<td>" + item.remote_oj + "</td>\n" +
                "<td>" + item.remote_id + "</td>\n" +
                "<td><a href='/problem/" + item.remote_oj + "/" + item.remote_id + "/'>" + item.alias + "</a></td>\n" +
                "</tr>\n";
            $("#id_problem_list").append(text);
        });

    }
}

$(document).ready(function () {
    let contest_id = window.location.pathname.split('/')[2];
    let contestObj = new Contest();
    contestObj.problems(contest_id, handleProblemList);
});