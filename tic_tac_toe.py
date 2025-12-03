import os
import time
import json
import random

# --------------------------------------
# AI MEMORY (Load if exists)
# --------------------------------------

STATE_FILE = "state_value.json"

try:
    with open(STATE_FILE, "r") as f:
        state_value = json.load(f)
    print("Loaded AI memory from state_value.json")
except:
    state_value = {}
    print("No previous AI memory. Starting fresh.")

last_states = []
LEARNING_RATE = 0.3
DISCOUNT = 0.9


# --------------------------------------
# Save Learning
# --------------------------------------

def save_learning():
    with open(STATE_FILE, "w") as f:
        json.dump(state_value, f)
    # print("AI memory saved.")


# --------------------------------------
# Basic Game Functions
# --------------------------------------

board = [' ' for _ in range(10)]

def insertLetter(letter, pos):
    if pos in range(1, 10):
        board[pos] = letter

def spaceIsFree(pos):
    return board[pos] == ' '

def printBoard(board):
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')

def isWinner(bo, le):
    return (bo[7]==le and bo[8]==le and bo[9]==le) or \
           (bo[4]==le and bo[5]==le and bo[6]==le) or \
           (bo[1]==le and bo[2]==le and bo[3]==le) or \
           (bo[1]==le and bo[4]==le and bo[7]==le) or \
           (bo[2]==le and bo[5]==le and bo[8]==le) or \
           (bo[3]==le and bo[6]==le and bo[9]==le) or \
           (bo[1]==le and bo[5]==le and bo[9]==le) or \
           (bo[3]==le and bo[5]==le and bo[7]==le)

def isBoardFull(board):
    return board.count(' ') <= 1


# --------------------------------------
# Quit Anytime
# --------------------------------------

def force_quit(user_input):
    if user_input.lower() in ["q", "quit", "exit"]:
        print("Exiting game...")
        save_learning()
        exit()


# --------------------------------------
# Player Move
# --------------------------------------

def playerMove(name):
    while True:
        move = input(f"{name}, choose position (1-9) or Q to quit: ")
        force_quit(move)

        try:
            move = int(move)
            if move in range(1,10):
                if spaceIsFree(move):
                    insertLetter('X', move)
                    return
                else:
                    print("That space is occupied.")
            else:
                print("Enter a number 1-9.")
        except:
            print("Invalid input.")


# --------------------------------------
# simple Move
# --------------------------------------
def compMove():
    possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
    move = 0

    for let in ['O', 'X']:
        for i in possibleMoves:
            boardCopy = board[:]
            boardCopy[i] = let
            if isWinner(boardCopy, let):
                move = i
                return move

    cornersOpen = []
    for i in possibleMoves:
        if i in [1,3,7,9]:
            cornersOpen.append(i)
            
    if len(cornersOpen) > 0:
        move = selectRandom(cornersOpen)
        return move

    if 5 in possibleMoves:
        move = 5
        return move

    edgesOpen = []
    for i in possibleMoves:
        if i in [2,4,6,8]:
            edgesOpen.append(i)
            
    if len(edgesOpen) > 0:
        move = selectRandom(edgesOpen)
        
    return move

def selectRandom(li):
    import random
    ln = len(li)
    r = random.randrange(0,ln)
    return li[r]
    
# --------------------------------------
# RL Move
# --------------------------------------

def compMove_RL():
    best_value = -999
    best_move = 0

    for pos in range(1, 10):
        if spaceIsFree(pos):
            copy_board = board.copy()
            copy_board[pos] = 'O'
            state = ''.join(copy_board)
            value = state_value.get(state, 0)

            if value > best_value:
                best_value = value
                best_move = pos

    if best_move == 0:
        moves = [i for i in range(1,10) if spaceIsFree(i)]
        best_move = random.choice(moves)

    # Track learning state
    new_state = board.copy()
    new_state[best_move] = 'O'
    last_states.append(''.join(new_state))

    return best_move


# --------------------------------------
# Reinforcement Learning Update
# --------------------------------------

def reinforce(result):
    reward = result

    for state in reversed(last_states):
        old = state_value.get(state, 0)
        new = old + LEARNING_RATE * (reward - old)
        state_value[state] = new
        reward = new * DISCOUNT

    last_states.clear()
    save_learning()


# --------------------------------------
# Self Training
# --------------------------------------

def self_play_training(games=10000):
    print(f"Loading. Please wait...")
    global board

    for _ in range(games):
        board = [' ' for _ in range(10)]

        while True:
            # O move (RL)
            move = compMove_RL()
            insertLetter('O', move)
            if isWinner(board, 'O'):
                reinforce(+1)
                break
            if isBoardFull(board):
                reinforce(0)
                break

            # X move (random)
            moves = [i for i in range(1,10) if spaceIsFree(i)]
            if not moves:
                reinforce(0)
                break

            x_move = random.choice(moves)
            insertLetter('X', x_move)

            if isWinner(board, 'X'):
                reinforce(-1)
                break

    print("Done..\n")


# --------------------------------------
# MINIMAX
# --------------------------------------

def minimax(board_state, depth, isMax):
    if isWinner(board_state, 'O'):
        return 10 - depth
    if isWinner(board_state, 'X'):
        return depth - 10
    if isBoardFull(board_state):
        return 0

    if isMax:
        best = -999
        for i in range(1, 10):
            if board_state[i] == ' ':
                board_state[i] = 'O'
                val = minimax(board_state, depth + 1, False)
                board_state[i] = ' '
                best = max(best, val)
        return best
    else:
        best = 999
        for i in range(1, 10):
            if board_state[i] == ' ':
                board_state[i] = 'X'
                val = minimax(board_state, depth + 1, True)
                board_state[i] = ' '
                best = min(best, val)
        return best


def compMove_minimax():
    best_score = -999
    best_move = 0

    for i in range(1, 10):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i

    return best_move


# --------------------------------------
# Main Game
# --------------------------------------

def main_loop(diff, name):
    global board

    printBoard(board)

    while True:

        # PLAYER MOVE
        if not isWinner(board, 'O'):
            playerMove(name)
            if isWinner(board, 'X'):
                os.system('cls')
                printBoard(board)
                print(f"{name}, you win!")
                reinforce(-1)
                return
        else:
            os.system('cls')
            printBoard(board)
            print("Computer wins!")
            reinforce(+1)
            return

        if isBoardFull(board):
            os.system('cls')
            printBoard(board)
            print("It's a tie!")
            reinforce(0)
            return

        print("\nComputer thinking...")
        time.sleep(0.5)

        # DIFFICULTY ROUTING
        if diff == "easy" or diff == "1":
            move = compMove_RL()


        elif diff == "medium" or diff == "2":
            move = compMove()

        elif diff == "hard" or diff == "3":
            move = compMove_minimax()

        else:
            move = self_play_training(20000)

        insertLetter('O', move)

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Computer placed O in {move} position.\n")
        printBoard(board)

        if isWinner(board, 'O'):
            print("Computer wins!")
            reinforce(+1)
            time.sleep(1)
            # os.system('cls')
            return

        if isBoardFull(board):
            print("It's a tie!")
            reinforce(0)
            time.sleep(1)
            # os.system('cls')
            return


# --------------------------------------
# Start Game
# --------------------------------------

def introduction():
    os.system('cls')
    print("Welcome to Tic Tac Toe!")
    name = input("Enter your name (or Q to quit): ")
    force_quit(name)
    return name


name = introduction()

while True:
    os.system('cls')
    diff = input("\nChoose difficulty:\n"
                 "1. Easy\n"
                 "2. Medium\n"
                 "3. Hard\n"
                 "Q. Quit\n")
    time.sleep(1)
    os.system('cls')
    force_quit(diff)
    diff = diff.strip().lower()

    if diff < "1" or diff > "3":
        self_play_training(50000)
        diff = "1"  # RL after training

    board = [' ' for _ in range(10)]
    main_loop(diff, name)

    again = input("\nPlay again? (Y/N): ")
    force_quit(again)

    if again.lower() not in ["y", "yes"]:
        break

save_learning()
