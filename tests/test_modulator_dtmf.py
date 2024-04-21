
import sys
sys.path.append('src')


import pytest
from modulators.dtmf import DTMF

import numpy as np


@pytest.fixture
def sampling_rate():
    return 44100 # samples/second


@pytest.fixture
def default_tone_length():
    return 1.0 # s


class TestDtmf:
    # Support methods
    def compute_buffer_length(self, sampling_rate: int, tone_length: float):
        return int(sampling_rate * tone_length)
    
    
    def find_frequencies(self, tone, sampling_frequency):
        length = len(tone)
        # Find peak
        fft_result = np.fft.fft(tone)
        all_freq = np.fft.fftfreq(length, 1/sampling_frequency)
        freq = all_freq[:len(all_freq)//2]
        magnitude = np.abs(fft_result[:len(fft_result)//2])
        epsilon = np.max(magnitude) * 0.9

        peaks = []
        for i in range(len(magnitude)):
            if magnitude[i] > epsilon:
                # print(f"{i} {magnitude[i]} {freq[i]}")
                peaks.append(int(freq[i]))
        return peaks
        
    # Tests
    def test_dtmf_creation(self, sampling_rate):
        try:
            dtmf = DTMF(sampling_rate, 0.1)
            assert True
        except:
            assert False
    
    
    def test_dtmf_null_tone(self, sampling_rate, default_tone_length):
        try:
            dtmf = DTMF(sampling_rate, default_tone_length) 
            null_tone = dtmf.get_tone("XXXX")
            assert len(null_tone) == self.compute_buffer_length(sampling_rate, default_tone_length)
            for n in null_tone:
                assert n == 0
        except:
            assert False
    
    
    def test_dtmf_tones(self, sampling_rate, default_tone_length):
        import matplotlib.pyplot as plt
        try:
            dtmf = DTMF(sampling_rate, default_tone_length)            
            for s in dtmf.tone_symbols.keys():
                tone = dtmf.get_tone(s)
                length = len(tone)
                # Check length
                assert length == self.compute_buffer_length(sampling_rate, default_tone_length)
                # Check frequencies                
                frequency_ids = dtmf.tone_symbols[s]
                if frequency_ids == '--':
                    # Null tone check
                    for n in tone:
                        assert n == 0
                else:
                    # Extract tone frequencies indexes
                    frequency_id1 = int(frequency_ids[0])
                    frequency_id2 = int(frequency_ids[1])
                    # Extract frequencies from DTMF class used to compute the tone
                    assert_frequencies = [dtmf.frequencies_1[frequency_id1], dtmf.frequencies_2[frequency_id2]]
                    # Measure the computed tone with FFT and get the resulting frequencies
                    measured_frequencies = self.find_frequencies(tone, sampling_rate)
                    print(f"Tone: {s} frequencies {assert_frequencies} measured {measured_frequencies}")
                    # Compare the frequencies
                    assert assert_frequencies == measured_frequencies
            assert True
        except:
            assert False

