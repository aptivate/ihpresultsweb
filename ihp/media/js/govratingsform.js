country_select = function(e) {
    country_id = $("#id_country option:selected");
    $("textarea").text("");

    $.getJSON("/api/gov_ratings/" + country_id.val(), function(data) {
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
    $("#id_country").change(country_select);
    $("#id_country").keyup(country_select);

    $("#id_submit").click(function(e) {
        country_id = $("#id_country option:selected");

        fields = $('[id^="id_"]');
        data = {}
        for (i = 0; i < fields.length; i++) {
            field = fields[i]
            name = field.name
            data[name] = field.value
        }

        $.post("/api/gov_ratings/" + country_id.val() + "/", 
            data , 
            function(data) {
                for (key in data) {
                    $("#id_" + key).text(data[key])
                }
            },
            "json"
        );

        return false;
    });
});
