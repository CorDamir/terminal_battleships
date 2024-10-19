import random

game_message = {
    "computer": "",
    "player": "",
    }

class Board():
    def __init__(self, size, player):
        self.size = size
        self.battleships = int(size * size / 5)
        self.name = player
        self.current_status = []

        for row in range(size):
            self.current_status.append(["*" for i in range(size)])

    def draw_self(self):
        """
        Draws a numbered grid representation of current board status
        """
        for i in range(self.size + 1):
            print(f" {i} ", end = "")
        
        print()
        
        for i in range(self.size +1):
            print("===", end = "")

        print()

        y = 1
        for row in self.current_status:
            print(f" {y}|", end = "")
            for field in row:
                print(f" {field} ", end="")
            print()
            y += 1

    def randomize_battleship_locations(self):
        """
        Puts battleships to random locations on board
        """
        ships_left_to_assign = self.battleships
        
        while(ships_left_to_assign):
            row = random.randint(0, self.size - 1)
            column = random.randint(0, self.size - 1)
            
            if self.current_status[row][column] == "*":
                self.current_status[row][column] = "O"
                ships_left_to_assign -= 1

def draw_game_status():
    """
    Clears screen then draws player and computer boards on it
    """
    print("\033c", end = "")
    players_board.draw_self()
    print()
    computers_board.draw_self()
    print()

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
            game_message["player"] = f"You destroyed enemy battleship at ({row+1}, {column+1}) coordinates!"
            return True

        case "X" | "-":
            game_message["player"] = f"You already hit ({row+1}, {column+1}) coordinates. Try again.\n"
            game_message["computer"] = ""
            return False
        
        case "*":
            computers_board.current_status[row][column] = "-"
            game_message["player"] = f"No enemy battleships at ({row+1}, {column+1}) coordinates. A miss!"
            return True

def computer_guess():
    """
    Makes a random non-repeated guess and adjusts the board
    status accordingly
    """
    while(True):
        row_guess = random.randint(0, computers_board.size - 1)
        column_guess = random.randint(0, computers_board.size - 1)

        match players_board.current_status[row_guess][column_guess]:
            case "O":
                players_board.current_status[row_guess][column_guess] = "X"
                players_board.battleships -= 1
                game_message["computer"] = f"Computer destroyed your battleship at ({row_guess}, {column_guess}) coordinates!"
                return

            case "*":
                players_board.current_status[row_guess][column_guess] = "-"
                game_message["computer"] = f"Computer missed at ({row_guess + 1}, {column_guess + 1}) coordinates!"
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

    try: #convert user input to integers
        row_guess = int(row_guess) - 1
        column_guess = int(column_guess) - 1

    except: #display try again message to player if not integers
        game_message["player"] = "Row and Column must be single numbers. Try again.\n"
        game_message["computer"] = ""

    else:  #otherwise check if input is within board limits
        if column_guess >= 0 and column_guess < players_board.size and row_guess >= 0 and row_guess < players_board.size:
            #within limits: execute user input handling function
            return handle_user_guess(row_guess, column_guess) #return handling functions result
        else: #outside limits: display a try again message to user
            game_message["player"] = "That hit would be outside the battlefield. Try again.\n"
            game_message["computer"] = ""

    return False  

#BASE CODE BEGINS HERE
print("\033c", end = "")
name = input("Your game tag:\n")

players_board = Board(5, name)
computers_board = Board(5, "Computer")

players_board.randomize_battleship_locations()
computers_board.randomize_battleship_locations()

while(True):
    """ Game loop """
    draw_game_status()

    print(f"{players_board.name}: {players_board.battleships}    Computer: {computers_board.battleships}\n")

    if game_message["player"]:
        print(f"{game_message["player"]}")
    if game_message["computer"]:
        print(f"{game_message["computer"]}\n")

    print("Where could the enemy battleship be?")

    if get_user_guess(): #if user guess is validated and not repeated continue with game
        computer_guess()
    