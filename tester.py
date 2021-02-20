import math

def loc_angle(c, a, b):
    numerator = math.pow(c, 2) - math.pow(a, 2) - math.pow(b, 2)
    denominator = -2*a*b
    frac = numerator / denominator
    result = math.acos(frac)
    return math.degrees(result)

print(loc_angle(5, 4, 3))