import numpy as np
import os
import torch
from torch.utils.data import Dataset


class BoardsDataset(Dataset):
	""" Go Boards Dataset	"""
	
	def __init__(self, x_np_array, y_np_array, transform=None, mode='train'):
		'''
		Args:
			x_np_array: np array containing an integer number of encoded board positions
			y_np_array: np array containing an integer number of encoded moves that answer the corresponding board positions
		
		'''
		self.x_tensor = torch.from_numpy(x_np_array).type(torch.float32) #performs the numpy array to torch tensor convertion
		self.num_samples = len(self.x_tensor)
		self.mode = mode	
			
		if mode == 'train': #test mode does not include y data.
			self.y_tensor = torch.from_numpy(y_np_array).type(torch.float32)	
			assert len(self.x_tensor) == len(self.y_tensor)
					
		
	def __len__(self):
		return self.num_samples
		
	def __getitem__(self, idx):

		input_board_state = self.x_tensor[idx].unsqueeze(0)
		if self.mode == 'train':
		#moves are one-hot encoded, so we'll return the index corresponding to target board position
			answer_move = torch.argmax(self.y_tensor[idx], dim=0) 
			output = {"board": input_board_state, "move": answer_move}
		else:
			output = input_board_state
			
		return output
		
def loadArrays(rootdir, x_filename, y_filename):
	'''
	Utility function to load the saved data.
	
	Args:
		rootdir: root dir containing x and y .npy files
		x_filename: .npy file containing the encoded board samples
		y_filename: .npy file containing encoded moves that answer the corresponding board positions
	'''

	if os.pathisdir(rootdir):
		x_filepath = os.path.join(rootdir, x_filename)
		y_filename = os.path.join(rootdir, y_filename)
		
		x_array = np.load(x_filepath)
		y_array = np.load(y_filepath)
		
		return x_array, y_array
	
	else:
		print('Specified root directory does not exists')
	
def splitData(rootdir, x_filename, y_filename, validation_proportion=0.2):
	'''
	Utility function to load saved data , create datasets and split into train and test samples
	
	Args:
		validation_proportion: train/test data proportion, default is 0.2 meaning that aprox. 1/5 of the data will be used as test data
		rootdir: root dir containing x and y .npy files
		x_filename: .npy file containing the encoded board samples
		y_filename: .npy file containing encoded moves that answer the corresponding board positions
		
	'''
	
	x_array, y_array = loadArrays(rootdir, x_filename, y_filename)
	train_prop = 1 - validation_proportion
	#splitting into train and validation data
	indx = int(train_prop*len(x_array))
	x_train = x_array[:indx]
	x_valid = x_array[indx:]
	
	y_train = x_array[:indx]
	y_valid = y_array[indx:]
	
	#instantiating each dataset.
	trainset = BoardsDataset(x_train, y_train)
	testset = BoardsDatset(x_valid, y_valid, mode='test')

	datasets = {'train': trainset, 'test': testset}
	return datasets
	
	
	
