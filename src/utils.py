from src.boards import GenerateBoard
import plotly.express as px  # Import Plotly Express

def select_board(level: str = 'easy', size: int = 18, board_number: int = 0):
    initial_board_image, target_positions, info = GenerateBoard(level, size, board_number).setup_initial_board() 

    # Convert initial_board_image to a Plotly figure
    fig = px.imshow(initial_board_image)  # Use Plotly's imshow with gray scale
    fig.update_xaxes(showticklabels=False)  # Hide x-axis ticks
    fig.update_yaxes(showticklabels=False)  # Hide y-axis ticks

    return fig, target_positions, info