import cmath

# Evaluate a polynomial at N points in O(N log N)

# P(x) = p0 + p1 x + p2 x^2 + p3 x^3 + p4 x^4 ... pn-1 x^n
#      = (p0 + p2 x^2 + p4 x^4 + ...) + x (p1 + p3 x^2 + p5 x^4 + ...)
#      = P_even(x^2) + x P_odd(x^2) where
# P_even(x) = (p0 + p2 x + p4 x^2 + ...) and P_odd = (p1 + p3 x + p5 x^2 + ...)
# P(-x) is therefore P_even(x^2) - x P_odd (x^2)

# Given coeffs [p0, p1, p2, p3, ... pn] evaluate P(x) 
# If is_inverse is true, uses inverse DFT matrix coefficients
def fft_recur(coeffs, is_inverse):
    n = len(coeffs)
    if n == 1:
        return coeffs # fourier transform of constant is itself
    w_0 = cmath.exp((-1 if is_inverse else 1) * 2 * cmath.pi * 1j / n) # find roots of unity
    p_even = [coeffs[2 * i] for i in range((len(coeffs) + 1) // 2)] # split even and odd indexed samples
    p_odd = [coeffs[2 * i + 1] for i in range(len(coeffs) // 2)]

    ret = [0] * n
    y_e = fft_recur(p_even, is_inverse) # calculate fft over even and odd split (log N recursive step)
    y_o = fft_recur(p_odd, is_inverse)

    for i in range(n // 2):
        w = w_0**i
        ret[i] = y_e[i] + w * y_o[i] # calculate full fourier transform by combining even and odd indexed transforms
        ret[i + n//2] = y_e[i] - w * y_o[i]
    return ret

def fft(coeffs, is_inverse): # make sure that the length of the input is a power of 2
    n = len(coeffs)
    power = 1
    while power < n:
        power *= 2
    coeffs += [0] * (power - n)
    # print(coeffs)
    return fft_recur(coeffs, is_inverse)
