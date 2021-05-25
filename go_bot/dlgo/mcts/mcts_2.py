import math
import random

from dlgo import agent
from dlgo.agent import naive
from dlgo.agent.base import Agent
from dlgo.gotypes import Player
from dlgo.utils import point_from_coords

__all__ = [
	'MCTSAgent',
]

def fmt(x):
    if x is Player.black:
        return 'B'
    if x is Player.white:
        return 'W'
    if x.is_pass:
        return 'pass'
    if x.is_resign:
        return 'resign'
    return coords_from_point(x.point)
    
def show_tree(node, indent='', max_depth=3):
    if max_depth < 0:
        return
    if node is None:
        return
    if node.parent is None:
        print('%sroot' % indent)
    else:
        player = node.parent.game_state.next_player
        move = node.move
        print('%s%s %s %d %.3f' % (
            indent, fmt(player), fmt(move),
            node.num_rollouts,
            node.winning_frac(player),
        ))
    for child in sorted(node.children, key=lambda n: n.num_rollouts, reverse=True):
        show_tree(child, indent + '  ', max_depth - 1)

class MCTSNode(object):
	def __init__(self, game_state, parent=None, move=None, children=None, win_counts=None, num_rollouts=None, unvisited_nodes=None):
		self.game_state = game_state
		self.parent = parent
		self.move = move
		self.children = []
		self.win_counts = {
			Player.black: 0,
			Player.white: 0
		}
		self.num_rollouts = 0
		self.unvisited_nodes = game_state.legal_moves()
		
	def add_random_child(self):
		random_index = random.choice(range(0, len(self.unvisited_nodes) - 1))
		unvisited_node = self.unvisited_nodes.pop(random_index)
		next_state = self.game_state.apply_move(unvisited_node)
		new_node = MCTSNode(next_state, self, unvisited_node)
		self.children.append(new_node)
		return new_node
		
	def record_win(self, winner):
		self.win_counts[winner] += 1
		self.num_rollouts += 1
		
	def can_add_child(self):
		return len(self.unvisited_nodes) > 0
		
	def is_terminal(self):
		return self.game_state.is_over()
		
	def winning_pct(self, player):
		return float(self.win_counts[player])/float(self.num_rollouts)

def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
	exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
	return win_pct + temperature * exploration

		
class MCTSAgent(Agent):
	def __init__(self, num_rounds, temperature):
		Agent.__init__(self)
		self.num_rounds = num_rounds
		self.temperature = temperature
	
	def select_move(self, game_state):
		root = MCTSNode(game_state)
		
		
		for i in range(self.num_rounds):
			node = root
			while (not node.can_add_child()) and (not node.is_terminal()):
				node = self.select_child(node)
				
			if node.can_add_child():
				node = node.add_random_child()
				
			winner = self.simulate_random_game(node.game_state)
			
			while node is not None:
				node.record_win(winner)
				node = node.parent
				
		best_move = None
		best_pct = -1.0
		for child in root.children:
			child_pct = child.winning_pct(game_state.next_player)
			if child_pct > best_pct:
				best_pct = child_pct
				best_move = child.move
			return best_move
	
	def select_child(self, node):
		total_rollouts = sum(child.num_rollouts for child in node.children)
		
		best_score = -1
		best_child = None
		for child in node.children:
			score = uct_score(total_rollouts, child.num_rollouts, child.winning_pct(node.game_state.next_player), self.temperature)
			if score > best_score:
				best_score = score
				best_child = child
				
		return best_child
	
	@staticmethod
	def simulate_random_game(game):
		bots = {
			Player.black: naive.RandomBot(),
			Player.white: naive.RandomBot(),
		}
		while not game.is_over():
			bot_move = bots[game.next_player].select_move(game)
			game = game.apply_move(bot_move)
		return game.winner()
	
	
	
	
	
	
	
