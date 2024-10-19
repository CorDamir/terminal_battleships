import random

class Board():
    def __init__(self, size, player):
        self.size = size
        self.battleships = int(size * size / 5)
        self.player = player
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
            row = random.randint(0, 4)
            column = random.randint(0, 4)
            if self.current_status[row][column] == "*":
                self.current_status[row][column] = "O"
                ships_left_to_assign -= 1

name = input("Your game tag:\n")
players_board = Board(7, name)
computers_board = Board(7, "Computer")
players_board.randomize_battleship_locations()
computers_board.randomize_battleship_locations()

def temp_print_test():
    print()
    players_board.draw_self()
    print()
    computers_board.draw_self()
    print()

temp_print_test()