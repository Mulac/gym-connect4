import gym
from gym import error, spaces, utils
from gym.utils import seeding

from itertools import groupby


class TictactoeEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.action_space = spaces.Discrete(7)
    self.observation_space = spaces.Box(7, 6)
    self.game = Connect4()
    self.reset()

  def step(self, action):
    reward = 0

    self.game.make_move(action)

    status = self.game.winner
    if status:
      self.done = True
      reward = 1 if status == 1 else -1

    return self.game.board, reward, self.done, None

  def reset(self):
    self.done = False

  def render(self, mode='human'):
    self.game.show()

  def close(self):
    ...


class Connect4:
  def __init__(self):
    self.board = {0: [0]*6,
                  1: [0]*6,
                  2: [0]*6,
                  3: [0]*6,
                  4: [0]*6,
                  5: [0]*6,
                  6: [0]*6}
    self.possible_moves = [i for i in range(7)]
    self.player = 0
    self.winner = None
      
  def make_move(self, move):
    if move not in self.possible_moves:
      return
        
    # Switch the player and play their move in the top of the specified column
    self.player = 1 if self.player != 1 else 2
    top_of_col = self.board[move].index(0)
    self.board[move][top_of_col] = self.player
    
    # Players have reached the top of column so remove it from possible actions
    if top_of_col >= 5:
      self.possible_moves.remove(move)
        
    if self.check_winner(move, top_of_col):
      self.winner = self.player
          
  def check_winner(self, col, row):
    # just to keep variable names short
    val = self.player
    brd = self.board

    # check right 
    if col <= 3:
      # Horizontal
      if brd[col+1][row] == brd[col+2][row] == brd[col+3][row] == val:
        return True
      # Diagonal Down
      if row >= 3 and brd[col+1][row-1] == brd[col+2][row-2] == brd[col+3][row-3] == val:
        return True
      # Diagonal Up
      if row <= 2 and brd[col+1][row+1] == brd[col+2][row+2] == brd[col+3][row+3] == val:
        return True
    
    # check left
    if col >= 3:
      # Horizontal
      if brd[col-1][row] == brd[col-2][row] == brd[col-3][row] == val:
        return True
      # Diagonal Down
      if row >= 3 and brd[col-1][row-1] == brd[col-2][row-2] == brd[col-3][row-3] == val:
        return True
      # Diagonal Up
      if row <= 2 and brd[col-1][row+1] == brd[col-2][row+2] == brd[col-3][row+3] == val:
        return True
        
    # check vertical
    return any(1 for key, group in groupby(brd[col]) if len(list(group)) > 3 and key == val)

  def show(self):
    for x in range(5, -1, -1):
      print([self.board[k][x] for k in self.board])
