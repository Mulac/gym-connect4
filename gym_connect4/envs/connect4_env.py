import gym
from gym import error, spaces, utils
from gym.utils import seeding

from itertools import groupby
import numpy as np
import random


class Connect4Env(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.action_space = spaces.Discrete(7)
    self.observation_space = spaces.Discrete(42)
    self.reset()

  def step(self, action):
    reward = 0

    if action not in self.game.possible_moves:
      reward = -10

    self.game.make_move(action)

    # Check if game is over and change reward accordingly
    status = self.game.winner
    if status is not None:
      self.done = True
      reward = 1 if status == 1 else -1 if status == 2 else 0

    return [v for col in self.game.board.values() for v in col], reward, self.done, None

  def reset(self):
    self.game = Connect4()
    self.done = False

    # initial empty state
    return [0]*self.observation_space.n

  def render(self, mode='human'):
    self.game.show()

  def close(self):
    ...


class Connect4:
  """
  Simple connect4 game logic.  For two players 1 & 2.

  Attributes
    + board           {index: column}
    + possible_moves  [column indexes]
    + player          1 or 2
    + winner          0 or 1 or 2 -> gameover
                      None        -> in play

  Methods
    + show
    + make_move( column index )
  """
  def __init__(self):
    self.board = {0: [0]*6,
                  1: [0]*6,
                  2: [0]*6,
                  3: [0]*6,
                  4: [0]*6,
                  5: [0]*6,
                  6: [0]*6}
    self.possible_moves = [i for i in range(7)]
    self.player = 1
    self.winner = None
      
  def make_move(self, move):
    if move not in self.possible_moves:
      return
        
    # Play their move in the top of the specified column
    top_of_col = self.board[move].index(0)
    self.board[move][top_of_col] = self.player
    
    # Players have reached the top of column so remove it from possible actions
    if top_of_col >= 5:
      self.possible_moves.remove(move)
        
    # Check if the game is over
    if self.check_winner(move, top_of_col):
      self.winner = self.player
    if not self.possible_moves:
      self.winner = 0

    # Switch the player
    self.player = 1 if self.player != 1 else 2
          
  def check_winner(self, col, row):
    val = self.player
    brd = self.board

    # check right 
    if col <= 3:
      # Horizontal
      if brd[col+1][row] == brd[col+2][row] == brd[col+3][row] == val:
        return True
      # (bounds check)  Diagonal Down 
      if row >= 3 and brd[col+1][row-1] == brd[col+2][row-2] == brd[col+3][row-3] == val:
        return True
      # (bounds check)  Diagonal Up
      if row <= 2 and brd[col+1][row+1] == brd[col+2][row+2] == brd[col+3][row+3] == val:
        return True
    
    # check left
    if col >= 3:
      # Horizontal
      if brd[col-1][row] == brd[col-2][row] == brd[col-3][row] == val:
        return True
      # (bounds check)  Diagonal Down 
      if row >= 3 and brd[col-1][row-1] == brd[col-2][row-2] == brd[col-3][row-3] == val:
        return True
      # (bounds check)  Diagonal Up
      if row <= 2 and brd[col-1][row+1] == brd[col-2][row+2] == brd[col-3][row+3] == val:
        return True

    # check vertical
    return any([1 for key, group in groupby(brd[col]) if len(list(group)) > 3 and key == val])

  def show(self):
    print()
    for x in range(5, -1, -1):
      print([self.board[k][x] for k in self.board])
