import numpy as np


class NeuralNetwork:
    def __init__(self,input_size: int, hidden_size: int, output_size: int):
        self.w1 = np.random.randn(input_size, hidden_size) = 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.w2 = np.random.randn(hidden_size, output_size) = 0.01
        self.b2 = np.zeros((1, output_size))


if __name__ == "__main__":
    nn = NeuralNetwork(input_size=784, hidden_size=128, output_size=10)
    nn = NeuralNetwork()
