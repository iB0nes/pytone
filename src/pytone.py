# PyTone
# 
# Description:
# A Python software to play audio tones
# 
# License:
# MIT License
# 
# Author:
# Ivano Bonesana
# 
# Date Created:
# 20-apr-2024
# 
# Requirements:
# - Python 3.10
# 
# Usage:
# 
# 
# References:
# 
# ------------------------------------------------------------------------------
# MIT License
# 
# Copyright (c) 2024 I.Bonesana
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ------------------------------------------------------------------------------

import argparse
import time
import struct

from modulators.dtmf import DTMF
from sound.sound_player import SoundPlayer

# import sounddevice as sd

if __name__ == "__main__":

    sampling_rate = 44100
    tone_length = 100
    
    parser = argparse.ArgumentParser(
        prog='PyTone', description='A Python software to play audio tones.', epilog=''
    )
    parser.add_argument("-m", "--message",      type=str, required=True, help="Message to transmit")
    parser.add_argument("-e", "--encoding",     type=str, help="Transmission encoding mode. Default DTMF.", default="DTMF")
    parser.add_argument("-t", "--tone-length",  type=int, help="DTMF tone length in ms. Default 100ms.",    default="100")
    parser.add_argument("-v", '--version',      action='version', version='%(prog)s v1.0.0')
    
    args = parser.parse_args()
    message = args.message
    encoding = args.encoding
    tone_length = args.tone_length/1000.0
    
    print(message)
    print(encoding)
    print(tone_length)
        
    dtmf = DTMF(sampling_rate, tone_length)
    sp = SoundPlayer(sampling_rate)
    
    # sp.init_mixer()
    
    # tone1 = dtmf.get_tone("1")
    # tb1 = struct.pack('<' + 'h' * len(tone1), *tone1) 
    # t1 = sp.get_sound_buffer(tb1)
    
    # tone2 = dtmf.get_tone("2")
    # tb2 = struct.pack('<' + 'h' * len(tone2), *tone2) 
    # t2 = sp.get_sound_buffer(tb2)
    
    # tone3 = dtmf.get_tone("3")
    # tb3 = struct.pack('<' + 'h' * len(tone3), *tone3) 
    # t3 = sp.get_sound_buffer(tb3)

    # tone = tone1 + tone2 + tone3
    # tb = struct.pack('<' + 'h' * len(tone), *tone)
    # t = sp.get_sound_buffer(tb)
    
    # sp.alternative_player([t, t, t, t, t2])
    

