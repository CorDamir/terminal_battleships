"""Module for generating random numbers"""
import random


class Board():
    """
    Contains player name, field size, battleship number
    and status of all fields.
    """
    def __init__(self, size, player):
        self.size = size
        self.battleships = int(size * size / 5)
        self.name = player
        self.current_status = []

        for _ in range(size):
            self.current_status.append(["*" for i in range(size)])

        self.randomize_battleship_locations()

    def draw_self(self, hidden):
        """
        Draws a numbered grid representation of current board status
        With argument true hides battleship locations
        """
        for i in range(self.size + 1):
            print(f" {i} ", end="")

        print()

        for i in range(self.size + 1):
            print("===", end="")

        print()

        y = 1
        for row in self.current_status:
            print(f" {y}|", end="")
            for field in row:
                if hidden and field == "O":
                    print(" * ", end="")
                else:
                    print(f" {field} ", end="")
            print()
            y += 1

    def randomize_battleship_locations(self):
        """
        Puts battleships to random locations on board
        """
        ships_left_to_assign = self.battleships

        while ships_left_to_assign:
            row = random.randint(0, self.size - 1)
            column = random.randint(0, self.size - 1)

            if self.current_status[row][column] == "*":
                self.current_status[row][column] = "O"
                ships_left_to_assign -= 1


def draw_game_status():
    """
    Clears screen then draws player and computer boards
    and displays score
    """
    print("\033c", end="")
    players_board.draw_self(False)
    print()
    computers_board.draw_self(True)
    print()

    print(f"{players_board.name}: {players_board.battleships}    "
          f"Computer: {computers_board.battleships}\n")

    if game_message["player"]:
        print(f"{game_message["player"]}")
    if game_message["computer"]:
        print(f"{game_message["computer"]}\n")


def handle_user_guess(row, column):
    """
    Determines the outcome of user guess and changes current state of board
    accordingly. Sets an appropriate game message and score. Returns false
    if player input was a repeated guess
    """
    match computers_board.current_status[row][column]:
        case "O":
            computers_board.current_status[row][column] = "X"
            computers_board.battleships -= 1
            game_message["player"] = (f"You destroyed enemy battleship at "
                                      f"({row+1}, {column+1}) coordinates!")
            return True

        case "X" | "-":
            game_message["player"] = (f"You already hit ({row+1}, {column+1}) "
                                      f"coordinates. Try again.\n")
            game_message["computer"] = ""
            return False

        case "*":
            computers_board.current_status[row][column] = "-"
            game_message["player"] = (
                                f"No enemy battleships at "
                                f"({row+1}, {column+1}) coordinates. A miss!"
                                )
            return True


def computer_guess():
    """
    Makes a random non-repeated guess and adjusts the board
    status accordingly
    """
    while True:
        row_guess = random.randint(0, computers_board.size - 1)
        column_guess = random.randint(0, computers_board.size - 1)

        match players_board.current_status[row_guess][column_guess]:
            case "O":
                players_board.current_status[row_guess][column_guess] = "X"
                players_board.battleships -= 1
                game_message["computer"] = (
                                f"Computer destroyed your battleship "
                                f"at ({row_guess + 1}, {column_guess + 1})"
                                f" coordinates!"
                                )
                return

            case "*":
                players_board.current_status[row_guess][column_guess] = "-"
                game_message["computer"] = (
                            f"Computer missed at "
                            f"({row_guess + 1}, {column_guess + 1}) "
                            f"coordinates!"
                            )
                return

            case _:
                pass


def get_user_guess():
    """
    Gets user row and column input, validates input. Returns false on failed
    validation otherwise returns 'handle_user_guess' function result
    """
    row_guess = input("Row:\n")
    column_guess = input("Column:\n")

    try:
        # convert user input to integers
        row_guess = int(row_guess) - 1
        column_guess = int(column_guess) - 1

    except Exception:
        # display try again message to player if not integers
        game_message["player"] = (
            "Row and Column must be single numbers. Try again.\n"
            )
        game_message["computer"] = ""

    else:
        # otherwise check if input is within board limits
        if (
          0 <= column_guess < players_board.size and
          0 <= row_guess < players_board.size
          ):
            # within limits: execute user input handling function
            return handle_user_guess(row_guess, column_guess)

        # outside limits: display a try again message to user
        game_message["player"] = (
            "That hit would be outside the battlefield. Try again.\n"
            )
        game_message["computer"] = ""

    # if user input not validated return false to loop user input
    return False


def end_game(player_won):
    """
    Clears screen then displays defeated players board
    and declares a winner. Use True argument for player win and
    false for computer win
    """
    print("\033c", end="")
    if player_won:
        computers_board.draw_self(False)
        print(f"\nCongratulations {players_board.name}, you WON!\n")
    else:
        players_board.draw_self(False)
        print("\nComputer wins this one.\n")

    input("Press enter to reset...")
    main()


def display_welcome_screen():
    """
    Displays simple instructons before
    the game start
    """
    print("\033c", end="")

    print(
        "\tWelcome to Battleships game!\n\n"
        "After you enter your game tag, your battle board will be\n"
        "displayed first and computers second with following logic:\n\n"
        "'*' - unchecked field\n"
        "'O' - field with your battleship\n"
        "'X' - field with a destroyed battleship\n"
        "'-' - checked empty field\n\n"
        "Below the battle boards you will see remaining battleships\n"
        "for yourself and computer.\n\n"
        "Enter numbers of row and column for the field you wish to\n"
        "check and the result will be displayed both on the battlefield\n"
        "and in text below. Destroy computers battleships before yours\n"
        "are destroyed and win!\n\n"
        "Ctrl+c if you wish to stop game.\n"
        )

    if game_message["player"]:
        print(game_message["player"])


def game_loop():
    """Game loop"""
    while True:
        draw_game_status()

        if get_user_guess():
            # if user guess is validated and not repeated continue with game
            if not computers_board.battleships:
                # if player won the game
                end_game(True)

            computer_guess()

            if not players_board.battleships:
                # if computer won the game
                end_game(False)


def main():
    """
    Sets initial values, gets user tag and calls game loop
    """
    global players_board
    global computers_board
    global game_message

    game_message = {
        "computer": "",
        "player": "",
    }

    while True:
        display_welcome_screen()
        name = input("Your game tag (3-12):\n")

        if (len(name) > 12 or len(name) < 3):
            game_message["player"] = "Game tag should be 3-12 characters long"
        else:
            game_message["player"] = ""
            break

    players_board = Board(5, name)
    computers_board = Board(5, "Computer")

    game_loop()


main()
