NUM_SIMULATIONS = 300


class Node:
    def __init__(self, prior):
        self.prior = prior
        self.player = None
        self.visits = 0
        self.value_sum = 0
        self.children = []

    @property
    def value(self):
        """ Average value expected reward from this node """
        return self.value_sum / self.visits if self.visits else 0

    @property
    def expanded(self):
        """ Has the node been explored (is it a leaf)? """
        return len(self.children) > 0


def mcts(game, network):
    root = Node(0)
    root.player = game.player

    for _ in range(NUM_SIMULATIONS):
        fake_game = game.clone()
        node = root
        trajectory = []

        while node.expanded:
            # Has children so pick one
            action, node = select_child(node)
            fake_game.make_move(action)
            trajectory.append(node)

        # Expand node
        value = expand_node(node, fake_game, network)
        backpropagate(trajectory, value, game.player)

    return select_action(root)


def select_child(node):
    _, action, child = max((ucb_score(child), action, child) for action, child in node.children.items())
    return action, child


def ucb_score(node):
    """ Q + U is the ucb score that takes exploration into account"""
    raise NotImplementedError


def expand_node(node, game, network):
    value, policy_dist = network(game.board)

    node.player = game.player
    policy = {a: policy_dist[a] for a in game.legal_moves}
    for action, p in policy.items():
        node.children[action] = Node(p)

    return value


def backpropagate(trajectory, value, player):
    for node in trajectory:
        node.visits += 1
        node.value_sum += value if node.player == player else -value


def select_action(root):
    _, action = max((child.value, action) for action, child in root.children.items())
    return action
