from fft import fft

# len(coeffs) must be 2^k
def multiply_poly(coeffs1, coeffs2):
    deg1 = len(coeffs1)
    deg2 = len(coeffs2)
    coeffs1 += [0] * (deg2 + 1)
    coeffs2 += [0] * (deg1 + 1)
    pts1 = fft(coeffs1, False)
    pts2 = fft(coeffs2, False)
    ptsmult = []
    for (pt_1, pt_2) in zip(pts1, pts2):
        ptsmult.append(pt_1 * pt_2)
    return [round_j(p / len(ptsmult), 10) for p in fft(ptsmult, True)]



def round_j(x, k):
    return round(x.real, k) + 1j * round(x.imag, k)
