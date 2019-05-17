import tkinter as tk
import pickle
import os
import random

human = 1
computer = 2
side = "X"  # human letter (representation stays same for boards)
other_side = "O"
window = tk.Tk()
matchboxes = []
boxes = []
moves = []
start = False
button_list = []
Board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

# check if file exists
if os.path.getsize('matchboxes.pkl') != 0:
    with open('matchboxes.pkl', 'rb') as rfp:
        matchboxes = pickle.load(rfp)

# the main component, a matchbox is basically a state of the board paired
# with possible moves from the position. Each time the computer loses, it removes
# the move last move it made from next_moves. If there are no more moves left in
# next_moves, the move of the previous matchbox which made the move that would cause
# the state to be un-winnable.
class Matchbox(object):
    def __init__(self, state):
        self.state = state
        self.next_moves = []
        for x in range(3):
            for y in range(3):
                if state[x][y] == 0:
                    self.next_moves.append((x, y))
        print("matchbox initialized")

    def losing_move(self, move, box_list, move_list):
        self.next_moves.remove(move)
        if len(self.next_moves) == 0:
            matchboxes.remove(self)
            ind = box_list.index(self)
            box_list[ind - 1].losing_move(move_list[ind - 1])

    def choose_move(self):
        return random.choice(self.next_moves)

# large overarching function to make a move
def choose_move_big(the_board, box_list, move_list, matchbox_list):
    for matchbox in matchbox_list:
        if matchbox.state == the_board:
            print("matchbox matches")
            print("the_board is", the_board)
            print("matchbox.state is", matchbox.state)
            box_list.append(matchbox)
            move = matchbox.choose_move()
            move_list.append(move)
            return move
    new_matchbox = Matchbox(the_board)
    matchbox_list.append(new_matchbox)
    box_list.append(new_matchbox)
    move = new_matchbox.choose_move()
    move_list.append(move)
    return move

# function to check if the game is over
def end(board):
    for x in range(3):
        if (board[x][0] == (board[x][1]) & (board[x][2])) & (board[x][0] != 0):
            return True
        elif (board[0][x] == (board[1][x]) & (board[2][x])) & (board[0][x] != 0):
            return True
    if (board[0][0] == (board[1][1]) & (board[2][2])) & (board[0][0] != 0):
            return True
    elif (board[2][0] == (board[1][1]) & (board[0][2])) & (board[2][0] != 0):
            return True
    else:
        return False

# function for changing who starts game, not implemented yet
def choose(state):
    global start
    start = state  # false means human start, true means computer

# function for computer to make a move
def computer_make_move():
    print('length of matchboxes', len(matchboxes))
    move = choose_move_big(Board, boxes, moves, matchboxes)
    Board[move[0]][move[1]] = computer
    poss = ((move[0]) * 3) + (move[1] + 1)
    button_list[poss - 1] = tk.Label(text=other_side)
    button_list[poss - 1].grid(row=move[0] + 1, column=move[1], sticky="nsew", padx=4, pady=4)
    if end(Board):
        window.destroy()
        with open('matchboxes.pkl', 'wb') as wfp:
            pickle.dump(matchboxes, wfp, pickle.HIGHEST_PROTOCOL)
        print("game over")
        print("computer wins")

# function for making a move based on human input
def human_make_move(position, number):
    global Board
    x, y = position
    Board[x][y] = human
    button_list[number - 1] = tk.Label(text=side)
    button_list[number - 1].grid(row=x + 1, column=y, sticky="nsew", padx=4, pady=4)
    if end(Board):
        boxes[-1].losing_move(moves[-1], boxes, moves)
        window.destroy()
        with open('matchboxes.pkl', 'wb') as wfp:
            pickle.dump(matchboxes, wfp, pickle.HIGHEST_PROTOCOL)
        print("game over")
        print("human wins")
    else:
        computer_make_move()

# Everything here and below has to do with the GUI
# each button calls the human_make_move function with it's coordinates as parameters
window.title("A semi-beatable ai until it isn't")
window.configure(bg="white")

start_button_computer = tk.Button(window, text="computer start", command=lambda: choose(True), bg="white")
button1 = tk.Button(window, command=lambda: human_make_move((0, 0), 1), width=10, height=5)
button_list.append(button1)
button2 = tk.Button(window, command=lambda: human_make_move((0, 1), 2), width=10, height=5)
button_list.append(button2)
button3 = tk.Button(window, command=lambda: human_make_move((0, 2), 3), width=10, height=5)
button_list.append(button3)
button4 = tk.Button(window, command=lambda: human_make_move((1, 0), 4), width=10, height=5)
button_list.append(button4)
button5 = tk.Button(window, command=lambda: human_make_move((1, 1), 5), width=10, height=5)
button_list.append(button5)
button6 = tk.Button(window, command=lambda: human_make_move((1, 2), 6), width=10, height=5)
button_list.append(button6)
button7 = tk.Button(window, command=lambda: human_make_move((2, 0), 7), width=10, height=5)
button_list.append(button7)
button8 = tk.Button(window, command=lambda: human_make_move((2, 1), 8), width=10, height=5)
button_list.append(button8)
button9 = tk.Button(window, command=lambda: human_make_move((2, 2), 9), width=10, height=5)
button_list.append(button9)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
start_button_computer.grid(row=0, column=0, columnspan=3)
button1.grid(row=1, column=0, sticky="nsew", padx=4, pady=4)
button2.grid(row=1, column=1, sticky="nsew", padx=4, pady=4)
button3.grid(row=1, column=2, sticky="nsew", padx=4, pady=4)
button4.grid(row=2, column=0, sticky="nsew", padx=4, pady=4)
button5.grid(row=2, column=1, sticky="nsew", padx=4, pady=4)
button6.grid(row=2, column=2, sticky="nsew", padx=4, pady=4)
button7.grid(row=3, column=0, sticky="nsew", padx=4, pady=4)
button8.grid(row=3, column=1, sticky="nsew", padx=4, pady=4)
button9.grid(row=3, column=2, sticky="nsew", padx=4, pady=4)

tk.mainloop()
