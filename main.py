import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt


def conv2d(board, kernel):
    return convolve2d(board, kernel, mode='same', boundary='wrap')


class gameOfLife:

    def __init__(self, height, width, x, y):

        self.height = height
        self.width = width

        u = {i for i in range(9)}

        # Rule Bx/Sy
        self.x = list(set(x))
        self.ny = list(u - set(y))

        self.board = np.random.randint(low=0, high=2,
                                       size=(self.height, self.width))
        self.kernel = np.array([[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1]], dtype=np.uint8)

    def set_board(self, board):
        self.board = board.astype(np.uint8)

    def step(self):

        num_neighbors = conv2d(self.board, self.kernel)

        next_board = np.where((np.isin(self.board, [0])
                               & np.isin(num_neighbors, self.x)),
                              1, self.board)

        next_board = np.where((np.isin(self.board, [1])
                               & np.isin(num_neighbors, self.ny)),
                              0, next_board)

        self.board = next_board

        return self.board


def main():

    width = 100
    height = 100

    gol = gameOfLife(height=100,
                     width=100,
                     x = [3],
                     y = [2,3])
    
    plt.figure()

    for t in range(1000):
        gol.step()
        plt.clf()
        plt.axis('off')
        plt.imshow(gol.board, cmap='gray')
        plt.waitforbuttonpress(0.01)


if __name__ == '__main__':
    main()
