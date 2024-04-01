"""
Author: Andreas Becker
For Fraunhofer IZFP
Date:09.01.24

Description: 
This Script generates a csv file for a Lookup-table with n_val number of values, 
representing a bipolar Pulse with a duty cycle of d and a frequency of f

"""


import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import os


# Pulse frequency in Hz
f = 50e3
T=1/(f)
# Amplitude in %
A = 100
# total number of samples
n_val = 8
# timevector for signal
t= np.arange(0-(T/n_val), T+(T/n_val), (T/n_val))


#desired filename for the csv-file
filename = 'Unipolarer Puls' +'.csv'

def GeneratePulse(f, A, n_val):

    holdoff_t = np.array([])
    values = np.zeros(n_val)
    holdoff_t=(np.repeat((T/n_val),n_val))
    values = (A/2) * sp.signal.square(2 * np.pi * f* t)+(A/2)
    
    
    return values, holdoff_t, t

def plot(values, holdoff_t, t):
    values[0]=0
    values[len(values)-1]=0
    plt.rcParams['figure.dpi'] = 160
    plt.figure(1, figsize=([5,4]))
    plt.plot(t*1e6,values, linestyle='-', drawstyle='steps-post')
    plt.grid('on')
    plt.title('waveform')
    plt.xlabel('time in µs')
    plt.ylabel('Amplitude')
    plt.savefig(filename.removesuffix('.csv')+'.png',format='png')
    
def MakeCsvFile(values, t, filename):
        t= np.round(holdoff_t*1e6, decimals=6)
        np.savetxt(filename, np.column_stack((values, values, t)), delimiter=" ,  ", fmt='%s')


                
values, holdoff_t, t = GeneratePulse(f, A, n_val)

print((1/(holdoff_t[0]*n_val)))

plot(-values, holdoff_t, t)
path = r'O:\BA\LUTs'
os.chdir(path)
#MakeCsvFile(values, holdoff_t, filename)
