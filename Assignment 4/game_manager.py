from copy import deepcopy
from player import HumanPlayer
import game_rules

# Game state constants
AWAITING_INITIAL_X = -1
AWAITING_INITIAL_O = 0
X_TURN = 1
O_TURN = 2
X_VICTORY = 3
O_VICTORY = 4

class GameManager:
    def __init__(self, rows, cols, player1, player2, verbose=False):
        self.rows,self.cols = rows, cols
        self.p1, self.p2 = player1, player2
        self.verbose = verbose

        self.reset()

    def reset(self):
        self.turn_number = 1
        self.state = AWAITING_INITIAL_X
        self.board = game_rules.makeBoard(self.rows, self.cols)

    def interrupt(self, a, b):
        import sys
        sys.exit(1)

    def play(self):
        while self.state is not X_VICTORY and self.state is not O_VICTORY:
            self._takeTurn()
            if self.verbose: game_rules.printBoard(self.board)

    def GetTurn(self):
        if self.state == AWAITING_INITIAL_X or self.state == X_TURN: return self.p1.symbol
        if self.state == AWAITING_INITIAL_O or self.state == O_TURN: return self.p2.symbol
        if self.state == X_VICTORY or self.state == O_VICTORY: return ''

    def GetWinner(self):
        if self.state < 3: return None
        return 'X' if self.state == X_VICTORY else 'O'

    def _takeTurn(self, move_pair=None):
        playerBoard = deepcopy(self.board)
        old = self.state

        if len(game_rules.getLegalMoves(self.board, self.GetTurn())) < 1:
            if self.state == X_TURN: self.state = O_VICTORY
            if self.state == O_TURN: self.state = X_VICTORY
            return

        if self.state   == AWAITING_INITIAL_X: self._handleInitialX(playerBoard, self.board, move_pair)
        elif self.state == AWAITING_INITIAL_O: self._handleInitialO(playerBoard, self.board, move_pair)
        elif self.state == X_TURN: self._handleTurnX(playerBoard, self.board, move_pair)
        elif self.state == O_TURN: self._handleTurnO(playerBoard, self.board, move_pair)
        if self.state != old: self.turn_number += 1

    def _handleInitialX(self, playerBoard, board, move_pair):
        move = move_pair[0] if isinstance(self.p1, HumanPlayer) else self.p1.selectInitialX(playerBoard)
        if move in game_rules.getFirstMovesForX(board):
            self.board[move[0]][move[1]] = " "
            self.state = AWAITING_INITIAL_O

    def _handleInitialO(self, playerBoard, board, move_pair):
        move = move_pair[0] if isinstance(self.p2, HumanPlayer) else self.p2.selectInitialO(playerBoard)

        if move in game_rules.getFirstMovesForO(board):
            self.board[move[0]][move[1]] = " "
            self.state = X_TURN

    def _handleTurnX(self, playerBoard, board, move_pair):
        move = move_pair if isinstance(self.p1, HumanPlayer) else self.p1.getMove(playerBoard)
        if not move: self.state = O_VICTORY
        elif game_rules.isLegalMove(board, 'x', move, False):
            self.board = game_rules.makeMove(board, move)
            self.state = O_TURN

    def _handleTurnO(self, playerBoard, board, move_pair):
        move = move_pair if isinstance(self.p2, HumanPlayer) else self.p2.getMove(playerBoard)
        if not move: self.state = X_VICTORY
        elif game_rules.isLegalMove(board, 'o', move, False):
            self.board = game_rules.makeMove(board, move)
            self.state = X_TURN
