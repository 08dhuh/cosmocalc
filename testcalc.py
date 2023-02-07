import numpy as np
import sys
import mpmath
import math

arguments = sys.argv[1:]
H0 = float(arguments[0])
omega_M = float(arguments[1])
omega_Lambda = float(arguments[2])
omega_rad = float(arguments[3])
w = float(arguments[4])
wa = float(arguments[5])
z = arguments[6]
args = [float(a) for a in arguments]
print(args)

# print(arguments[0])
# print(sys.argv[2])
# print(sys.argv)
