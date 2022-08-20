from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
import json

draft_board = Blueprint('draft_board',
                         __name__, 
                        url_prefix="/draftboard",
                        template_folder='templates',
                        static_folder='static')

@draft_board.route('/initialize', methods=["POST"])
def initialize_draft_settings():
    session["draftboard"] = {}
    session["draftboard"]["settings"] = request.json
    session["draftboard"]["settings"]["current_round"] = 0
    session["draftboard"]["settings"]["ranking_scheme"] = "adp"
    session["draftboard"]["rounds"] = {}

    for i in range(1, int(session["draftboard"]["settings"]["number_rounds"]) + 1):
        session["draftboard"]["rounds"][i] = {
            "QB" : [],
            "RB" : [],
            "WR" : [],
            "TE" : []
        }

    return jsonify({"message" : "Draft Settings Initialized."}), 200


@draft_board.route('/round/next', methods=["GET"])
def next_round():
    session["draftboard"]["settings"]["current_round"] = session["draftboard"]["settings"]["current_round"] + 1
    session.modified = True

    if session["draftboard"]["settings"]["current_round"] > int(session["draftboard"]["settings"]["number_rounds"]):
        return redirect(url_for("draft_board.draft_planning_output"))

    return redirect(url_for("draft_board.draft_planning"))


@draft_board.route('/round/submit', methods=["POST"])
def submit_round_players():
    round_players = request.json
    current_round = str(session["draftboard"]["settings"]["current_round"])

    for player in round_players:
        if player["position"] in session["draftboard"]["rounds"][current_round]:
            session["draftboard"]["rounds"][current_round][player["position"]].append(player)

    session.modified = True
    return jsonify ({"message" : "Successfully Saved Round Selections."}), 200


@draft_board.route('/planning', methods=["GET"])
def draft_planning():
    return render_template("draft_planning.html", current_round=session["draftboard"]["settings"]["current_round"])


@draft_board.route('/output', methods=["GET"])
def draft_planning_output():
    return render_template("output.html")


@draft_board.route('/output/generate', methods=["POST"])
def draft_planning_output_generate():
    file_path = request.json["file_path"]
    
    try:
        with open(file_path, "w") as outfile:
            json.dump(session, outfile)

        return jsonify ({"message" : "Successfully Saved Round Selections."}), 200
    except Exception as ex:
        print(ex)
        return jsonify({"message" : str(ex)}), 400


