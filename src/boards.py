from PIL import Image
from grip_env.environment import GridWorldEnv
import os
import json
import numpy as np


class GenerateBoard():

    def __init__(self, level: str, board_size: int, board_number: int):
        self.level = level
        self.board_size = board_size

        metadata_path = os.path.join('src', f'test_{level}.json')

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        self.board_num = board_number
        self.board_data = metadata[self.board_num]
    
    def setup_initial_board(self):

        metadata_obj = self.board_data[-1]
        default_start_pos = np.array(metadata_obj['agent_start_pos'])
        default_target_pos = np.array(metadata_obj['target_pos'])

        info = metadata_obj['info']
        target_options = []
        for piece in info:
            target_info_dict = {}
            target = f"{piece['piece_colour']} {piece['piece_shape']} at {piece['piece_region']}" 
            target_info_dict['target_str'] = target
            target_info_dict['piece_info'] = piece
            target_options.append(target_info_dict)
        
        env = GridWorldEnv(render_mode="rgb_array", size=self.board_size, grid_info=info, agent_pos=default_start_pos, target_pos=default_target_pos)
        env.reset()
        image = env.render()
        image = Image.fromarray(image)

        # Convert all white pixels to gray
        image = image.convert("RGBA")  # Ensure the image has an alpha channel
        data = np.array(image)  # Convert image to numpy array
        # Create a mask for white pixels
        white_pixels = (data[:, :, :3] == [255, 255, 255]).all(axis=2)
        data[white_pixels] = [200, 200, 200, 20]

        image = Image.fromarray(data)  # Convert back to image

        return image, target_options, info

