#!/usr/bin/env python3
import random
import math
import cmath
import numpy as np
from PIL import Image

# Grid and square settings
n_rows, n_cols = 512, 512   # Number of rows and columns
square_size = 2          # Side length of each square in pixels

# SVG canvas size
width, height = n_cols * square_size, n_rows * square_size

# Make 2D array with random Fourier components
A = np.zeros((n_rows,n_cols), dtype=complex)

grayRange = np.array([0,1])

# Important Constants
oscillators = 6
d = 0.0255
xc = 0.5
xpos = np.array([xc - 2.5*d, xc - 1.5*d, xc - 0.5*d, xc + 0.5*d, xc + 1.5*d, xc + 2.5*d])
#xpos = np.array([xc - d, xc, xc + d])
BeamSteer = -0.4
BeamFocus = 0
phaseOffset = np.array([0, BeamSteer*math.pi, 2*BeamSteer*math.pi, 3*BeamSteer*math.pi, 4*BeamSteer*math.pi, 5*BeamSteer*math.pi])

kvec = 20

for k in range(0,oscillators):
    x0 = xpos[k]
    y0 = 0.5 # always same
    print(f'voortgang "{(k/oscillators)*100}" procent', end='\r')
    
    for i in range(n_rows):
        for j in range(n_cols):
            r_square = ((i/n_rows)-y0)**2 + ((j/n_cols) - x0)**2
            A[i,j] += cmath.exp(1j*(2*math.pi*kvec*math.sqrt( r_square ) + phaseOffset[k]) )

B = np.multiply(A, np.matrix.conjugate(A))
#B = np.square(np.absolute(A)) 
print(B)               
B -= np.min(B) # shift whole thing to above zero
Anorm = B/np.max(B) # normalize
Afinal = Anorm*(grayRange[1] - grayRange[0]) + grayRange[0] # squeeze to interval grayRange

# convert to 16 bit uint for png: 
Afinal1 = (Afinal*65536).astype(np.uint16)

# save as 16 bit png (8 bit is te weinig, dan heb je 256 levels wat resulteert in terrasvorming)
image = Image.fromarray(Afinal1, mode = 'I;16')
image.save('Waves4Steer_power6.png')
