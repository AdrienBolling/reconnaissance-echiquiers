
import numpy as np
import tensorflow as tf
from tensorflow import keras
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
from tensorflow.keras import layers


'''
Define a prediction function taking a picture of a non-empty square as input and outputs its class
using the weights after training
with this format :
'empty'
'occupied'
'''