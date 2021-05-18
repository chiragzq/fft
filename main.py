from fft import fft
from multiply_poly import multiply_poly
from sound import create_sample, read_mp3, convert_audio_to_spectrogram_data, convert_spectrogram_data_to_img

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def example_mult_poly():
    poly1 = [-3, 4, 8]
    poly2 = [-1, -2, 5]
    print("Multiplying (" + str_poly(poly1) + ") * (" + str_poly(poly2)  + ")")
    res = multiply_poly(poly1, poly2)
    print(str_poly_i(res)) 

# list of coeffs to string
def str_poly(poly):
    s = []
    for (i, coeff) in enumerate(poly):
        if coeff != 0:
            s.append(str(coeff) + "x^" + str(i))
    return " + ".join(s)

# list of imaginary coeffs to string
def str_poly_i(poly):
    s = []
    for (i, coeff) in enumerate(poly):
        if coeff.real != 0:
            s.append(str(coeff.real) + "x^" + str(i))
    return " + ".join(s)

def example_fft_sound():
    sample = create_sample(30,1,5,1024)
    sample2 = create_sample(5,1,1,1024)

    t_data = [pt[0] for pt in sample]
    a_data = [pt1[1] + pt2[1] for pt1,pt2 in zip(sample,sample2)]

    fig, (ax1, ax2) = plt.subplots(2,1)
    ax1.plot(t_data, a_data)


    res = [abs(x) for x in fft(a_data, False)]
    res = res[:len(res)//2]

    ax2.plot(range(len(res)), res)
    plt.show()

def example_fft_file():
    y, sr = read_mp3("music/Zero Percent.mp3")
    t_data = [x / sr for x in range(len(y))]
    t_data = t_data[sr:sr+sr]
    a_data = y[sr:sr+sr]

    fig, (ax1, ax2) = plt.subplots(2,1)
    ax1.plot(t_data, a_data)

    res = [abs(x) for x in fft(a_data, False)]
    res = res[:len(res)//2]

    ax2.plot(range(len(res)), res)
    plt.show()

def example_spectrogram():
    y, sr = read_mp3("music/Zero Percent.mp3")
    data = convert_audio_to_spectrogram_data(y, sr)
    convert_spectrogram_data_to_img(data)

example_spectrogram()