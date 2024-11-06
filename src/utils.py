from src.boards import GenerateBoard
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def randomize_board(level: str = 'easy', size: int = 18):
    initial_board_image, target_positions, info = GenerateBoard(level, size).setup_initial_board() 

    # Convert initial_board_image to a matplotlib figure
    fig, ax = plt.subplots()
    ax.imshow(initial_board_image)
    ax.axis('off')

    return fig, target_positions, info