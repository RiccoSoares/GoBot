'''
		Script made to understand better each of the two defined models.
	
		Random tensors having the expected input's shape (1x1x9x9) or (1x1x19x19) are created,
	each layer's input and output shapes are printed. The __call__ method for each model is tested too.	
'''

import torch
import torch.nn as nn
import torch.nn.functional as F
from model import nineNet
from model import standardNet

print('')
print("Testing the 9x9 board model's layers and __call__ method with a random input")
print('')
#instanciating the 9x9 model and testing each layer's output.
net = nineNet()

example_input = torch.rand((1,1,9,9))
conv1_output = F.relu(net.conv1(example_input))
print('first convolution layer')
print(example_input.shape, conv1_output.shape)
print('')

conv1_pool = F.max_pool2d(conv1_output, (2,2))
print('max pool')
print(conv1_output.shape, conv1_pool.shape)
print('')

print('second convolution layer')
conv2 = F.relu(net.conv2(conv1_pool))
print(conv1_pool.shape, conv2.shape)
print('')

print('flattening the output')
flat = conv2.flatten(0)
print(conv2.shape, flat.shape)
print('')

print('first linear layer')
fc1_out = F.relu(net.fc1(flat))
print(flat.shape, fc1_out.shape)
print('')

print('second linear layer')
fc2_out = F.relu(net.fc2(fc1_out))
print(fc1_out.shape, fc2_out.shape)
print('')

#testing the same model directly calling the __call__ method.
print('using call method')
example_output = net(example_input)
print(example_input.shape, example_output.shape)
print('')


print('')
print("Testing the 19x19 board model's layers and __call__ method with a random input")
print('')
#instanciating the 19x19 model and testing each layer's output.
net = standardNet()

example_input = torch.rand((1,1,19,19))
conv1_output = F.relu(net.conv1(example_input))
print('first convolution layer')
print(example_input.shape, conv1_output.shape)
print('')

print('second convolution layer')
conv2 = F.relu(net.conv2(conv1_output))
print(conv1_output.shape, conv2.shape)
print('')

conv2_pool = F.max_pool2d(conv2, (2,2))
print('max pool')
print(conv2.shape, conv2_pool.shape)
print('')

print('third convolution layer')
conv3 = F.relu(net.conv3(conv2_pool))
print(conv2_pool.shape, conv3.shape)
print('')

print('fourth convolution layer')
conv4 = F.relu(net.conv4(conv3))
print(conv3.shape, conv4.shape) 
print('')

print('flattening the output')
flat = conv4.flatten(0)

print('first linear layer')
fc1 = F.relu(net.fc1(flat))
print(flat.shape, fc1.shape)
print('')

print('second linear layer')
fc2 = F.relu(net.fc2(fc1))
print(fc1.shape, fc2.shape)
print('')

print('third linear layer')
fc3 = F.relu(net.fc3(fc2))
print(fc2.shape, fc3.shape)
print('')

#testing the same model directly calling the __call__ method.
print('using call method')
example_output = net(example_input)
print(example_input.shape, example_output.shape)
print('')

