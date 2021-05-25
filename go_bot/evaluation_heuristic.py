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
