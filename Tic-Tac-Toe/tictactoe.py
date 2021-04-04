def init_field():
    global game_matrix
    game_matrix = [["_"] * 3 for _ in range(3)]


def print_field():
    print("---------")
    for i in range(3):
        print("|", end=" ")
        for j in range(3):
            print(game_matrix[i][j], end=" ")
        print("|")
    print("---------")


def is_empty(x, y):
    return game_matrix[x][y] == "_"


def field_is_full():
    for i in range(3):
        for j in range(3):
            if is_empty(i, j):
                return False
    return True


def get_coordinates():
    while True:
        x, y = input("Enter the coordinates: ").split()
        if not (x.isnumeric() and y.isnumeric()):
            print("You should enter numbers!")
        elif int(x) < 1 or int(x) > 3 or int(y) < 1 or int(y) > 3:
            print("Coordinates should be from 1 to 3!")
        elif not is_empty(int(x) - 1, int(y) - 1):
            print("This cell is occupied! Choose another one!")
        else:
            return [int(x) - 1, int(y) - 1]


def game_ended():
    # Check for win in a row
    def win_in_row(char):
        for i in range(3):
            for j in range(3):
                if game_matrix[i][j] != char:
                    break
            else:
                return True
        return False

    # Check for win in a column
    def win_in_column(char):
        for i in range(3):
            for j in range(3):
                if game_matrix[j][i] != char:
                    break
            else:
                return True
        return False

    # Check for win in a diagonal
    def win_in_diagonal(char):
        for i in range(3):
            if game_matrix[i][i] != char:
                break
        else:
            return True

        for i in range(3):
            for j in range(3):
                if i + j == 2 and game_matrix[i][j] != char:
                    return False
        return True

    if any([win_in_row("X"), win_in_column("X"), win_in_diagonal("X")]):
        print("X wins")
        return True
    elif any([win_in_row("O"), win_in_column("O"), win_in_diagonal("O")]):
        print("O wins")
        return True
    elif field_is_full():
        print("Draw")
        return True
    else:
        return False


def move(coordinates, char):
    game_matrix[coordinates[0]][coordinates[1]] = char


def game():
    init_field()
    print_field()
    while True:
        move(get_coordinates(), "X")
        print_field()
        if game_ended():
            break
        move(get_coordinates(), "O")
        print_field()
        if game_ended():
            break


game_matrix = []
game()  # All functions together in an infinite loop
