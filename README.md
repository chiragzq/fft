# FFT

Implementation of Cooley-Tukey FFT in python and some applications 

### Fast Polynomial Multiplication

![Diagram of FFT multiplication](https://i.imgur.com/Xejz8v8.png)

```py
poly1 = [-3, 4, 8]
poly2 = [-1, -2, 5]
res = multiply_poly(poly1, poly2)
print("Multiplying (" + str_poly(poly1) + ") * (" + str_poly(poly2)  + ")")
print(str_poly_i(res)) 
```
```
Multiplying (-3x^0 + 4x^1 + 8x^2) * (-1x^0 + -2x^1 + 5x^2)
3.0x^0 + 2.0x^1 + -31.0x^2 + 4.0x^3 + 40.0x^4
```

### Converting time domain signal to frequency domain

![Sum of 30Hz signal of amplitude 5 and 5Hz signal of amplitude 1, with sample rate 1024Hz](https://i.imgur.com/59fzb2h.png)
Sum of 30Hz signal of amplitude 5 and 5Hz signal of amplitude 1, with sample rate 1024Hz


![One second sample from a song](https://i.imgur.com/sqqkvvs.png)
One second sample from a song

### Spectrogram from file

![Spectrogram of a beep used to censor a word](https://i.imgur.com/C8nYhys.png)
Spectrogram of a beep used to censor a word

![Spectrogram of a 440Hz tone of amplitude 10^-5 created in mathematica](https://i.imgur.com/oaBzMJQ.png)
Spectrogram of a 440Hz tone of amplitude 10<sup>-5</sup> created in mathematica

![](https://i.imgur.com/B1amUaM.png)
Spectrogram of a full song