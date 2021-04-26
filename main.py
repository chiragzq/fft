from fft import fft
from multiply_poly import multiply_poly
from sound import create_sample, read_mp3, convert_audio_to_spectrogram_data, convert_spectrogram_data_to_img

import numpy as np
import matplotlib.pyplot as plt

def example_mult_poly():
  print(multiply_poly([5,-3,2,14,-26,1,-2],[1,-2,9,6,-4,3,-6])) 
  print(fft(fft([5,3,2,1], False), True))

def example_fft_sound():
    sample = create_sample(30,1,5,1000)
    sample2 = create_sample(50,1,1,1000)

    t_data = [pt[0] for pt in sample]
    a_data = [pt1[1] + pt2[1] for pt1,pt2 in zip(sample,sample2)]

    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.plot(t_data, a_data)

    res = [abs(x) for x in fft(a_data, False)]
    res = res[:len(res)//2]

    ax2.plot(range(len(res)), res)
    plt.show()

def example_spectrogram():
    y, sr = read_mp3("music/beep.mp3")
    data = convert_audio_to_spectrogram_data(y, sr)
    convert_spectrogram_data_to_img(data)

example_spectrogram()