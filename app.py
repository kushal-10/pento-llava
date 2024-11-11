import gradio as gr
import numpy as np
import plotly.graph_objects as go

from src.utils import select_board

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


    pento_llava_app.load()

pento_llava_app.queue()
pento_llava_app.launch()
