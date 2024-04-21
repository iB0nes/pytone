import numpy as np
from modulators.abstract_modulator import AbstractModulator


class DTMF(AbstractModulator):
    frequencies_1 = (697,  770,  852,  941 ) 
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
                     'd':'33',
                     'p':'--'
                    }
    
                        
    def __init__(self, sampling_rate: int, tone_length: float) -> None:
        super().__init__()
        self.sampling_rate = sampling_rate
        self.tone_length = tone_length
        self.buffer_length = int(sampling_rate * tone_length)
        self.tone_matrix = {}
        self.null_matrix = []
        
        self._init_matrix()
        
    # Private methods
    
    def _init_matrix(self) -> None:
        self._compute_null_matrix()
        self._compute_tone_matrix()
        
    
    def _compute_null_matrix(self) -> None:
        self.null_matrix = np.zeros(self.buffer_length, dtype=np.uint16)
    
    
    def _compute_tone_matrix(self) -> None:
        self.tone_matrix['--'] = self.null_matrix
        for id1 in range(0, 4):
            for id2 in range(0, 4):
                self.tone_matrix[f"{id1}{id2}"] = self._generate_tone(self.frequencies_1[id1], self.frequencies_2[id2])
    
    
    def _generate_tone(self, frequency_1: int, frequency_2: int) -> list[int]:
        tone = [0] * self.buffer_length
        MaxValue = 32767

        # Tone generation
        for i in range(0, len(tone)):
            t = i / float(self.sampling_rate)
            tone[i] = np.int16((MaxValue / 10.0) * (np.sin(2 * np.pi * frequency_1 * t) + np.sin(2 * np.pi * frequency_2 * t)))
            
        # Fading
        fade = 0.0
        fade_limit = np.power(self.buffer_length // 6, 2.0) + (self.buffer_length // 6)
        for i in range(0, self.buffer_length // 5):
            if fade >= 1.0:
                fade = 1.0
                break
            else:
                fade = (np.power(float(i), 2.0) + i) / fade_limit
            tone[i] = np.int16(tone[i] * fade)
            tone[self.buffer_length - 1 - i] = np.int16(tone[self.buffer_length - 1 - i] * fade)
        
        return tone
    
    
    # Public methods
    
    def set_buffer_length(self, buffer_length: int) -> None:
        self.buffer_length = buffer_length
        self._init_matrix()
    
    
    def get_tone(self, tone_symbol: str ) -> list[int]:
        try:
            id = tone_symbol.lower()  
            return self.tone_matrix[self.tone_symbols[id]]
        except KeyError:
            return self.null_matrix

