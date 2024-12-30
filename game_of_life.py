import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter


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

    def reset(self, board: np.ndarray = None) -> None:
        """Set a custom board state

        If no argument is passed, board is set to a random state

        Args:
        - board: 2D numpy array of shape (height, width) with values 0 (dead), 1 (alive)
        """
        if board is None:
            self.board = np.random.randint(low=0, high=2,
                                           size=(self.height, self.width))
        else:
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

    def save(self, fname: str, steps: int, cmap: str, fps: int = 16) -> None:
        """Save as an animation (gif)

        Args:
        - fname: Path to file
        - steps: Number of steps to simulate
        - cmap: Colormap
        - fps: Framerate
        """

        fig, ax = plt.subplots(figsize=(6, 6))

        ax = plt.axes([0, 0, 1, 1], frameon=False)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.autoscale(tight=True)

        img = ax.imshow(self.board, cmap=cmap, interpolation='none')

        def update(frame):
            img.set_data(self.board)
            self.step()
            return [img]

        animation = FuncAnimation(fig, update, frames=steps)
        gif_writer = PillowWriter(fps=fps)
        animation.save(fname, writer=gif_writer)


def main():

    gol = gameOfLife(height=100,
                     width=100,
                     birth_rules=[3],
                     survival_rules=[2, 3])

    gol.save('test.gif', steps=64, cmap='gray')


if __name__ == '__main__':
    main()
