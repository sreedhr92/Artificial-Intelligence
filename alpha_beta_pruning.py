import copy
import itertools
import random
from collections import namedtuple

import numpy as np
GameState = namedtuple('GameState', ['to_move', 'utility', 'board', 'moves'])
class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [(x, y) for x in range(1, h + 1)
                 for y in range(1, v + 1)]
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(
                             board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n >= self.k

def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search apps here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth >
                                   d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action

app = TicTacToe()
state = app.initial
flag=0
while True:
    print("User input: Pick an available move")
    for i,j in enumerate(state.moves):
        print(i+1,j)
    moves = state.moves
    x = int(input("Enter the value :"))
    next_move = moves[x-1]
    next_state = app.result(state,next_move)
    app.display(next_state)
    state = next_state
    print()
    if app.terminal_test(state) == True and state.utility == 0:
        print("Draw")
        break
    elif app.terminal_test(state) == True and state.utility == 1:
        print("Player wins")
        break
    print("Now the computer plays :")
    best = alpha_beta_cutoff_search(state,app)
    next_state = app.result(state,best)
    app.display(next_state)
    print()
    if app.terminal_test(next_state) == True and next_state.utility == 0:
        print("Draw")
        break
    elif app.terminal_test(next_state) == True and next_state.utility == -1:
        print("computer wins")
        break
    state = next_state

'''Output:
-----------Case 1-----------------

User input: Pick an available move
1 (1, 1)
2 (1, 2)
3 (1, 3)
4 (2, 1)
5 (2, 2)
6 (2, 3)
7 (3, 1)
8 (3, 2)
9 (3, 3)
Enter the value :5
. . . 
. X . 
. . .

Now the computer plays :
O . . 
. X .
. . .

User input: Pick an available move
1 (1, 2)
2 (1, 3)
3 (2, 1)
4 (2, 3)
5 (3, 1)
6 (3, 2)
7 (3, 3)
Enter the value :5
O . . 
. X .
X . . 

Now the computer plays :
O . O
. X .
X . .

User input: Pick an available move
1 (1, 2)
2 (2, 1)
3 (2, 3)
4 (3, 2)
5 (3, 3)
Enter the value :1
O X O 
. X .
X . . 

Now the computer plays :
O X O
. X .
X O .

User input: Pick an available move
1 (2, 1)
2 (2, 3)
3 (3, 3)
Enter the value :3
O X O
. X .
X O X

Now the computer plays :
O X O
O X .
X O X

User input: Pick an available move
1 (2, 3)
Enter the value :1
O X O
O X X
X O X

Draw

-------Case 2--------------------
User input: Pick an available move
1 (1, 1)
2 (1, 2)
3 (1, 3)
4 (2, 1)
5 (2, 2)
6 (2, 3)
7 (3, 1)
8 (3, 2)
9 (3, 3)
Enter the value :6
. . . 
. . X 
. . .

Now the computer plays :
O . . 
. . X
. . .

User input: Pick an available move
1 (1, 2)
2 (1, 3)
3 (2, 1)
4 (2, 2)
5 (3, 1)
6 (3, 2)
7 (3, 3)
Enter the value :2
O . X 
. . X 
. . .

Now the computer plays :
O O X 
. . X
. . .

User input: Pick an available move
1 (2, 1)
2 (2, 2)
3 (3, 1)
4 (3, 2)
5 (3, 3)
Enter the value :2
O O X
. X X
. . .

Now the computer plays :
O O X
O X X
. . .

User input: Pick an available move
1 (3, 1)
2 (3, 2)
3 (3, 3)
Enter the value :1
O O X
O X X
X . .

Player wins

--------------case 3------------------
User input: Pick an available move
1 (1, 1)
2 (1, 2)
3 (1, 3)
4 (2, 1)
5 (2, 2)
6 (2, 3)
7 (3, 1)
8 (3, 2)
9 (3, 3)
Enter the value :8
. . . 
. . .
. X .

Now the computer plays :
O . . 
. . .
. X .

User input: Pick an available move
1 (1, 2)
2 (1, 3)
3 (2, 1)
4 (2, 2)
5 (2, 3)
6 (3, 1)
7 (3, 3)
Enter the value :1
O X . 
. . .
. X .

Now the computer plays :
O X . 
. O .
. X .

User input: Pick an available move
1 (1, 3)
2 (2, 1)
3 (2, 3)
4 (3, 1)
5 (3, 3)
Enter the value :5
O X .
. O .
. X X

Now the computer plays :
O X .
. O .
O X X

User input: Pick an available move
1 (1, 3)
2 (2, 1)
3 (2, 3)
Enter the value :1
O X X
. O .
O X X

Now the computer plays :
O X X
O O .
O X X

computer wins
'''