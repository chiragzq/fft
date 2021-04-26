import math
from fft import fft
import librosa
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as tick

import numpy as np

# Creates a sample with frequency f, length t, and amplitude a
def create_sample(f, t, a, samples):
    ret = []
    for k in range(samples):
        ret.append([t * k / samples, a * math.sin((f * 2 * math.pi) * t * k / samples)])
    return ret


def read_mp3(path):
    y, sr = librosa.load(path, None)
    return y.tolist(), sr

# sample_window in ms
def convert_audio_to_spectrogram_data(amps, sample_rate, sample_window=1000, frequency_range=18000, frequency_buckets=1000):
    sample_window_size = int(sample_window / 1000 * sample_rate)
    amps = [amps[i:i + sample_window_size] for i in range(0, len(amps), sample_window_size)]
    y = []
    for i, amp_data in enumerate(amps):
        print(i)
        fft_data = [abs(x) / len(amp_data) for x in fft(amp_data, False)]
        fft_data = fft_data[:len(fft_data)//2]
        freq_bucket_size = frequency_range // frequency_buckets
        res2 = []
        for j in range(frequency_buckets):
            tot = 0
            for k in range(j * freq_bucket_size, (j + 1) * freq_bucket_size):
                if k >= len(fft_data):
                    break
                tot += fft_data[k]
            ratio = tot / freq_bucket_size
            if ratio <= 0:
                ratio = 1e-10
            res2.append(20 * math.log10(ratio))
        # print(res2)
        y.append(res2)
    return np.flip(np.array(y).T,0)

def convert_spectrogram_data_to_img(data, max_freq=18000, sample_window=1000):
    print(data.shape)
    norm = mpl.colors.Normalize(vmin=-120, vmax=0)
    plt.style.use("dark_background")
    fig, (ax1) = plt.subplots(1)
    pos = ax1.imshow(data, cmap=plt.cm.turbo, norm=norm, aspect='auto', extent=[0, sample_window / 1000 * data.shape[1], 0, max_freq])
    fig.colorbar(pos, ax=ax1)
    plt.gca().xaxis.set_major_formatter(tick.FormatStrFormatter('%d s'))
    plt.gca().yaxis.set_major_formatter(tick.FormatStrFormatter('%d Hz'))
    plt.show()

def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

print(plt.cm.turbo)