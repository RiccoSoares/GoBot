def best_result(game_state, max_depth, eval_fn):
	if game_state.is_over():
		if game_state.winner() == game_state.next_player: #we're conventioning that evaluation of the board occurs in the next player's pov
			return MAX_SCORE
		else:
			return MIN_SCORE
		
	if max_depth == 0:
		return  eval_fn(game_state)
	
	best_so_far = MIN_SCORE
	for candidate_move in game_state.legal_moves():
		next_state = game_state.apply_move(cadidate_move)
		opponent_best_result = best_result(next_state, max_depth - 1, eval_fn)
		actual_player_result = -1*opponent_best_result
		if actual_player_result > best_so_far:
			best_so_far = actual_player_result
		
	return best_so_far
	

