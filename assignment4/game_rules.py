from copy import deepcopy
import math

def makeBoard(rows, cols):
    return [['x' if (r+c)%2 == 0 else 'o' for c in range(cols)] for r in range(rows)]

def makeMove(board, move):
    return makePlayerMove(board, pieceAt(board, move[0]), move)

def makePlayerMove(board, player, move):
    if isLegalMove(board, player, move):
        newBoard = deepcopy(board)
        for jump in interpolateMove(move):
            _makeJump(newBoard, jump)
        return newBoard
    else:
        return board

def _makeJump(board, jump):
    mid = midPoint(jump)
    board[mid[0]][mid[1]] = " "
    board[jump[1][0]][jump[1][1]] = board[jump[0][0]][jump[0][1]]
    board[jump[0][0]][jump[0][1]] = " "

def moveLength(move):
    return abs(move[0][0] - move[1][0]) if verticalMove(move) else abs(move[0][1] - move[1][1])

def isLegalMove(board, player, move, loud=True):
    if not onBoard(len(board), len(board[0]), move[1]):
        if loud:
            print("Pieces must stay on the board")
        return False
    if pieceAt(board, move[0]) != player:
        if loud:
            print("You can only move your own pieces")
        return False
    length = moveLength(move)
    if length % 2 == 1:
        if loud:
            print("Cannot move an odd number of squares")
        return False
    if length == 0:
        if loud:
            print("Cannot stay put")
        return False
    other = 'o' if player == 'x' else 'x'
    hasJumped = False
    for jump in interpolateMove(move):
        if not isLegalJump(board, player, other, jump):
            if loud:
                print("Illegal move")
            return False
        board = deepcopy(board)
        _makeJump(board, jump)
        hasJumped = True
    return hasJumped

def isLegalJump(board, player, other, jump):
    return pieceAt(board, jump[0]) == player and pieceAt(board, midPoint(jump)) == other and pieceAt(board, jump[1]) == " "

def isInitialMove(board):
    return countPieces(board, ' ') < 2

def countPieces(board, piece):
    return sum([sum([1 if c == piece else 0 for c in row]) for row in board])

def interpolateMove(move):
    points = []
    if horizontalMove(move):
        step = 2 if move[0][1] < move[1][1] else -2
        points = [(move[0][0], c) for c in range(move[0][1], move[1][1] + step, step)]
    elif verticalMove(move):
        step = 2 if move[0][0] < move[1][0] else -2
        points = [(r, move[0][1]) for r in range(move[0][0], move[1][0] + step, step)]
    else: return []
    
    return zip(points, points[1:])

def midPoint(move):
    if horizontalMove(move): return (move[0][0], int((move[0][1] + move[1][1])/2))
    elif verticalMove(move): return (int((move[0][0] + move[1][0])/2), move[0][1])
    else: print("Cannot move diagonally")

def horizontalMove(move):
    return move[0][0] == move[1][0]

def verticalMove(move):
    return move[0][1] == move[1][1]

def pieceAt(board, point):
    return board[point[0]][point[1]]

def onBoard(rows, cols, point):
    return 0 <= point[0] and point[0] < rows and 0 <= point[1] and point[1] < cols

def getNeighbors(board, point):
    rows = len(board)
    cols = len(board[0])
    return set(filter(lambda pt: onBoard(rows, cols, pt), [(point[0]-1, point[1])
            , (point[0]+1, point[1])
            , (point[0], point[1]-1)
            , (point[0], point[1]+1)]))

def getCorners(board):
    return set([(0, 0), (len(board)-1, 0), (0, len(board[0])-1), (len(board)-1, len(board[0])-1)])

def getMiddles(board):
    rm = (len(board) - 1) / 2.
    rowMid = [math.floor(rm), math.ceil(rm)]
    cm = (len(board[0]) - 1) / 2.
    colMid = [math.floor(cm), math.ceil(cm)]
    return set([(int(r), int(c)) for r in rowMid for c in colMid])

def getEmptySquares(board):
    return set((r, c) for r in range(len(board)) for c in range(len(board[0])) if board[r][c] == " ")

def getFirstMovesForX(board):
    return set(filter(lambda pt: pieceAt(board, pt) == 'x', getCorners(board).union(getMiddles(board))))

def getFirstMovesForO(board):
    return getNeighbors(board, getEmptySquares(board).pop())

def getLegalMoves(board, symbol):
    empties = getEmptySquares(board)
    if len(empties) == 0: return getFirstMovesForX(board)
    elif len(empties) == 1: return getFirstMovesForO(board)
    else:
        mine = [(r, c) for r in range(len(board)) for c in range(len(board[0])) if pieceAt(board, (r, c)) == symbol]
        allMoves = [(o, d) for o in mine for d in empties]
        return [move for move in allMoves if isLegalMove(board, symbol, move, False)]

def linearizeBoard(board):
    return "".join(["".join(row) for row in board])

def delinearizeBoard(rawBoard, rows, cols):
    board = [list(rawBoard[i:i+cols]) for i in range(0, len(rawBoard), cols)]
    assert len(board) == rows, print("Problem parsing board! Expected {} rows, got {}.".format(rows, len(board)))
    return board

def printBoard(board):
    for row in board: print("".join(row))
    print()
