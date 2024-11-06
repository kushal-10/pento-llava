import gradio as gr

from src.utils import randomize_board

TITLE = """<h1 align="center" id="space-title"> Pento-LLaVA 🤖🎯🎮</h1>"""

pento_llava_app = gr.Blocks()
fig, targets, info = randomize_board('easy', 18)

target_strs = []
for t in targets:
    target_strs.append(t['target_str'])

def gen_new_board():
    fig, targets, info = randomize_board('easy', 18)
    target_strs = []
    for t in targets:
        target_strs.append(t['target_str'])

    return fig, target_strs

with pento_llava_app:

    gr.HTML(TITLE)

    with gr.Row():
        with gr.Column():    
            main_board = gr.Plot(fig)

        with gr.Column():
            select_target = gr.Dropdown(
                choices = target_strs,
                value=target_strs[0],
                label="Select the target piece",
                allow_custom_value=True
            )
    
    random_button = gr.Button(
        value='Randomize Board'
    )

    random_button.click(
        gen_new_board,
        outputs=[main_board, select_target]
    )


    pento_llava_app.load()

pento_llava_app.queue()
pento_llava_app.launch()


"""
TODOS

Set Board selection - 0-514
(Remove randomization)

...
"""