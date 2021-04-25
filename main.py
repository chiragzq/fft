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

# no padded zeros! they make everything slower
def multiply(coeffs1, coeffs2):
    deg1 = len(coeffs1)
    deg2 = len(coeffs2)
    coeffs1 += [0] * (deg2 + 1)
    coeffs2 += [0] * (deg1 + 1)
    pts1 = fft(coeffs1, False)
    pts2 = fft(coeffs2, False)
    print(len(pts1))
    ptsmult = []
    for (pt_1, pt_2) in zip(pts1, pts2):
        ptsmult.append(pt_1 * pt_2)
    return [round_j(p / len(ptsmult), 15) for p in fft(ptsmult, True)]

def round_j(x, k):
    return round(x.real, k) + 1j * round(x.imag, k)

print(multiply([2,3,1],[1,0,2]))
# print(fft(fft([5,3,2,1], False), True))
