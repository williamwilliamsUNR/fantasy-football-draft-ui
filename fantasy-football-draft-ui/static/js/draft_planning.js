'use strict';
let playerTable = null;

$(document).ready(function() {
    playerTable = $('#player_table').DataTable({
        "columns" : [
            { "data": "adp"},
            { "data": "name"},
            { "data": "position"},
            { "data": "depth_order"},
            { "data": "team"},
            { "data": "bye"},
            { "data": "adp_formatted"},
            { "data": "rank"},
            { "data": "andy"},
            { "data": "jason"},
            { "data": "mike"},
            { "data": "high"},
            { "data": "low"}
        ]
});
    populateTable();
});


$('#player_table tbody').on('click', 'tr', function () {
    $(this).toggleClass('selected');
});


$('#submit_round_selection').click(function () {
    let playersSubmitted = function() {
        location.href = "/draftboard/round/next";
    }

    $.ajax({
        url: "/draftboard/round/submit", 
        contentType: "application/json",
        type: "POST",
        data: JSON.stringify(playerTable.rows('.selected').data().toArray()),
        success: playersSubmitted,
        error: function() {
            console.log(`ERROR: Saving player selections failed.`);
            return;
        }
    });
});


function populateTable() {
    let roundPlayersRetrieved = function(players) {
        for (let p of players) {
            for (let key of ["adp","name","position","depth_order","team","bye","adp_formatted","rank","andy","jason","mike","high","low"]) {
                if (!Object.keys(p).includes(key)) {
                    p[key] = "";
                }
            }
            
        }

        playerTable.rows.add(players).draw();
    }

    $.ajax({
        url: `/api/v1/players/round`, 
        contentType: "application/json",
        type: "GET",
        success: roundPlayersRetrieved,
        error: function() {
            console.log(`An error occured getting player data for round ${current_round}.`);
            return;
        }
    });
}