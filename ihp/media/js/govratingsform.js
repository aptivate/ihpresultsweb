country_select = function(e) {
    country_id = $("#id_country option:selected");
    $("textarea").text("");

    $.getJSON("/api/gov_ratings/" + country_id.val(), function(data) {
        $("#id_r1").val(data["rating1"]);
        $("#id_r2a").val(data["rating2a"]);
        $("#id_r2b").val(data["rating2b"]);
        $("#id_r3").val(data["rating3"]);
        $("#id_r4").val(data["rating4"]);
        $("#id_r5a").val(data["rating5a"]);
        $("#id_r5b").val(data["rating5b"]);
        $("#id_r6").val(data["rating6"]);
        $("#id_r7").val(data["rating7"]);
        $("#id_r8").val(data["rating8"]);

        $("#id_er1_en").text(data["progress1_en"]);
        $("#id_er2a_en").text(data["progress2a_en"]);
        $("#id_er2b_en").text(data["progress2b_en"]);
        $("#id_er3_en").text(data["progress3_en"]);
        $("#id_er4_en").text(data["progress4_en"]);
        $("#id_er5a_en").text(data["progress5a_en"]);
        $("#id_er5b_en").text(data["progress5b_en"]);
        $("#id_er6_en").text(data["progress6_en"]);
        $("#id_er7_en").text(data["progress7_en"]);
        $("#id_er8_en").text(data["progress8_en"]);

        $("#id_er1_fr").text(data["progress1_fr"]);
        $("#id_er2a_fr").text(data["progress2a_fr"]);
        $("#id_er2b_fr").text(data["progress2b_fr"]);
        $("#id_er3_fr").text(data["progress3_fr"]);
        $("#id_er4_fr").text(data["progress4_fr"]);
        $("#id_er5a_fr").text(data["progress5a_fr"]);
        $("#id_er5b_fr").text(data["progress5b_fr"]);
        $("#id_er6_fr").text(data["progress6_fr"]);
        $("#id_er7_fr").text(data["progress7_fr"]);
        $("#id_er8_fr").text(data["progress8_fr"]);

        $("#id_gr1").text(data["gen1"]);
        $("#id_gr2a").text(data["gen2a"]);
        $("#id_gr2b").text(data["gen2b"]);
        $("#id_gr3").text(data["gen3"]);
        $("#id_gr4").text(data["gen4"]);
        $("#id_gr5a").text(data["gen5a"]);
        $("#id_gr5b").text(data["gen5b"]);
        $("#id_gr6").text(data["gen6"]);
        $("#id_gr7").text(data["gen7"]);
        $("#id_gr8").text(data["gen8"]);
    });
}

$(document).ready(function(){
    $.loading({onAjax:true, text: 'Loading...'});
    $("#id_country").change(country_select);
    $("#id_country").keyup(country_select);

    $("#id_submit").click(function(e) {
        country_id = $("#id_country option:selected");

        $.post("/api/gov_ratings/" + country_id.val() + "/", 
            { 
                r1: $("#id_r1").val(),
                er1_en: $("#id_er1_en").val(),
                er1_fr: $("#id_er1_fr").val(),
                r2a: $("#id_r2a").val(),
                er2a_en: $("#id_er2a_en").val(),
                er2a_fr: $("#id_er2a_fr").val(),
                r2b: $("#id_r2b").val(),
                er2b_en: $("#id_er2b_en").val(),
                er2b_fr: $("#id_er2b_fr").val(),
                r3: $("#id_r3").val(),
                er3_en: $("#id_er3_en").val(),
                er3_fr: $("#id_er3_fr").val(),
                r4: $("#id_r4").val(),
                er4_en: $("#id_er4_en").val(),
                er4_fr: $("#id_er4_fr").val(),
                r5a: $("#id_r5a").val(),
                er5a_en: $("#id_er5a_en").val(),
                er5a_fr: $("#id_er5a_fr").val(),
                r5b: $("#id_r5b").val(),
                er5b_en: $("#id_er5b_en").val(),
                er5b_fr: $("#id_er5b_fr").val(),
                r6: $("#id_r6").val(),
                er6_en: $("#id_er6_en").val(),
                er6_fr: $("#id_er6_fr").val(),
                r7: $("#id_r7").val(),
                er7_en: $("#id_er7_en").val(),
                er7_fr: $("#id_er7_fr").val(),
                r8: $("#id_r8").val(),
                er8_en: $("#id_er8_en").val(),
                er8_fr: $("#id_er8_fr").val(),
            },
            function(data) {
                $("#id_gr1").text(data["gen1"]);
                $("#id_gr2a").text(data["gen2a"]);
                $("#id_gr2b").text(data["gen2b"]);
                $("#id_gr3").text(data["gen3"]);
                $("#id_gr4").text(data["gen4"]);
                $("#id_gr5a").text(data["gen5a"]);
                $("#id_gr5b").text(data["gen5b"]);
                $("#id_gr6").text(data["gen6"]);
                $("#id_gr7").text(data["gen7"]);
                $("#id_gr8").text(data["gen8"]);
            },
            "json"
        );
        return false;
    });
});
