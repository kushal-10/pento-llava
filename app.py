import gradio as gr

from src.utils import select_board
from src.play import PlayEpisode as Play
import plotly.express as px

TITLE = """<h1 align="center" id="space-title"> Pento-LLaVA 🤖🎯🎮</h1>"""

pento_llava_app = gr.Blocks()
fig, targets, info = select_board('easy', 18, 0)

# Update the figure to include a boundary/frame
fig.update_layout(
    xaxis=dict(showline=True, linecolor='black', linewidth=2, showgrid=True, zeroline=True),
    yaxis=dict(showline=True, linecolor='black', linewidth=2, showgrid=True, zeroline=True),
    margin=dict(l=0, r=0, t=0, b=0),
    height=512,
    width=512
)

target_strs = []
for t in targets:
    target_strs.append(t['target_str'])

def gen_new_board(value):
    value = int(value)
    fig, _, _ = select_board('easy', 18, value)

    # Update the figure to include a boundary/frame
    fig.update_layout(
        xaxis=dict(showline=True, linecolor='black', linewidth=2, showgrid=True, zeroline=True),
        yaxis=dict(showline=True, linecolor='black', linewidth=2, showgrid=True, zeroline=True),
        margin=dict(l=0, r=0, t=0, b=0),
        height=512,
        width=512
    )

    return fig

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

def setup_play(value):
    play = Play('easy', 18, value)
    initial_image = play.get_initial_image()

    image = play.play_instance(model=None, processor=None, input_image=initial_image)
    initial_board_image = image

    fig = px.imshow(initial_board_image)  # Use Plotly's imshow with gray scale
    fig.update_xaxes(showticklabels=False)  # Hide x-axis ticks
    fig.update_yaxes(showticklabels=False)  # Hide y-axis ticks

    return fig



with pento_llava_app:

    gr.HTML(TITLE)

    with gr.Row():
        with gr.Column():    
            main_board = gr.Plot(fig)

        with gr.Column():
            with gr.Row():
                select_board_items = gr.Dropdown(
                    choices=range(512),
                    interactive=True
                )
                
                play_button = gr.Button("Play")  # Add Play button

            with gr.Row():
                 display_string = gr.HTML(value=gen_target_str(0)) 
        

            select_board_items.change(
                fn=gen_new_board,
                inputs=[select_board_items],
                outputs=[main_board],
                queue=True
            )

            select_board_items.change(
                fn=gen_target_str,
                inputs=[select_board_items],
                outputs=[display_string],
                queue=True
            )

            play_button.click(  # Set up button click event
                fn=setup_play,
                inputs=[select_board_items],
                outputs=[main_board],
                queue=True
            )

    pento_llava_app.load()

pento_llava_app.queue()
pento_llava_app.launch()
