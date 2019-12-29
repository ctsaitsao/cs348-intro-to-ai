import sys, os, game_rules, curses, game_manager
import player

class Display(object):
    """"""
    def __init__(self, stdscr, manager):
        super(Display, self).__init__()
        self._stdscr = stdscr
        self._gm = manager
        self.SetDimensions()

        self._cursor = self._start
        self._last = 0

        self._p1state = self._p2state = None
        if isinstance(self._gm.p1, player.HumanPlayer): self._p1state = self.PlayerInputState()
        if isinstance(self._gm.p2, player.HumanPlayer): self._p2state = self.PlayerInputState()

        inbounds = self._dimensions > (self._gm.rows+3,self._gm.cols+3)
        # ASSERRTIONS ARE CONTRACTS WITHOUT BLAME.
        # We do this so that the screen isn't too small. There will still be problems if people resize.
        assert inbounds, "Screen too small for board: {} vs {}".format((self._gm.rows, self._gm.cols), self._dimensions)

    def MoveCursor(self, dx, dy):
        x, y = self._cursor
        height,width = self._dimensions
        x = min(width - 1, max(0, x+dx))
        y = min(height - 2, max(0, y+dy))

        self._cursor = (x,y)


    def SetDimensions(self):
        self._dimensions = self._stdscr.getmaxyx()
        height,width = self._dimensions
        self._center = (width//2,height//2)
        self._start = (width//2 - self._gm.cols//2, height//2 - self._gm.rows//2)


    def Loop(self):
        stdscr = self._stdscr
        stdscr.clear()

        self.SetDimensions()
        self.Draw(stdscr)

        cursor_x, cursor_y = self._cursor
        stdscr.move(cursor_y, cursor_x)        
        self.ProcessInput(stdscr)

        stdscr.refresh()


    def Draw(self, stdscr):
        self.DrawBoard(stdscr)
        self.DrawStatus(stdscr)


    def DrawBoard(self, stdscr):
        height, width = self._dimensions
        cursor_x, cursor_y = self._cursor

        board = self._gm.board
        center_x,center_y = self._center
        start = self._start
        for i, row in enumerate(board):
            string = ''.join(row)
            stdscr.addstr(start[1]+i, start[0], string)

        stdscr.attron(curses.color_pair(2))
        if self._gm.GetTurn() == 'x' and self._p1state and self._p1state.selected:
            pos = self._p1state.selected; stdscr.addstr(pos[1], pos[0], 'x')
        if self._gm.GetTurn() == 'o' and self._p2state and self._p2state.selected:
            pos = self._p2state.selected; stdscr.addstr(pos[1], pos[0], 'o')
        stdscr.attroff(curses.color_pair(2))


    def DrawStatus(self, stdscr):
        symbol = self._gm.GetTurn().capitalize()
        player = self._gm.p1 if symbol == 'X' else self._gm.p2
        
        text = ' Press \'q\' to quit'
        if self._gm.GetWinner(): text += ' | {} wins!'.format(self._gm.GetWinner())
        else: text += ' | Turn {0:{width}} ({1}, {2}) '.format(self._gm.turn_number, symbol, player, width=3)
        height, width = self._dimensions
        
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, text)
        stdscr.addstr(height-1, len(text), ' ' * (width - len(text) - 1))
        stdscr.attroff(curses.color_pair(3))


    def ProcessInput(self, stdscr):
        self._last = stdscr.getch()

        if   self._last == curses.KEY_DOWN:  self.MoveCursor(0,1)
        elif self._last == curses.KEY_UP:    self.MoveCursor(0,-1)
        elif self._last == curses.KEY_RIGHT: self.MoveCursor(1,0)
        elif self._last == curses.KEY_LEFT:  self.MoveCursor(-1,0)
        elif self._last == 32: self.TakeTurn()
        elif self._last == ord('q'): self._gm.interrupt(None, None)


    def TakeTurn(self):
        if self._gm.GetTurn() == 'x' and self._p1state:
            if self._p1state.selected:
                pair = self.GetMovePair(self._p1state.selected, self._cursor)
                self._gm._takeTurn(pair)
                self._p1state.Deselect()
            else: self._p1state.Select(self._cursor)
        elif self._gm.GetTurn() == 'o' and self._p2state:
            if self._p2state.selected:
                pair = self.GetMovePair(self._p2state.selected, self._cursor)
                self._gm._takeTurn(pair)
                self._p2state.Deselect()
            else: self._p2state.Select(self._cursor)
        else: self._gm._takeTurn()

    def GetMovePair(self, start, end):
        startpos = (start[1] - self._start[1], start[0] - self._start[0])
        endpos = (end[1] - self._start[1], end[0] - self._start[0])
        return (startpos, endpos)


    class PlayerInputState(object):
        """Container class for input state. Just keep adding layers of abstraction; it's the computer science way."""
        def __init__(self): self.selected = None
        def __str__(self): return str(self.selected)
        def Select(self, cursor): self.selected = cursor
        def Deselect(self): self.selected = None


def MakeBoard(p1, p2):
    iterations = 1 
    depth = 3
    rows, cols = 10, 10
    gm = game_manager.GameManager(rows, cols, player.makePlayer(p1, 'x', depth), player.makePlayer(p2, 'o', depth), True)

    return gm

def Init(stdscr):
    stdscr.clear()
    stdscr.refresh()
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

def Loop(stdscr, p1, p2):
    Init(stdscr)

    gm = MakeBoard(p1, p2)
    display = Display(stdscr, gm)
    while True: display.Loop()


if __name__ == '__main__':
    args = sys.argv
    p1, p2 = 'H', 'R'

    if len(args) == 3:
        p1 = str(args[1]).capitalize()
        p2 = str(args[2]).capitalize()

    if p1 not in ['A', 'M', 'R', 'D', 'H']: p1 = 'H'
    if p2 not in ['A', 'M', 'R', 'D', 'H']: p2 = 'R'
    
    curses.wrapper(Loop, p1, p2)