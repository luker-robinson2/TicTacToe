import random
import pickle
import os


if os.path.getsize('matchboxes.pkl') != 0:
    with open('matchboxes.pkl', 'rb') as rfp:
        matchboxes = pickle.load(rfp)


class Matchbox(object):
    def __init__(self, state):
        self.state = state
        self.next_moves = []
        for x in range(3):
            for y in range(3):
                if state[x][y] == 0:
                    self.next_moves.append((x, y))
        print("matchbox initialized")

    def losing_move(self, move, boxes, moves):
        self.next_moves.remove(move)
        if len(self.next_moves) == 0:
            matchboxes.remove(self)
            ind = boxes.index(self)
            boxes[ind - 1].losing_move(moves[ind - 1])

    def choose_move(self):
        return random.choice(self.next_moves)


def choose_move_big(state, boxes, moves, matchbox_list):
    print(state)
    print("len matchboxes:", len(matchbox_list))
    for matchbox in matchbox_list:
        if matchbox.state == state:
            print(matchbox_list[0].state)
            boxes.append(matchbox)
            move = matchbox.choose_move()
            moves.append(move)
            print("hit")
            return move

    new_matchbox = Matchbox(state)
    matchbox_list.append(new_matchbox)
    boxes.append(new_matchbox)
    move = new_matchbox.choose_move()
    moves.append(move)
    return move


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
