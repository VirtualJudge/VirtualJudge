function handleSupport(res) {
    let remotes = "";
    res.data.forEach(function (oj_name) {
        remotes += "<option value=\"" + oj_name + "\">" + oj_name + "</option>";
    });
    localStorage.setItem('supports', remotes);
    return remotes;
}

function getRemotes() {
    if (localStorage.getItem('supports') === null || localStorage.getItem('set_supports_times') === null || moment().subtract(1, 'hours').isAfter(localStorage.getItem('set_supports_times'))) {
        getSupport(handleSupport);
        localStorage.setItem('set_supports_times', moment().format());
    }
    return localStorage.getItem('supports');

}

function getRemoteItem() {
    return "                                <div  class=\"form-row id_pid_item\">\n" +
        "                                    <div class=\"form-group col-md-3\">\n" +
        "                                        <select class=\"class_supports form-control class_oid\">\n" +
        getRemotes() +
        "                                        </select>\n" +
        "\n" +
        "                                    </div>\n" +
        "                                    <div class=\"form-group col-md-2\">\n" +
        "                                        <input type=\"text\" class=\"form-control class_pid\" placeholder=\"源编号\">\n" +
        "                                    </div>\n" +
        "                                    <div class=\"form-group col-md-4\">\n" +
        "                                        <input type=\"text\" class=\"form-control class_alias\" placeholder=\"重命名\">\n" +
        "                                    </div>\n" +
        "                                    <div class=\"form-group col-md-3\">\n" +
        "                                        <span class=\"badge class_link\"></span>\n" +
        "                                    </div>\n" +
        "                                </div>\n";
}


function handlePidChange() {
    let this_tr = $(this).parent().parent();
    getProblem(this_tr.find('.class_oid').val(), this_tr.find('.class_pid').val(), this_tr.find('.class_link'), handleProblemSearch);
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
    if ($("#id_pid_list").children().length > 0) {
        $("#id_pid_list").children("div:last-child").remove();
        $("#id_add_pid").disabled = false
    } else {
        $(this).disabled = true
    }
});
$(document).ready(function () {
    $("#id_start_time").val(moment().format("YYYY-MM-DDTLT"));
    $("#id_start_time").attr('time_offset', moment().format("Z"));
    $("#id_end_time").val(moment().add(5, 'h').format("YYYY-MM-DDTLT"));
    $("#id_end_time").attr('time_offset', moment().format("Z"));
});
$("#id_button").click(function () {
    $("#id_pid_list").children().each(function (i, item) {
        console.log(item.children());
        console.log(i);
    });
});
