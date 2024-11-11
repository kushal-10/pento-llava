import os
import json
import numpy as np
from grip_env.environment import GridWorldEnv
from PIL import Image
import random
class PlayEpisode():

    def __init__(self, level: str, board_size: int, board_number: int):
        self.level = level
        self.board_size = board_size
        self.board_number = board_number

        metadata_path = os.path.join('src', f'test_{level}.json')

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)

        self.board_num = board_number
        self.board_data = metadata[self.board_num][-1]

        print(self.board_data)

        metadata_obj = self.board_data
        self.info = metadata_obj['info']
        self.agent_start_pos = np.array(metadata_obj['agent_start_pos'])
        self.target_pos = np.array(metadata_obj['target_pos'])

        target_shape = metadata_obj['target_shape']
        target_color = metadata_obj['target_color']
        target_region = self.info[0]['piece_region']

        base_prompt = f"You are at the black dot in the board. The target is the {target_color} {target_shape} piece located at the {target_region}. Your task is to move towards the target and grab it. Predict your next move from up, down, left, right, grip."
        self.prompt = f"USER: <image>\n{base_prompt}. Answer in one word only.\nASSISTANT:"

        self.env = GridWorldEnv(render_mode="rgb_array", size=self.board_size, grid_info=self.info, agent_pos=self.agent_start_pos, target_pos=self.target_pos)
        self.env.reset()
        self.initial_image = self.env.render()
        self.initial_image = Image.fromarray(self.initial_image)

    def get_initial_image(self):
        return self.initial_image

    @staticmethod
    def convert_move_to_step(move_str):
        if move_str == 'up':
            step_val = 3
        elif move_str == 'down':
            step_val = 1
        elif move_str == 'left':
            step_val = 2
        elif move_str == 'right':
            step_val = 0
        else:
            step_val = 4 # Do nothing/Grip

        return step_val

    @staticmethod
    def get_next_position(prediction, predicted_position):
        if prediction == 'right':
            predicted_position[0] += 1
        elif prediction == 'left':
            predicted_position[0] -= 1
        elif prediction == 'up':
            predicted_position[1] -= 1
        elif prediction == 'down':
            predicted_position[1] += 1

        return predicted_position

    def play_instance(self, model=None, processor=None, input_image=None):
        
        # inputs = processor(text=self.prompt, images=[input_image], return_tensors="pt").to("cuda")
        # generated_ids = model.generate(**inputs, max_new_tokens=self.max_len)
        # generated_texts = processor.batch_decode(generated_ids, skip_special_tokens=True)
        
        # # Extract move
        # move = generated_texts[0].split('ASSISTANT:')[-1].strip()
        # print(f"Prompt: {self.prompt}\n\n")
        # print(f"Predicted move: {move}\n\n")
        # move = move.lower()

        move = random.choice(['up', 'down', 'left', 'right', 'grip'])
  
        self.env.step(self.convert_move_to_step(move))
        image = self.env.render()
        image = Image.fromarray(image)

        return image
