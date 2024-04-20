import numpy as np
from modulators.abstract_modulator import AbstractModulator


class DTMF(AbstractModulator):
    frequencies_1 = (697, 770, 852, 941) 
    frequencies_2 = (1200, 1336, 1477, 1633)
    tone_symbols = { '1':'00',
                     '2':'01',
                     '3':'02',
                     'a':'03',
                     '4':'10',
                     '5':'11',
                     '6':'12',
                     'b':'13',
                     '7':'20',
                     '8':'21',
                     '9':'22',
                     'c':'23',
                     '*':'30',
                     '0':'31',
                     '#':'32',
                     'd':'33'
                    }
                        
    def __init__(self, sampling_rate, buffer_length) -> None:
        super().__init__()
        self.sampling_rate = sampling_rate
        self.buffer_length = buffer_length
        self.tone_matrix = {}
        self.null_matrix = []
        
        self._init_matrix()
        
    # Private methods
    
    def _init_matrix(self):
        self._compute_tone_matrix()
        self._compute_null_matrix()
        
    
    def _compute_null_matrix(self):
        self.null_matrix = [0] * self.buffer_length
    
    
    def _compute_tone_matrix(self):
        for id1 in range(0, 4):
            for id2 in range(0, 4):
                self.tone_matrix[f"{id1}{id2}"] = self._generate_tone(self.frequencies_1[id1], self.frequencies_2[id2])
    
    
    def _generate_tone(self, frequency_1: int, frequency_2: int):
        tone = [0] * self.buffer_length
        MaxValue = 65535

        # Tone generation
        for i in range(0, len(tone)):
            t = i / float(self.sampling_rate)
            tone[i] = int((MaxValue / 10.0) * (np.sin(2 * np.pi * frequency_1 * t) + np.sin(2 * np.pi * frequency_2 * t)))
            
        # Fading
        fade = 0.0
        fade_limit = np.power(self.buffer_length // 6, 2.0) + (self.buffer_length // 6)
        for i in range(0, self.buffer_length // 5):
            if fade >= 1.0:
                fade = 1.0
            else:
                fade = (np.power(float(i), 2.0) + i) / fade_limit
            tone[i] = tone[i] * fade
            tone[self.buffer_length - 1 - i] = tone[self.buffer_length - 1 - i] * fade
            
        return tone
    
    
    def _write_to_file(self):
        pass
    
    # Public methods
    
    def set_buffer_length(self, buffer_length: int):
        self.buffer_length = buffer_length
        self._init_matrix()
    
    
    def get_tone(self, id: str ) -> any:
        try:
            id_lc = id.lower()
            if id_lc == 'p':
                return self.null_matrix
            else:          
                return self.tone_matrix[self.tone_symbols[id_lc]]
        except KeyError:
            return None

