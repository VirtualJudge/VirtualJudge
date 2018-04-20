function handleRank(res) {
    console.log(res);
    let rank = $("#id_rank_list");
    rank.html('');
    if (res.status === 0) {
        res.data.forEach(function (data, index) {
            console.log(data);
            let item = "<tr>";
            item += '<td>' + (index + 1) + '</td>';
            item += '<td>' + data.username + '</td>';
            item += '<td>' + data.accepted + '</td>';
            item += '<td>' + data.attempted + '</td>';
            item += '<td>' + data.submitted + '</td>';
            item += '</tr>';
            rank.append(item);
        })
    }
}

$(document).ready(function () {
    let accoutObj = new Account();
    accoutObj.rank(handleRank);
});