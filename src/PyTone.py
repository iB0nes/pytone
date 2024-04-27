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
# PyTone [-h] -m MESSAGE [-e ENCODING] [-t TONE_LENGTH] [-f FADING] [-v]
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

from str2bool import str2bool

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
    parser.add_argument("-f", "--fading",       type=str, help="Enable or disable tone fading.",            default="true")
    parser.add_argument("-v", '--version',      action='version', version='%(prog)s v1.0.0')
    
    args = parser.parse_args()
    message = args.message
    encoding = args.encoding
    tone_length = args.tone_length/1000.0
    fading = str2bool(args.fading)
    
    print(f"message:   {message}")
    print(f"encoding:  {encoding}")
    print(f"tone len.: {tone_length}")
    print(f"fading:    " + "yes" if fading else "no")
        
    dtmf = DTMF(sampling_rate, tone_length, fading=fading)
    sp = SoundPlayer(sampling_rate)
    
    encoded_msg = dtmf.encode_message_and_pack(message)
    sp.init_mixer()
    sp.tones_player(encoded_msg)
    
    print("complete")

