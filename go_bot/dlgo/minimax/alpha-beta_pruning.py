def alpha_beta_result(game_state, max_depth, best_black, best_white, eval_fn):
	if game_state.next_player == Player.white:
		if best_so_far > best_white:
			best_white = best_so_far
		outcome_for_black = -1*best_white
		if outcome_for_black < best_black: #this is the case where the best move for white beats the best move for black
			return best_so_far
