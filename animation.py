import pygame

class Animation:
    def __init__(self):
        self.all_images = {}
        self.animation_data = {}
        self.animation_data['walk'] = self.load_animation("assets/sprites/Player/walk", [5, 5, 5, 5])
        self.animation_data['idle'] = self.load_animation("assets/sprites/Player/idle", [20, 20, 40, 20])
        self.animation_data['jump'] = self.load_animation("assets/sprites/Player/jump", [1])
        self.animation_data['fall'] = self.load_animation("assets/sprites/Player/fall", [1])
        self.current_frame = 0
    
    
    def load_animation(self, path, durations):
        animation = []
        animation_name = path.split('/')[-1]
        frame_index = 0
        for frames in durations:
            img_name = animation_name + "_" + str(frame_index)
            img_path = path + "/" + img_name + ".png"
            image = pygame.image.load(img_path)
            self.all_images[img_name] = image.copy()
            for frame in range(frames):
                animation.append(img_name)
            frame_index += 1
        return animation
    

    def change_action(self, action, frame, new_action):
        if action != new_action:
            action = new_action
            frame = 0
        return action, frame
