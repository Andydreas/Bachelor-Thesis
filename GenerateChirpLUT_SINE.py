"""
Author: Andreas Becker
For Fraunhofer IZFP
Date: 17.03.24

Description: 
This Script generates a csv file for a Lookup-table with n_val number of values, 
representing a stepped sine wave with a linear frequency sweep from f1 to f2
for a set number of values per period (n_prd).
Plots are generated for Inspection of the Waveform's Properties
"""

import matplotlib.pyplot as plt
import numpy as np


# start frequency in Hz
f1 = 25e3
# stop frequency in Hz
f2 = 75e3
# Amplitude in %
A = 100
# total number of samples
n_val = 1024
# total number of values per period
n_prd = 64
#desired filename for the csv-file
filename = 'Sinus Chirp von '+ str(f1/1e3) + 'kHz nach ' + str(f2/1e3) + 'kHz'

def GenerateChirp(f1, f2, A, n_val, n_prd):
    
    #local variables and Arrays
    start_t = 0
    holdoff_t = np.array([])
    t = np.array([])
    values = np.array([])
    
    # calculation of possible number of frequencies
    freqs = int(n_val / n_prd)
    print('possible number of frequencies: ', freqs)
    
    # stepped modulated holdoff-times for frequency modulation
    f_mod = np.linspace(f1, f2, int(freqs))
    # time vector for sinusoid period
    t_prd = np.linspace(0, 1-(1/n_prd), int(n_prd))
    
    # generating waveform

    for f in f_mod:
        T = 1 / f
        T_i = (T / n_prd)
        end_t = start_t + T - (T / n_prd)
        holdoff_t = np.concatenate([holdoff_t, np.repeat(T_i, n_prd)])
        t_i = np.linspace(start_t, end_t, n_prd)
        t = np.concatenate([t, t_i])
        if f==f_mod[len(f_mod)-1]:
            t_prd=np.linspace(0, 1, int(n_prd))
        values = np.concatenate([values, A * np.sin(2 * np.pi * t_prd)])
        values = np.round(values, decimals=8)
        start_t = end_t
        
    return values, f_mod, holdoff_t, t

def plot(y, x, holdoff_t, t):
    # set the figure Properties
    plt.rcParams['figure.dpi'] = 560
    plt.figure(1, figsize=[10,7.5])
    plt.subplots_adjust(hspace=0.5,wspace=0.5)

    #signal-waveform
    ax0 = plt.subplot2grid((3, 5), (0, 0), colspan=4, rowspan=1)
    ax0.set_title('waveform')
    ax0.set_ylabel('Amplitude [%]')
    ax0.grid('on')
    ax0.plot(y[0:n_prd+1], linestyle='-', drawstyle='steps-post')
    
    #holdoff-times
    ax1 = plt.subplot2grid((3, 5), (1, 0), colspan=4, rowspan=1)
    ax1.set_title('holdoff times')
    ax1.set_ylabel('time in us',labelpad=26)
    ax1.set_yticks(np.arange(1e-7,7e-7, 1e-7 ))
    ax1.grid('on')
    ax1.plot(holdoff_t, 'r', drawstyle='steps-post')
    
    #frequencies contained in the signal
    ax2 = plt.subplot2grid((3, 5), (2, 0), colspan=4, rowspan=1)
    ax2.set_title('frequencies')
    ax2.set_xlabel('samples')
    ax2.set_ylabel('frequency in kHz',labelpad=18)
    ax2.set_yticks(np.linspace(f1/1e3, f2/1e3, 6))
    ax2.grid('on')
    ax2.plot(np.repeat(x/1e3, n_prd), 'b', drawstyle='steps-post')
    
    #Plot of the complete signal
    ax3 = plt.subplot2grid((3, 5), (0, 4), colspan=1, rowspan=3)
    ax3.grid('on')
    ax3.set_title('SQW-chirp')
    ax3.yaxis.set_label_position("right")
    ax3.set_ylabel('time in µs',loc='center')
    ax3.set_xlabel('Amplitude [%]')
    ax3.plot(y, t*(10**6), linestyle='-', drawstyle='steps-post')
    
    plt.savefig(filename +'.png',format='png')
    plt.show()
    
def MakeCsvFile(values, t, filename):
        t= np.round(holdoff_t*(10**6), decimals=3)
        np.savetxt(filename+'.csv', np.column_stack((values, values, t)), delimiter=" ,  ", fmt='%s')
                
values, f_mod, holdoff_t, t = GenerateChirp(f1, f2, A, n_val, n_prd)
plot(values, f_mod, holdoff_t, t)
MakeCsvFile(values, holdoff_t, filename)
