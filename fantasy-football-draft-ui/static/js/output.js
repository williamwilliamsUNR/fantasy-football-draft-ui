'use strict';

$(document).ready(function() {

});

$("#submit_output_file").click(function() {
    let fileNamePath = $("#output_file_path_name_input").val();

    let draftSettingsUpdated = function() {
        location.href = "/draftboard/round/next";
    }

    $.ajax({
        url: "/draftboard/output/generate", 
        contentType: "application/json",
        type: "POST",
        data: JSON.stringify({
            "file_path" : fileNamePath
        }),
        success: function() {
            $("#message").html(`SUCCESS: Output File Generated.`);
        },
        error: function(results) {
            $("#message").html(`ERROR: Output File Failed Generation ${results['message']}.`);
        }
    });
});
