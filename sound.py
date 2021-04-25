import math

# Creates a sample with frequency f, length t, and amplitude a
def create_sample(f, t, a, samples):
    ret = []
    for k in range(samples):
        ret.append([t * k / samples, a * math.sin((f * 2 * math.pi) * t * k / samples)])
    return ret
