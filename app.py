import gradio as gr
import plotly.express as px
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt  # Add this import for Matplotlib
import io  # Add this import for io
import plotly.io as pio  # Import Plotly's I/O module

from src.play import PlayEpisode as Play
from src.boards import GenerateBoard



TITLE = """<h1 align="center" id="space-title"> Pento-LLaVA 🤖🎯🎮</h1>"""


pento_llava_app = gr.Blocks()

def select_board(level: str = 'easy', size: int = 18, board_number: int = 0):
    initial_board_image, target_positions, info = GenerateBoard(level, size, board_number).setup_initial_board() 
    return initial_board_image, target_positions, info

def get_plotly_fig(image):
    fig = px.imshow(image)  # Use Plotly's imshow with gray scale
    fig.update_xaxes(showticklabels=False)  # Hide x-axis ticks
    fig.update_yaxes(showticklabels=False)  # Hide y-axis ticks

    # Update the figure to include a boundary/frame
    fig.update_layout(
        xaxis=dict(showline=True, linecolor='black', linewidth=2, showgrid=True, zeroline=True),
        yaxis=dict(showline=True, linecolor='black', linewidth=2, showgrid=True, zeroline=True),
        margin=dict(l=0, r=0, t=0, b=0),
        height=512,
        width=512
    )

    return fig

def get_gray_image(image):
    gray_image = image
    # Convert all white pixels to gray
    gray_image = gray_image.convert("RGBA")  # Ensure the image has an alpha channel
    data = np.array(gray_image)  # Convert image to numpy array
    # Create a mask for white pixels
    white_pixels = (data[:, :, :3] == [255, 255, 255]).all(axis=2)
    data[white_pixels] = [200, 200, 200, 20]

    gray_image = Image.fromarray(data)  # Convert back to image

    return gray_image

def gen_new_board(value):
    value = int(value)
    image, _, _ = select_board('easy', 18, value)
    gray_image = get_gray_image(image)
    
    gray_fig = get_plotly_fig(gray_image)
    fig = get_plotly_fig(image)

    return fig, gray_fig

def gen_info(value):
    value = int(value)
    _, _, info = select_board('easy', 18, value)

    return info

def gen_target_str(value):
    value = int(value)
    _, _, info = select_board('easy', 18, value)
    target_info = info[0]
    target_str = f"<span>Target piece for this episode is <span style='color: {target_info['piece_colour']};'>{target_info['piece_colour']}</span> <span style='color: {target_info['piece_colour']};'>{target_info['piece_shape']}</span> located at <span style='color: {target_info['piece_colour']};'>{target_info['piece_region']}</span></span>"

    return target_str
global play

def setup_initial_env(value):
    global play
    play = Play('easy', 18, value)

def reverse_get_plotly_fig(plot_data):
    """Convert a Gradio PlotData object to a Matplotlib figure."""
    # Extract the Plotly figure from the Gradio PlotData object
    fig = plot_data.plot  # Access the underlying Plotly figure

    # Ensure fig is a Figure object
    if isinstance(fig, str):
        import plotly.io as pio
        fig = pio.from_json(fig)  # Convert string back to Figure

    # Convert the Plotly figure to a static image (PNG format)
    image_data = pio.to_image(fig, format="png")  # Get the image data in PNG format
    image = Image.open(io.BytesIO(image_data))  # Convert to PIL Image
    return image

def setup_play(image):
    global play  # Ensure play is accessible

    # Convert the Gradio PlotData to a Matplotlib figure
    matplot_image = reverse_get_plotly_fig(image)  # Ensure image is a valid Plotly Figure

    image = play.play_instance(model=None, processor=None, input_image=matplot_image)
    gray_image = get_gray_image(image)

    # Convert the processed image back to a Plotly figure
    gray_fig = get_plotly_fig(gray_image)
    image_fig = get_plotly_fig(image)

    return image_fig, gray_fig

## Initial Setup
fig, gray_fig = gen_new_board(0)
target_str = gen_target_str(0)
info = gen_info(0)


with pento_llava_app:

    gr.HTML(TITLE)

    with gr.Row():
        with gr.Column():    
            white_board = gr.Plot(fig, visible=True)

        with gr.Column():   
            gray_board = gr.Plot(gray_fig,
                                  visible=True)

    with gr.Row():
        select_board_items = gr.Dropdown(
            choices=range(512),
            interactive=True
        )

        display_string = gr.HTML(value=gen_target_str(0)) 

    
        play_button = gr.Button("Predict Next Move") 

        initial_setup_button = gr.Button("Setup Environment")
        

    select_board_items.change(
        fn=setup_initial_env,
        inputs=[select_board_items],
        queue=True
    )

    select_board_items.change(
        fn=gen_new_board,
        inputs=[select_board_items],
        outputs=[white_board, gray_board],
        queue=True
    )

    select_board_items.change(
        fn=gen_target_str,
        inputs=[select_board_items],
        outputs=[display_string],
        queue=True
    )

    play_button.click(  # Set up button click event
        fn=setup_play,  # Call setup_play once
        inputs=[white_board],
        outputs=[white_board, gray_board],
        queue=True
    )

    

    pento_llava_app.load()

pento_llava_app.queue()
pento_llava_app.launch()
