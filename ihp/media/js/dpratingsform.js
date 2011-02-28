agency_select = function(e) {
    option = $("#id_agency option:selected");
    $("textarea").text("");

    $.getJSON("/api/dp_ratings/" + option.val(), function(data) {
        for (key in data) {
            x = $("#id_" + key);
            if (x[0] && x[0].nodeName == "DIV")
                $("#id_" + key).text(data[key])
            else
                $("#id_" + key).val(data[key])
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

        $.post("/api/dp_ratings/" + option.val() + "/", 
            data,
            function(data) {
                $("#id_gr1").text(data["gr1"]);
                $("#id_gr2a").text(data["gr2a"]);
                $("#id_gr2b").text(data["gr2b"]);
                $("#id_gr2c").text(data["gr2c"]);
                $("#id_gr3").text(data["grn3"]);
                $("#id_gr4").text(data["gr4"]);
                $("#id_gr5a").text(data["gr5a"]);
                $("#id_gr5b").text(data["gr5b"]);
                $("#id_gr5c").text(data["gr5c"]);
                $("#id_gr6").text(data["gr6"]);
                $("#id_gr7").text(data["gr7"]);
                $("#id_gr8").text(data["gr8"]);
            }, "json"
        );
        return false;
    });
});
