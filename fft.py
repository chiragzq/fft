import cmath

# Evaluate a polynomial at N points in O(N log N)

# P(x) = p0 + p1 x + p2 x^2 + p3 x^3 + p4 x^4 ... pn-1 x^n
#      = (p0 + p2 x^2 + p4 x^4 + ...) + x (p1 + p3 x^2 + p5 x^4 + ...)
#      = P_even(x^2) + x P_odd(x^2) where
# P_even(x) = (p0 + p2 x + p4 x^2 + ...) and P_odd = (p1 + p3 x + p5 x^2 + ...)
# P(-x) is therefore P_even(x^2) - x P_odd (x^2)

# Given coeffs [p0, p1, p2, p3, ... pn] evaluate P(x) 
# If is_inverse is true, uses inverse DFT matrix coefficients
def fft(coeffs, is_inverse):
    while (len(coeffs) & (len(coeffs)-1) != 0) and len(coeffs) != 0:
        coeffs.append(0)
    n = len(coeffs)
    if n == 1:
        return coeffs
    w_0 = cmath.exp((-1 if is_inverse else 1) * 2 * cmath.pi * 1j / n)
    p_odd = []
    p_even = []
    for i, p_i in enumerate(coeffs):
        (p_even if i % 2 == 0 else p_odd).append(p_i)
    ret = [0] * n
    y_e = fft(p_even, is_inverse)
    y_o = fft(p_odd, is_inverse)

    for i in range(n // 2):
        ret[i] = y_e[i] + w_0**i * y_o[i]
        ret[i + n//2] = y_e[i] - w_0**i * y_o[i]
    return ret