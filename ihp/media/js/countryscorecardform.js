country_select = function(e) {
    option = $("#id_country option:selected");
    $("textarea").text("");
    //$("select").val("");

    $.getJSON("/api/country_scorecard/" + option.val(), function(data) {
        // TODO still need to do ratings
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
            name = field.id.split("_")[1]
            data[name] = field.value
        }

        $.post("/api/country_scorecard/" + option.val() + "/", 
            data , function(data) {}, "json"
        );
        return false;
    });
});
