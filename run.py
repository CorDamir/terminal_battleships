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
        ships_left_to_assign = self.battleships
        
        while(ships_left_to_assign):
            row = random.randint(0, self.size - 1)
            column = random.randint(0, self.size - 1)
            
            if self.current_status[row][column] == "*":
                self.current_status[row][column] = "O"
                ships_left_to_assign -= 1

def draw_game_status():
    print("\033c")
    players_board.draw_self()
    print()
    computers_board.draw_self()
    print()

def handle_user_guess(row, column):

    match computers_board.current_status[row][column]:
        case "O":
            computers_board.current_status[row][column] = "X"
            game_message["player"] = f"You destroyed enemy battleship at ({row+1}, {column+1}) coordinates!"
            return True

        case "X" | "-":
            game_message["player"] = f"You already hit ({row+1}, {column+1}) coordinates. Try again."
            return False
        
        case "*":
            computers_board.current_status[row][column] = "-"
            game_message["player"] = f"No enemy battleships on ({row+1}, {column+1}) coordinates. A miss!"
            return True

#BASE CODE BEGINS HERE
name = input("Your game tag:\n")

players_board = Board(7, name)
computers_board = Board(7, "Computer")

players_board.randomize_battleship_locations()
computers_board.randomize_battleship_locations()

while(True):
    draw_game_status()

    print(f"Remaining battleships for {players_board.name}: {players_board.battleships}")
    print(f"Remaining battleships for Computer: {computers_board.battleships}\n")

    print(f"{game_message["player"]}\n")
    print(f"{game_message["computer"]}\n")

    print("Where could the enemy battleship be?")
    
    row_guess = input("Row:\n")
    column_guess = input("Column:\n")
    handle_user_guess(int(row_guess)-1, int(column_guess)-1)