agency_select = function(e) {
    option = $("#id_agency option:selected");
    $("textarea").text("");
    //$("select").val("");

    $.getJSON("/api/dp_ratings/" + option.val(), function(data) {
        // TODO still need to do ratings
        $("#id_r1").val(data["rating1"]);
        $("#id_r2a").val(data["rating2a"]);
        $("#id_r2b").val(data["rating2b"]);
        $("#id_r2c").val(data["rating2c"]);
        $("#id_r3").val(data["rating3"]);
        $("#id_r4").val(data["rating4"]);
        $("#id_r5a").val(data["rating5a"]);
        $("#id_r5b").val(data["rating5b"]);
        $("#id_r5c").val(data["rating5c"]);
        $("#id_r6").val(data["rating6"]);
        $("#id_r7").val(data["rating7"]);
        $("#id_r8").val(data["rating8"]);

        $("#id_er1").text(data["progress1"]);
        $("#id_er2a").text(data["progress2a"]);
        $("#id_er2b").text(data["progress2b"]);
        $("#id_er2c").text(data["progress2c"]);
        $("#id_er3").text(data["progress3"]);
        $("#id_er4").text(data["progress4"]);
        $("#id_er5a").text(data["progress5a"]);
        $("#id_er5b").text(data["progress5b"]);
        $("#id_er5c").text(data["progress5c"]);
        $("#id_er6").text(data["progress6"]);
        $("#id_er7").text(data["progress7"]);
        $("#id_er8").text(data["progress8"]);
    });
}

$(document).ready(function(){
    $.loading({onAjax:true, text: 'Loading...'});
    $("#id_agency").change(agency_select);
    $("#id_agency").keyup(agency_select);

    $("#id_submit").click(function(e) {
        option = $("#id_agency option:selected");

        $.post("/api/dp_ratings/" + option.val() + "/", 
            { 
                r1: $("#id_r1").val(),
                er1: $("#id_er1").val(),
                r2a: $("#id_r2a").val(),
                er2a: $("#id_er2a").val(),
                r2b: $("#id_r2b").val(),
                er2b: $("#id_er2b").val(),
                r2c: $("#id_r2c").val(),
                er2c: $("#id_er2c").val(),
                r3: $("#id_r3").val(),
                er3: $("#id_er3").val(),
                r4: $("#id_r4").val(),
                er4: $("#id_er4").val(),
                r5a: $("#id_r5a").val(),
                er5a: $("#id_er5a").val(),
                r5b: $("#id_r5b").val(),
                er5b: $("#id_er5b").val(),
                r5c: $("#id_r5c").val(),
                er5c: $("#id_er5c").val(),
                r6: $("#id_r6").val(),
                er6: $("#id_er6").val(),
                r7: $("#id_r7").val(),
                er7: $("#id_er7").val(),
                r8: $("#id_r8").val(),
                er8: $("#id_er8").val(),
            },
            function(data) {
            }
        );
        return false;
    });
});
