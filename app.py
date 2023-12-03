import os
import sys
import threading
from flask import Flask, render_template
from Scoreboardv6 import SimpleSquare, Team, SoftballGame


# --------------------------
print("Enter New Game")
# get game details
if not os.path.exists("game.txt"):
    print("Game settings file doesn't exist.")
    # get team as input
    home_team = input("Home Team: ")
    away_team = input("Away Team: ")
else:
    try:
        with open("game.txt") as game_file:
            teams = game_file.readlines()
            home_team = teams[0].split(":")[-1].removesuffix("\n")
            away_team = teams[1].split(":")[-1].removesuffix("\n")
    except:
        print("Error reading game file. Please reformat and try again.")
        sys.exit(1)


# Initialize the game
sb = SimpleSquare()
home_team = Team(home_team)
away_team = Team(away_team)
game = SoftballGame(home_team, away_team)
endgame = False

# Create threads for user input and scoreboard display
display_process = threading.Thread(target=sb.process, args=())

# Start the threads
display_process.start()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", game=game.game_dict())


@app.route("/<team>/<action>/<change>")
def action(team, action, change):
    if team == "none":
        # Check for endgame
        if action == "none":
            if change == "none":
                # call endgame
                endgame = threading.Thread(target=sb.endgame)
                endgame.start()
                return render_template("index.html", game=game.game_dict())
        if action == "inning":
            change = int(change)
            game.update_inning(change)
        elif action == "atbat":
            game.switch_at_bat()
        elif action == "clear":
            game.reset()
    else:
        change = int(change)
        team = game.team1 if game.team1.name == team else game.team2
        if action == "score":
            game.update_score(team, change)
        elif action == "outs":
            game.update_outs(team, change)

    return render_template("index.html", game=game.game_dict())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
