
import sys
sys.path.append('src')


import pytest
from modulators.dtmf import DTMF

@pytest.fixture
def sampling_buffer_length():
    sampling_rate = 44100 # samples/second
    tone_length = 1       # s
    return int(tone_length * sampling_rate)


class TestDtmf:
    
    def test_dtmf_creation(self, sampling_buffer_length):
        try:
            dtmf = DTMF(44100, sampling_buffer_length)
            assert True
        except:
            assert False

