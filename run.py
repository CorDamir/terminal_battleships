class Board():
    def __init__(self, size, battleships, player):
        self.size = size
        self.battleships = battleships
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


name = input("Your game tag:\n")
players_board = Board(7, 5, name)
computers_board = Board(7, 5, "Computer")
print()
players_board.draw_self()
print()
computers_board.draw_self()
print()