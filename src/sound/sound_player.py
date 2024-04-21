# import sounddevice as sd
# import soundfile as sf

# data, samplerate = sf.read('dtmf.wav')

# sd.play(data, samplerate)


# from playsound import playsound
# playsound('dtmf.wav')


# import time
# import pygame

# pygame.mixer.init()
# print(pygame.mixer.music.get_pos())
# pygame.mixer.music.load("dtmf.wav")
# print(pygame.mixer.music.get_pos())
# pygame.mixer.music.play()
# print(pygame.mixer.music.get_pos())

# while pygame.mixer.music.get_busy():
#     print(pygame.mixer.music.get_busy())
#     time.sleep(1)
# print(pygame.mixer.music.get_busy())

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import time
import pygame
import subprocess

from enum import Enum

# rawdata1 = subprocess.check_output([
#     'sox', '-n', '-b', '16', '-e', 'signed', '-r', '44100',
#     '-c', '1', '-t', 'raw', '-', 'synth', '0.5', 'sin', '440'])

# rawdata2 = subprocess.check_output([
#     'sox', '-n', '-b', '16', '-e', 'signed', '-r', '44100',
#     '-c', '1', '-t', 'raw', '-', 'synth', '0.75', 'sin', '880'])

# rawdata3 = subprocess.check_output([
#     'sox', '-n', '-b', '16', '-e', 'signed', '-r', '44100',
#     '-c', '1', '-t', 'raw', '-', 'synth', '0.5', 'sin', '1760'])

# pygame.mixer.pre_init(frequency=44100, size=-16, channels=1)
# pygame.init()

# beep1 = pygame.mixer.Sound(buffer=rawdata1)
# beep2 = pygame.mixer.Sound(buffer=rawdata2)
# beep3 = pygame.mixer.Sound(buffer=rawdata3)

# print(beep1.get_length())
# s1 = pygame.mixer.Sound.play(beep1)
# s2 = s1.queue(beep2)

# while s1.get_queue() is not None:
#     print(s1.get_queue())
#     print(s1.get_sound())
#     print("-------------")
#     time.sleep(0.250)
    
# s3 = s1.queue(beep3)

# while s1.get_queue() is not None:
#     print(s1.get_queue())
#     print(s1.get_sound())
#     print("-------------")
#     time.sleep(0.250)
    
# s1.queue(beep2)


# while s1.get_queue() is not None:
#     print(s1.get_queue())
#     print(s1.get_sound())
#     print("-------------")
#     time.sleep(0.250)
    
# s1.queue(beep1)

# while s1.get_sound() is not None:
#     print(s1.get_queue())
#     print(s1.get_sound())
#     print("-------------")
#     time.sleep(0.250)

# time.sleep(1)
# pygame.quit()



class SoundPlayerState(Enum):
    IDLE = 0
    INITIALIZED = 1
    PLAYING = 2


class SoundPlayer:
    
    def __init__(self, sampling_rate: int, channels: int = 1) -> None:
        pygame.mixer.pre_init(frequency=sampling_rate, size=-16, channels=channels)
        self.state = SoundPlayerState.IDLE
        self.sound_playing = None

    def init_mixer(self):
        pygame.init()
        self.state = SoundPlayerState.INITIALIZED
        
    def play_buffer(self, buffer):
        if self.state == SoundPlayerState.IDLE:
            print("- idle")
            return False
        elif self.state == SoundPlayerState.INITIALIZED:
            print("- init")
            self.state = SoundPlayerState.PLAYING
            self.sound_playing = pygame.mixer.Sound.play(buffer)
            return True
        else:
            return False

    def queue_buffer(self, buffer):
        if self.state == SoundPlayerState.PLAYING:
            print("- play")
            if self.sound_playing.get_queue() is None:
                self.sound_playing.queue(buffer)
                return True
        return False


    def queue_last_buffer(self, buffer):
        if self.queue_buffer(buffer):
            while self.sound_playing.get_sound() is not None:
                time.sleep(0.01)     
            self.quit_player()       
            return True
        return False
            

    def get_sound_buffer(self, rawdata):
        return pygame.mixer.Sound(buffer=rawdata)


    def stop(self):
        self.play_buffer.stop()
        self.sound_playing = None
    
        
    def quit_player(self):
        time.sleep(1)
        pygame.quit()
        self.sound_playing = None
        self.state = SoundPlayerState.IDLE
    
    
    def alternative_player(self, buffer_list):        
        self.sound_playing = pygame.mixer.Sound.play(buffer_list[0])
        for i in range(1, len(buffer_list)):
            while self.sound_playing.get_queue() is not None:
                time.sleep(0.01)
            self.sound_playing.queue(buffer_list[i])
        while self.sound_playing.get_sound() is not None:
            time.sleep(0.001)
        time.sleep(1)
        pygame.quit()
            
