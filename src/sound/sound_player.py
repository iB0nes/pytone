import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import time
import pygame
import subprocess

from enum import Enum


class SoundPlayer:
    
    def __init__(self, sampling_rate: int, channels: int = 1) -> None:
        pygame.mixer.pre_init(frequency=sampling_rate, size=-16, channels=channels)
        self.sound_playing = None


    def init_mixer(self):
        pygame.init()
        

    def stop(self):
        self.play_buffer.stop()
        self.sound_playing = None
    
        
    def quit_player(self):
        time.sleep(1)
        pygame.quit()
        self.sound_playing = None
    

    def get_sound_buffer(self, rawdata):
        return pygame.mixer.Sound(buffer=rawdata)
    
    
    def tones_buffer_player(self, buffer_list: list[(str, list[int])]) -> None:
        #print(f"playing: {buffer_list[0][0]}", end='', flush=True)
        self.sound_playing = pygame.mixer.Sound.play(buffer_list[0][1])
        for i in range(1, len(buffer_list)):
            while self.sound_playing.get_queue() is not None:
                time.sleep(0.0001)
            #print(buffer_list[i][0], end='', flush=True)
            self.sound_playing.queue(buffer_list[i][1])
        while self.sound_playing.get_sound() is not None:
            time.sleep(0.001)
        #print()
        time.sleep(1)
        pygame.quit()
            
    
    
    def tones_player(self, packed_tones: list[(str, list[int])]) -> None:
        buffer_list = []
        for pt in packed_tones:
            buffer_list.append((pt[0], self.get_sound_buffer(pt[1])))
        self.tones_buffer_player(buffer_list)

