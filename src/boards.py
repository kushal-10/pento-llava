from PIL import Image
from grip_env.environment import GridWorldEnv
import os
import json
import numpy as np


class GenerateBoard():

    def __init__(self, level: str, board_size: int):
        self.level = level
        self.board_size = board_size

        metadata_path = os.path.join('src', f'test_{level}.json')

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        num_boards = len(metadata)
        random_board_num = np.random.randint(0, num_boards)
        self.board_data = metadata[random_board_num]
    
    def setup_initial_board(self):

        metadata_obj = self.board_data[-1]
        default_start_pos = np.array(metadata_obj['agent_start_pos'])
        default_target_pos = np.array(metadata_obj['target_pos'])

        info = metadata_obj['info']
        target_options = []
        for piece in info:
            target = f"{piece['piece_colour']} {piece['piece_shape']} at {piece['piece_region']}" 
            target_options.append(target)


        
        env = GridWorldEnv(render_mode="rgb_array", size=self.board_size, grid_info=info, agent_pos=default_start_pos, target_pos=default_target_pos)
        env.reset()
        image = env.render()
        image = Image.fromarray(image)

        return image, target_options, info

