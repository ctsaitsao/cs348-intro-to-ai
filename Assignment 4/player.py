import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))
#
#
# START STUDENT CODE
#
#
# This class has been replaced with the code for a deterministic player.
# Your task is to rewrite it to use Minimax
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth): 
        super(MinimaxPlayer, self).__init__(symbol)
        self.depth = depth   # added

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        # legalMoves = game_rules.getLegalMoves(board, self.symbol)
        # if len(legalMoves) > 0: 
        #     return legalMoves[0]
        # else: return None

        def getMinimax(board, depth, opponent):

            if opponent:
                opponent_symbol = self.symbol
            else:
                if self.symbol == 'o':
                    opponent_symbol = 'x'
                else: opponent_symbol = 'o'

            legalMoves = game_rules.getLegalMoves(board, opponent_symbol)

            if len(legalMoves) == 0:
                return ((), self.h1(board, self.symbol))

            if depth == 0:
                return ((), self.h1(board, self.symbol))

            else:
                best_move =  0
                if not opponent: # min
                    best_score = 1000000000
                    for i in legalMoves:
                        new_board = game_rules.makeMove(board, i)
                        minimaxRecursion = getMinimax(new_board, depth - 1, True)
                        if best_score > minimaxRecursion[1]:
                            best_score = minimaxRecursion[1]
                            best_move = i
                    return (best_move, best_score)

                else: # max
                    best_score = -1000000000
                    for i in legalMoves:
                        new_board = game_rules.makeMove(board, i)
                        minimaxRecursion = getMinimax(new_board, depth - 1, False)
                        if best_score < minimaxRecursion[1]:
                            best_score = minimaxRecursion[1]
                            best_move = i
                    return (best_move, best_score)

        return getMinimax(board, self.depth, True)[0]



# This class has been replaced with the code for a deterministic player.
# Your task is to rewrite it to use Minimax with a-b pruning
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): 
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth = depth   # added

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        # legalMoves = game_rules.getLegalMoves(board, self.symbol)
        # if len(legalMoves) > 0: 
        #     return legalMoves[0]
        # else: return None

        def getAB(board, depth, a, b, opponent):

            if opponent:
                opponent_symbol = self.symbol
            else:
                if self.symbol == 'o':
                    opponent_symbol = 'x'
                else: opponent_symbol = 'o'

            legalMoves = game_rules.getLegalMoves(board, opponent_symbol)

            if len(legalMoves) == 0:
                return ((), self.h1(board, self.symbol))

            if depth == 0:
                return ((), self.h1(board, self.symbol))

            else:
                best_move =  0
                if not opponent: # min
                    best_score = 1000000000
                    for i in legalMoves:
                        new_board = game_rules.makeMove(board, i)
                        minimaxRecursion = getAB(new_board, depth - 1, a, b, True)
                        if minimaxRecursion[1] < best_score:
                            best_move = i
                            best_score = minimaxRecursion[1]
                        b = min(b, minimaxRecursion[1])
                        if a >= b:
                            break
                    return (best_move, best_score)

                else: #max
                    best_score = -1000000000
                    for i in legalMoves:
                        new_board = game_rules.makeMove(board, i)
                        minimaxRecursion = getAB(new_board, depth - 1, a, b, False)
                        if minimaxRecursion[1] > best_score:
                            best_move = i
                            best_score = minimaxRecursion[1]
                        a = max(a, minimaxRecursion[1])
                        if a >= b:
                            break
                    return (best_move, best_score)

        return getAB(board, self.depth, -1000000000, 1000000000, True)[0]       

#
#
# END STUDENT CODE
#
#

class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)
