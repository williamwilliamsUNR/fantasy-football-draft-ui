'use strict';

$(document).ready(function() {

});

$("#start_draft_planning").click(function() {
    $("#error_message").attr("hidden", true);

    let number_draft_players = parseInt($('input[name=number_players]:checked').val());
    let number_rounds = parseInt($("#number_rounds_input").val());
    let draft_position = parseInt($("#draft_position_input").val());

    if (draft_position > number_draft_players || draft_position < 1) {
       $("#error_message").html(`ERROR: Draft position cannont be greater than ${number_draft_players} or less than zero.`);
       $("#error_message").removeAttr("hidden");
       return;
    }

    let draftSettingsUpdated = function() {
        location.href = "/draftboard/round/next";
    }

    $.ajax({
        url: "/draftboard/initialize", 
        contentType: "application/json",
        type: "POST",
        data: JSON.stringify({
            "number_players" : number_draft_players,
            "number_rounds" : number_rounds,
            "draft_position" : draft_position
        }),
        success: draftSettingsUpdated,
        error: function() {
            $("#error_message").html(`ERROR: Initializing Draft Settings Failed.`);
            $("#error_message").removeAttr("hidden");
            return;
        }
    });
});
