import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_connect4.envs.connect4 import Connect4


class Connect4Env(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.action_space = spaces.Discrete(7)
    self.observation_space = spaces.Discrete(42)
    self.reset()

  def step(self, action):
    reward = 0

    if action not in self.game.legal_moves:
      reward = -10

    self.game.make_move(action)

    # Check if game is over and change reward accordingly
    status = self.game.winner
    if status is not None:
      self.done = True
      reward = 1 if status == 1 else -1 if status == 2 else 0

    return self.game.board, reward, self.done, None

  def reset(self):
    self.game = Connect4()
    self.done = False

    # initial empty state
    return self.game.board

  def render(self, mode='human'):
    self.game.show()

  def close(self):
    ...
