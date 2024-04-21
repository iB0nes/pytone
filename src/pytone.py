

import numpy as np
import matplotlib.pyplot as plt

from modulators.dtmf import DTMF


def find_frequencies(tone, epsilon=1e+08):
    length = len(tone)
    # Find peak
    fft_result = np.fft.fft(tone)
    all_freq = np.fft.fftfreq(length, 1/sampling_rate)
    freq = all_freq[:len(all_freq)//2]
    magnitude = np.abs(fft_result[:len(fft_result)//2])

    peaks = []
    for i in range(len(magnitude)):
        if magnitude[i] > epsilon:
            print(f"{i} {magnitude[i]} {freq[i]}")
            peaks.append(int(freq[i]))
    return peaks



#if __name__ == "__main__":
sampling_rate = 44100
default_tone_length = 1.0

dtmf = DTMF(sampling_rate, default_tone_length)
tone = dtmf.get_tone('2')
print(find_frequencies(tone))



