agency_select = function(e) {
    option = $("#id_agency option:selected");
    if (option.text() == "") {
        $("textarea").text("");
    }
    $.loading({onAjax:true, text: 'Loading...'});
    $.getJSON("/api/dp_summary/" + option.val(), function(data) {
        $("#id_text1").text(data["1DP"]);
        $("#id_text2a").text(data["2DPa"]);
        $("#id_text2b").text(data["2DPb"]);
        $("#id_text2c").text(data["2DPc"]);
        $("#id_text3").text(data["3DP"]);
        $("#id_text4").text(data["4DP"]);
        $("#id_text5a").text(data["5DPa"]);
        $("#id_text5b").text(data["5DPb"]);
        $("#id_text5c").text(data["5DPc"]);
        $("#id_text6").text(data["6DP"]);
        $("#id_text7").text(data["7DP"]);
        $("#id_text8").text(data["8DP"]);

        $("#id_summary1").text(data["summary1"]);
        $("#id_summary2").text(data["summary2"]);
        $("#id_summary3").text(data["summary3"]);
        $("#id_summary4").text(data["summary4"]);
        $("#id_summary5").text(data["summary5"]);
        $("#id_summary6").text(data["summary6"]);
        $("#id_summary7").text(data["summary7"]);
        $("#id_summary8").text(data["summary8"]);
    });
}

$(document).ready(function(){
    $("#id_agency").change(agency_select);
    $("#id_agency").keyup(agency_select);

    $("#id_submit").click(function(e) {
        option = $("#id_agency option:selected");

        $.loading({onAjax:true, text: 'Saving...'});
        $.post("/api/dp_summary/" + option.val() + "/", 
            { 
                summary1: $("#id_summary1").val(),
                summary2: $("#id_summary2").val(),
                summary3: $("#id_summary3").val(),
                summary4: $("#id_summary4").val(),
                summary5: $("#id_summary5").val(),
                summary6: $("#id_summary6").val(),
                summary7: $("#id_summary7").val(),
                summary8: $("#id_summary8").val()
            },
            function(data) {
            }
        );
        return false;
    });
});
