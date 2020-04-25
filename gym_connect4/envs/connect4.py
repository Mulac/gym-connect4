import numpy as np
from itertools import groupby
import random

class Connect4:
  """
  Simple connect4 game logic.  For two players 1 & 2.

  Attributes
    + board           -> np.array( shape=(cols, rows) )
    + legal_moves     -> list[int]
    + player          -> int
    + winner          -> int (or None)

  Methods
    + show
    + make_move( column index )
  """
  def __init__(self, cols=7, rows=6):
    self.cols, self.rows = cols, rows
    self.board = np.zeros(shape=(self.cols, self.rows), dtype=np.int8)
    self.player = 1

  @property
  def winner(self):
    return 1 if self.is_winner(1) \
      else -1 if self.is_winner(-1) \
        else 0 if self.board.all() \
          else None

  @property
  def legal_moves(self):
    return [i for i in range(self.cols) if self.board[i][self.rows - 1] == 0]

  def make_move(self, move):
    assert move in self.legal_moves

    # Play their move in the top of the specified column
    top_of_col = np.where(self.board[move] == 0)[0][0]
    self.board[move][top_of_col] = self.player

    # Switch the player
    self.player *= -1
          
  def is_winner(self, player):
    brd = self.board
    # Check horizontal
    for c in range(self.cols - 3):
      for r in range(self.rows):
        if player == brd[c][r] == brd[c+1][r] == brd[c+2][r] == brd[c+3][r]:
          return True

    # Check vertical 
    for c in range(self.cols):
      for r in range(self.rows - 3):
        if player == brd[c][r] == brd[c][r+1] == brd[c][r+2] == brd[c][r+3]:
          return True

    # Check positively sloped diaganols
    for c in range(self.cols - 3):
      for r in range(self.rows - 3):
        if player == brd[c][r] == brd[c+1][r+1] == brd[c+2][r+2] == brd[c+3][r+3]:
          return True

    # Check negatively sloped diaganols
    for c in range(self.cols - 3):
      for r in range(3, self.rows):
        if player == brd[c][r] == brd[c+1][r-1] == brd[c+2][r-2] == brd[c+3][r-3]:
          return True

  def show(self):
    print()
    print(np.rot90(self.board))
