from samplebase import SampleBase
from rgbmatrix import graphics, RGBMatrix
import time
import threading

# Load fonts
TeamNamefont = graphics.Font()
TeamNamefont.LoadFont("fonts/4x6.bdf")

Inningfont = graphics.Font()
Inningfont.LoadFont("fonts/6x12.bdf")

Scorefont = graphics.Font()
Scorefont.LoadFont("fonts/10x20.bdf")

# Global game object, and game over flag
game = None
endgame = False


# Helper function to get a valid integer input
def get_valid_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


# Function to return the current game
def return_game():
    return game


class Team:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.outs = 0


class SoftballGame:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.inning = 1
        self.at_bat = self.team2

    def switch_at_bat(self):
        self.at_bat = self.team2 if self.at_bat == self.team1 else self.team1
        self.at_bat.outs = 0

    def update_inning(self, change):
        self.inning = max(1, self.inning + change)

    def update_outs(self, team, change):
        team.outs = max(0, min(3, team.outs + change))

    def update_score(self, team, score_change):
        team.score += score_change

    def reset(self):
        self.inning = 1
        self.team1.score = 0
        self.team1.outs = 0
        self.team2.score = 0
        self.team2.outs = 0
        self.at_bat = self.team2

    def display_scoreboard(self):
        print("\n--- Softball Game Scoreboard ---")
        print(f"Inning: {self.inning}")
        print(
            f"  {self.team1.name:<15} {self.team1.score} runs | Outs: {self.team1.outs}"
        )
        print(
            f"  {self.team2.name:<15} {self.team2.score} runs | Outs: {self.team2.outs}"
        )
        print(f"At Bat: {self.at_bat.name}\n")

    def game_dict(self):
        return {
            "home": {
                "name": self.team1.name,
                "score": self.team1.score,
                "outs": self.team1.outs,
            },
            "away": {
                "name": self.team2.name,
                "score": self.team2.score,
                "outs": self.team2.outs,
            },
            "inning": self.inning,
            "atbat": self.at_bat.name,
        }


class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)

    def run(self):
        sb = self.matrix.CreateFrameCanvas()
        global game

        while True:
            if endgame:
                sb.Clear()
            else:
                sb.Clear()
                game_now = game

                # DRAW FRAME
                for x in range(0, sb.width):
                    sb.SetPixel(x, 0, 255, 0, 0)
                    sb.SetPixel(x, sb.height - 1, 255, 0, 0)

                for y in range(0, sb.height):
                    sb.SetPixel(0, y, 255, 0, 0)
                    sb.SetPixel(31, y, 255, 0, 0)
                    sb.SetPixel(32, y, 255, 0, 0)
                    sb.SetPixel(sb.width - 1, y, 255, 0, 0)

                for a in range(27, 38):
                    for b in range(0, 10):
                        sb.SetPixel(a, b, 0, 0, 0)

                # DRAWING TEAM NAMES
                red = graphics.Color(255, 0, 0)
                home_color = graphics.Color(255, 255, 255)
                away_color = graphics.Color(255, 255, 255)
                h1 = 255
                h2 = 255
                h3 = 255
                a1 = 255
                a2 = 255
                a3 = 255

                if (
                    game_now.team1.name == "MDXPS"
                    or game_now.team1.name == "MDEXPS"
                    or game_now.team1.name == "MARYLAND EXPRESS"
                    or game_now.team1.name == "MD XPS"
                    or game_now.team1.name == "MD EXPS"
                    or game_now.team1.name == "MD EXPRESS"
                ):
                    home_color = graphics.Color(0, 255, 0)
                    h1 = 0
                    h2 = 255
                    h3 = 0
                else:
                    away_color = graphics.Color(0, 255, 0)
                    a1 = 0
                    a2 = 255
                    a3 = 0

                graphics.DrawText(
                    sb, TeamNamefont, 1, 6, home_color, game_now.team1.name[:5]
                )  # home
                graphics.DrawText(
                    sb, TeamNamefont, 44, 6, away_color, game_now.team2.name[:5]
                )  # away

                # DRAWING INNINGS
                graphics.DrawText(sb, Inningfont, 30, 8, red, str(game_now.inning))

                # DRAWING SCORES
                graphics.DrawText(
                    sb, Scorefont, 3, 25, home_color, str(game_now.team1.score)
                )  # home
                graphics.DrawText(
                    sb, Scorefont, 43, 25, away_color, str(game_now.team2.score)
                )  # away

                if game_now.at_bat == game_now.team1:
                    # DRAWING OUTS HOME
                    graphics.DrawCircle(sb, 26, 3, 2, home_color)
                    graphics.DrawCircle(sb, 26, 9, 2, home_color)
                    graphics.DrawCircle(sb, 26, 15, 2, home_color)

                    if game_now.team1.outs > 0:
                        for o1x in range(25, 28):
                            for o1y in range(2, 5):
                                sb.SetPixel(o1x, o1y, h1, h2, h3)
                        if game_now.team1.outs > 1:
                            for o2x in range(25, 28):
                                for o2y in range(8, 11):
                                    sb.SetPixel(o2x, o2y, h1, h2, h3)
                            if game_now.team1.outs > 2:
                                for o3x in range(25, 28):
                                    for o3y in range(14, 17):
                                        sb.SetPixel(o3x, o3y, h1, h2, h3)
                else:
                    # DRAWING OUTS AWAY
                    graphics.DrawCircle(sb, 38, 3, 2, away_color)
                    graphics.DrawCircle(sb, 38, 9, 2, away_color)
                    graphics.DrawCircle(sb, 38, 15, 2, away_color)

                    if game_now.team2.outs > 0:
                        for o1x in range(37, 40):
                            for o1y in range(2, 5):
                                sb.SetPixel(o1x, o1y, a1, a2, a3)
                        if game_now.team2.outs > 1:
                            for o2x in range(37, 40):
                                for o2y in range(8, 11):
                                    sb.SetPixel(o2x, o2y, a1, a2, a3)
                            if game_now.team2.outs > 2:
                                for o3x in range(37, 40):
                                    for o3y in range(14, 17):
                                        sb.SetPixel(o3x, o3y, a1, a2, a3)
                sb = self.matrix.SwapOnVSync(sb)

    def endgame(self):
        sb = self.matrix.CreateFrameCanvas()
        sb.Clear()
        font = graphics.Font()
        font.LoadFont("fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = sb.width
        my_text = "Thank you for playing!"

        while True:
            sb.Clear()
            len = graphics.DrawText(sb, font, pos, 20, textColor, my_text)
            pos -= 1
            if pos + len < 0:
                pos = sb.width

            time.sleep(0.05)
            sb = self.matrix.SwapOnVSync(sb)


# Function to handle the game logic and user input
def play_game(game: SoftballGame):
    while True:
        game.display_scoreboard()
        print("Menu:")
        print("1. Update Inning")
        print("2. Switch At Bat Team")
        print(f"++HOME: {game.team1.name}++")
        print(f"3. Update {game.team1.name} Score")
        print(f"4. Update {game.team1.name} Outs")
        print(f"++AWAY: {game.team2.name}++")
        print(f"5. Update {game.team2.name} Score")
        print(f"6. Update {game.team2.name} Outs")
        print("7. Reset Game")
        print("0. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            change = get_valid_integer_input("Enter inning change (+/-): ")
            game.update_inning(change)
        elif choice == 2:
            game.switch_at_bat()
        elif choice == 3:
            score_change = get_valid_integer_input(
                f"Enter score change (+/-) for {game.team1.name}: "
            )
            game.update_score(game.team1, score_change)
        elif choice == 5:
            score_change = get_valid_integer_input(
                f"Enter score change (+/-) for {game.team2.name}: "
            )
            game.update_score(game.team2, score_change)
        elif choice == 4:
            outs_change = get_valid_integer_input(
                f"Enter outs change (+/-) for {game.team1.name}: "
            )
            game.update_outs(game.team1, outs_change)
        elif choice == 6:
            outs_change = get_valid_integer_input(
                f"Enter outs change (+/-) for {game.team2.name}: "
            )
            game.update_outs(game.team2, outs_change)
        elif choice == 7:
            game.reset()
        elif choice == 0:
            print("Exiting Game")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    # Initialize the board
    thisSB = SimpleSquare()

    # Initialize the game
    print("Enter New Game")
    team1_name = input("Home Team: ")
    team2_name = input("Away Team: ")
    team1 = Team(team1_name.upper())
    team2 = Team(team2_name.upper())
    game = SoftballGame(team1, team2)

    # Create threads for user input and scoreboard display
    display_process = threading.Thread(target=thisSB.process, args=())

    # Start the threads
    display_process.start()

    # Start User Input with game
    play_game(game)

    # End Game Message
    endgame = True
    thisSB.endgame()

    # Terminate the display thread
    display_process.join()
