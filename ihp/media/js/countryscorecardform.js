country_select = function(e) {
    option = $("#id_country option:selected");
    $("textarea").text("");

    $.getJSON("/api/country_scorecard/" + option.val(), function(data) {
        for (key in data) {
            $("#id_" + key).val(data[key])
        }
    });
}

$(document).ready(function(){
    $.loading({onAjax:true, text: 'Loading...'});
    $("#id_country").change(country_select);
    $("#id_country").keyup(country_select);

    $("#id_submit").click(function(e) {
        option = $("#id_country option:selected");
        
        fields = $('[id^="id_"]');
        data = {}
        for (i = 0; i < fields.length; i++) {
            field = fields[i]
            name = field.name
            data[name] = field.value
        }

        $.post("/api/country_scorecard/" + option.val() + "/", 
            data , function(data) {}, "json"
        );
        return false;
    });
});
