# !/usr/bin/python3.6.7
# Sample starter bot by Zac Partrdige
# 06/04/19
# Feel free to use this and modify it however you wish

import socket
import sys
import numpy as np
from keras.models import load_model
import time

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
boards = np.zeros((10, 10), dtype="int8")
curr = 0 # this is the current board to play in

# print a row
# This is just ported from game.c
def print_board_row(board, a, b, c, i, j, k):
    # The marking script doesn't seem to like this either, so just take it out to submit
    print("", board[a][i], board[a][j], board[a][k], end = " | ")
    print(board[b][i], board[b][j], board[b][k], end = " | ")
    print(board[c][i], board[c][j], board[c][k])

# Print the entire board
# This is just ported from game.c
def print_board(board):
    print_board_row(board, 1,2,3,1,2,3)
    print_board_row(board, 1,2,3,4,5,6)
    print_board_row(board, 1,2,3,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 4,5,6,1,2,3)
    print_board_row(board, 4,5,6,4,5,6)
    print_board_row(board, 4,5,6,7,8,9)
    print(" ------+-------+------")
    print_board_row(board, 7,8,9,1,2,3)
    print_board_row(board, 7,8,9,4,5,6)
    print_board_row(board, 7,8,9,7,8,9)
    print()

def getState(board, curr):
    state = []

    for i in range(1,10):
        for j in range(1,10):
            state.append(board[i][j] / 2)

    state.append(curr / 9)
    state = np.asarray(state).reshape(1,len(state))
    return state

def legal(board, curr):
    legals = []
    count = 1

    for i in range(1,10):
            if board[curr][i] == 0:
                legals.append(count)
            count += 1

    return legals

# choose a move to play
def play():
    print_board(boards)
    print("Current Board: %d" % curr)

    model = load_model("TTTAgent.h5")
    legal_moves = legal(boards, curr)
    state = getState(boards, curr)
    Q_values = model.predict(state)
    print(Q_values)
    for i in range(Q_values.shape[1]):
        if (i+1) not in legal_moves:
            Q_values[0][i] = -10
    action = np.argmax(Q_values)
    print(Q_values)
    n = action + 1
    print("Legal Moves:", end = " ")
    print(legal_moves)
    print("Moved %d\n" % n)

    # print("playing", n)
    place(curr, n, 1) #plave(board, move, x/0)
    return n

# place a move in the global boards
def place(board, num, player):
    global curr
    curr = num
    boards[board][num] = player

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == "third_move":
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        return play()
    elif command == "next_move":
        place(curr, int(args[0]), 2)
        return play()
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())

if __name__ == "__main__":
    main()
