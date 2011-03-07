agency_select = function(e) {
    option = $("#id_agency option:selected");
    if (option.text() == "") {
        $("textarea").text("");
    }
    $.getJSON("/api/dp_summary/" + option.val(), function(data) {
        for (key in data) {
            $("#id_" + key).text(data[key])
        }
    });
}

$(document).ready(function(){
    $.loading({onAjax:true, text: 'Loading...'});
    $("#id_agency").change(agency_select);
    $("#id_agency").keyup(agency_select);

    $("#id_submit").click(function(e) {
        option = $("#id_agency option:selected");

        fields = $('[id^="id_"]');
        data = {}
        for (i = 0; i < fields.length; i++) {
            field = fields[i]
            name = field.name
            data[name] = field.value
        }

        $.post("/api/dp_summary/" + option.val() + "/", 
            data,
            function(data) {
            }
        );
        return false;
    });
});
