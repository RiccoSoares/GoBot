import importlib

class Encoder:
	def name(self):
		raise NotImplementedError()
	def encode(self, game_state):
		raise NotImplementedError()
	def encode_point(self, point):
		raise NotImplementedError()
	def decode_point(self, index):
		raise NotImplementedError()
	def num_points(self):
		raise NotImplementedError()
	def shape(self):
		raise NotImplementedError()
		
		
def get_encoder_by_name(string, board_size): #creates an encoder by it's name (string), implicitly
	if isinstance(board_size, int):
		board_size = (board_size, board_size) #representing board's rowxcol in a tuple
	module = importlib.import_module('dlgo.encoders.' + string)
	constructor = getattr(module, 'create') #all encoders implemented will have to provide a 'create' function that returns an instance.
	return constructor(board_size)
