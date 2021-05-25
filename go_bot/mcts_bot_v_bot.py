from six.moves import input

from dlgo.mcts import mcts
from dlgo import gotypes
from dlgo.agent import naive
from dlgo import goboard_fast as goboard
from dlgo.utils import print_board, print_move, point_from_coords
import time

BOARD_SIZE = 5

def capture_diff(game_state):
	black_stones = 0
	white_stones = 0
	for i in range(1, game_state.board.num_rows + 1):
		for c in range(1, game_state.board.num_cols + 1):
			p = gotypes.Point(r, c)
			color = game_state.board.get(p)
			if color == gotypes.Player.black:
				black_stones += 1
			elif color == gotypes.Player.white:
				white_stones += 1
	dif = black_stones - white_stones
	if game_state.next_player == gotypes.Player.white:
		return -1*dif
	return dif
	
#this heuristics disconsiders the fact that in a go match, threatening to make a capture may have more value than a capture itself.

def main():
	game = goboard.GameState.new_game(BOARD_SIZE)
	bots = {
		gotypes.Player.black: mcts.MCTSAgent(500, temperature=1.4),
		gotypes.Player.white: mcts.MCTSAgent(500, temperature=1.4),
	}

	while not game.is_over():
		time.sleep(0.3)
		
		print(chr(27) + "[2J")
		print_board(game.board)
		bot_move = bots[game.next_player].select_move(game)
		print_move(game.next_player, bot_move)
		game = game.apply_move(bot_move)
		
if __name__ == '__main__':
	main()
		
