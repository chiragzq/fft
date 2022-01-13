#include <stdio.h>
#include <iostream>

#include <cmath>
#include <complex>
#include <chrono>

typedef std::complex<double> complex;

template <typename T>
struct identity_t { typedef T type; };

/// Make working with std::complex<> nubmers suck less... allow promotion.
#define COMPLEX_OPS(OP)                                                 \
  template <typename _Tp>                                               \
  std::complex<_Tp>                                                     \
  operator OP(std::complex<_Tp> lhs, const typename identity_t<_Tp>::type & rhs) \
  {                                                                     \
    return lhs OP rhs;                                                  \
  }                                                                     \
  template <typename _Tp>                                               \
  std::complex<_Tp>                                                     \
  operator OP(const typename identity_t<_Tp>::type & lhs, const std::complex<_Tp> & rhs) \
  {                                                                     \
    return lhs OP rhs;                                                  \
  }
COMPLEX_OPS(+)
COMPLEX_OPS(-)
COMPLEX_OPS(*)
COMPLEX_OPS(/)
#undef COMPLEX_OPS

#define PI 3.1415192653589793238460
#define j complex(0, 1)

// fft in place
extern "C" void fft_recur(complex* signal, int n) {
    if(n == 1)
        return; // base case, fourier trasnform of 1 element is itself
    // divide
    complex* even = new complex[n / 2];
    complex* odd = new complex[n / 2];
    for(int i = 0; i < n / 2; i++) {
        even[i] = signal[2 * i];
        odd[i] = signal[2 * i + 1];
    }

    // and conquer
    fft_recur(even, n / 2);
    fft_recur(odd, n / 2);

    for(int i = 0;i < n / 2; i++) {
        complex w = std::exp(complex(0, -2.0 * i * PI / n)); 

        signal[i] = even[i] + w * odd[i]; // calculate full fourier transform by combining even and odd indexed transforms
        signal[i + n/2] = even[i] - w * odd[i];
    }
    free(even);
    free(odd);
}

extern "C" void fft(double* data, int n) {
    complex* signal = new complex[n];
    for (int i = 0; i < n; i++) {
        signal[i] = complex(data[i], 0);
    }
    fft_recur(signal, n);
    for (int i = 0; i < n; i++) {      
        data[i] = abs(signal[i]);
    }
}

double* blackman(int n) {
    double* window = new double[n];
    for(int i = 0; i < n; i++) {
        // window[i] = 0.42 - 0.5 * cos(2 * PI * i / (n - 1)) + 0.08 * cos(4 * PI * i / (n - 1));
        window[i] = 0.5434 - (1 - 0.5434) * cos(2 * PI * i / (n - 1));
    }
    return window;
}

extern "C" void spectrogram(double* data, int n, int sampleRate, int windowBits, double* spectrogram) {
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();

    int windowSize = 1 << windowBits;
    int chunks = n / windowSize + 1;
    complex* chunk = new complex[windowSize];

    double* blackmanFn = blackman(windowSize);
    double windowSum = 0;
    for(int i = 0; i < windowSize; i++) {
        windowSum += blackmanFn[i] * 1.1;
    }

    for(int i = 0; i < chunks; i++) {
        std::cout << "\r" << ((double)i * windowSize / sampleRate) << std::flush;
        if(i != chunks - 1) {
            for(int jj = 0; jj < windowSize; jj++) {
                chunk[jj] = data[i * windowSize + jj] * blackmanFn[jj];
            }
        } else {
            for(int jj = 0; jj < windowSize; jj++) {
                chunk[jj] = 0;
            }
            for(int jj = i * windowSize; jj < n; jj++) {
                chunk[jj - i * windowSize] = data[jj] * blackmanFn[jj - i * windowSize];
            }
        }
        fft_recur(chunk, windowSize);
        for(int k = 0; k < windowSize / 2; k++) {
            double mag = (chunk[k].real() * chunk[k].real() + chunk[k].imag() * chunk[k].imag()) / (windowSum * windowSum);   
            if(mag < 1e-12) {
                mag = 1e-12;
            }
            spectrogram[i * windowSize / 2 + (-k + windowSize / 2)] = 10 * log10(mag);
        }
    }
    std::cout << std::endl;
    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << std::chrono::duration_cast<std::chrono::milliseconds>(end - begin).count() << "[ms]" << std::endl;

    free(chunk);
}