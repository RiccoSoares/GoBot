import torch
import torch.nn as nn
import torch.nn.functional as F


class nineNet(nn.Module): #simple neural network to play in a 9x9 board
	def __init__(self):
		super(nineNet, self).__init__()
		#input originally has only 1 input channel
		self.conv1 = nn.Conv2d(1, 32, 3, padding=1) #padding because of the small board size.
		self.conv2 = nn.Conv2d(32, 64, 3)

		self.fc1 = nn.Linear(64 * 2 * 2, 200)  
		self.fc2 = nn.Linear(200, 81)
		self.dropoutLayer = nn.Dropout(p=0.4)

	def forward(self, x):
		x = F.relu(self.conv1(x)) #first conv layer pass
		x = F.max_pool2d(x, (2,2)) #max pool pass
		x = F.relu(self.conv2(x)) #second conv layer
		x = x.flatten(1) #flattening
		x = self.dropoutLayer(x)
		x = F.relu(self.fc1(x)) #first linear layer
		x = self.dropoutLayer(x)
		x = self.fc2(x) #second linear layer
		
		return x
		
class nineNetv2(nn.Module): #same idea of nineNet, using more layers, more padding to produce larger outputs and without max pooling.
	def __init__(self):
		super(nineNetv2, self).__init__()
		#input originally has only 1 input channel
		self.conv1 = nn.Conv2d(1, 32, 3, padding=3) #padding because of the small board size.
		self.conv2 = nn.Conv2d(32, 64, 3, padding=2)
		self.conv3 = nn.Conv2d(64, 64, 3, padding=2)
		self.conv4 = nn.Conv2d(64, 128, 3, padding=2)
		self.conv5 = nn.Conv2d(128, 128, 3)

		self.fc1 = nn.Linear(128 * 17 * 17, 512)  
		self.fc2 = nn.Linear(512, 81)
		self.dropoutLayer = nn.Dropout(p=0.5)

	def forward(self, x):
		x = F.relu(self.conv1(x)) #first conv layer pass
		x = F.relu(self.conv2(x)) #second conv layer
		x = F.relu(self.conv3(x)) #third conv layer
		x = F.relu(self.conv4(x)) #fourth conv layer
		x = F.relu(self.conv5(x)) #fifth conv layer
		x = x.flatten(1) #flattening
		x = self.dropoutLayer(x) #adding dropout layer
		x = F.relu(self.fc1(x)) #first linear layer
		x = self.dropoutLayer(x) #second dropout layer
		x = self.fc2(x) #last linear layer
		
		return x

class standardNet(nn.Module): #simple neural network to play in a 19x19 board
	def __init__(self):
		super(standardNet, self).__init__()
		#input originally has only 1 input channel
		self.conv1 = nn.Conv2d(1, 32, 3)
		self.conv2 = nn.Conv2d(32, 64, 3)
		self.conv3 = nn.Conv2d(64, 128, 3)
		self.conv4 = nn.Conv2d(128, 256, 3)

		self.fc1 = nn.Linear(256*3*3, 1024)  
		self.fc2 = nn.Linear(1024, 256)
		self.fc3 = nn.Linear(256, 81)

	def forward(self, x):
		x = F.relu(self.conv1(x)) #first conv layer pass
		x = F.relu(self.conv2(x)) #second conv layer 
		x = F.max_pool2d(x, (2,2)) #max pool layer
		x = F.relu(self.conv3(x)) #third conv layer
		x = F.relu(self.conv4(x)) #fourth conv layer 
		x = x.flatten(1) #flattening
		x = F.relu(self.fc1(x)) #first linear layer
		x = F.relu(self.fc2(x)) #second linear layer
		x = self.fc3(x) #third linear layer
	
		return x
        

