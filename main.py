import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt


def conv2d(board, kernel):
    return convolve2d(board, kernel, mode='same', boundary='wrap')


class gameOfLife:

    def __init__(self, height: int, width: int,
                 birth_rules: list[int], survival_rules: list[int]) -> None:
        """ Game of Life

        Args:
        - height: Number of rows in the board.
        - width: Number of columns in the board.
        - birth_rules: List of neighbour counts required to set a cell to alive/on.
        - survival_rules: List of neighbour counts required to keep a cell alive/on.
        """
        self.height = height
        self.width = width

        valid_neighbors = set(range(9))
        self.birth_rules = list(set(birth_rules) & valid_neighbors)
        self.death_rules = list(valid_neighbors - set(survival_rules))

        self.board = np.random.randint(low=0, high=2,
                                       size=(self.height, self.width))
        self.kernel = np.array([[1, 1, 1],
                                [1, 0, 1],
                                [1, 1, 1]], dtype=np.uint8)

    def set_board(self, board: np.ndarray) -> None:
        """Set a custom board state

        Args:
        - board: 2D numpy array of shape (height, width) with values 0 (dead), 1 (alive)
        """

        self.board = board.astype(np.uint8)

    def step(self) -> np.ndarray:
        """Perform one step in Game of Life from current state

        Returns:
        - The updated board state
        """

        neighbor_count = conv2d(self.board, self.kernel)

        birth_indices = (self.board == 0) & np.isin(
            neighbor_count, self.birth_rules)

        death_indices = (self.board == 1) & np.isin(
            neighbor_count, self.death_rules)

        self.board[birth_indices] = 1
        self.board[death_indices] = 0

        return self.board

def main():

    gol = gameOfLife(height=1000,
                     width=1000,
                     birth_rules=[4, 6, 7, 8],
                     survival_rules=[3, 5, 6, 7, 8])

    plt.figure()

    for t in range(1000):
        gol.step()
        plt.clf()
        plt.axis('off')
        plt.imshow(gol.board, cmap='gray')
        plt.waitforbuttonpress(0.01)


if __name__ == '__main__':
    main()
