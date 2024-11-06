import gradio as gr
import numpy as np
import matplotlib.pyplot as plt

from src.boards import GenerateBoard

TITLE = """<h1 align="center" id="space-title"> Pento-LLaVA 🤖🎯🎮</h1>"""

initial_board_image, target_positions, info = GenerateBoard('easy', 18).setup_initial_board() 

# Convert initial_board_image to a matplotlib figure
fig, ax = plt.subplots()
ax.imshow(initial_board_image)
ax.axis('off')

pento_llava_app = gr.Blocks()

with pento_llava_app:

    gr.HTML(TITLE)
    gr.Plot(fig)

    pento_llava_app.load()

pento_llava_app.queue()
pento_llava_app.launch()