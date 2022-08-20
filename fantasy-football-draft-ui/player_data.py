from flask import Blueprint, render_template, current_app, jsonify, session
import json

player_data = Blueprint('player_data',
                         __name__, 
                        url_prefix="/api/v1/players")

@player_data.route('/', methods=['GET'])
def get_all_players():
    try:
        players = {}
        with open(current_app.config["PLAYER_DATA_PATH"]) as player_file:
            players = json.load(player_file)

        return jsonify(players), 200
    except Exception as ex:
        return jsonify(str(ex)), 400

@player_data.route('/round', methods=['GET'])
def get_players_for_round():
    try:
        players = {}
        with open(current_app.config["PLAYER_DATA_PATH"]) as player_file:
            players = json.load(player_file)

        # This value will return some players before your pick that may fall to you in that round.
        NUMBER_PLAYERS_BEFORE_EXPECTED = 10
        # This value should be up until your next pick if they pick purely auto ADP.
        NUMBER_PLAYERS_AFTER_EXPECTED = session["draftboard"]["settings"]["number_players"] * 2
        # Starting Value to return players rankings for.
        STARTING_RANKING = (session["draftboard"]["settings"]["draft_position"] * session["draftboard"]["settings"]["current_round"]) - NUMBER_PLAYERS_BEFORE_EXPECTED
        # Ending Value to return players rankings for.
        ENDING_RANKING = (session["draftboard"]["settings"]["draft_position"] * session["draftboard"]["settings"]["current_round"]) + NUMBER_PLAYERS_AFTER_EXPECTED

        round_players = []
        for p in players:
            if players[p]["adp"] >= STARTING_RANKING and players[p]["adp"] <= ENDING_RANKING:
                round_players.append(players[p])

        return jsonify(round_players), 200
    except Exception as ex:
        print(ex)
        return jsonify(str(ex)), 400