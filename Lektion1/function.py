import matplotlib.pyplot as plt
import pandas as pd
from scipy import fftpack
import numpy as np

data = np.array(pd.read_csv("electric_signals.csv"))

num_rows,num_columns = data.shape
fig, ax = plt.subplots(num_rows)
for i, row in enumerate(data):
    ax[i].plot(np.arange(num_columns),row)
    ax[i].set(xlabel = "Time [t]", ylabel = "Amplitude")
plt.show()

fourier_transformed_matrix = np.abs(fftpack.fft(data)[:,:num_columns//2])*2/num_columns
xf = np.linspace(0.0, int(num_columns/2), int(num_columns/2))
fig, ax = plt.subplots(4)
nfreqs = 2
dictionary = {}
def argmax_n(nr_of_values, absolute_values):
    freqs = []
    for i in range(nr_of_values):
        current_max_index = np.argmax(absolute_values)
        value = absolute_values[current_max_index]
        freqs.append((current_max_index, value))
        absolute_values[np.argmax(absolute_values)] = 0
    return freqs

for i, row in enumerate(fourier_transformed_matrix):
    ax[i].plot(xf,row)
    dictionary[i] = argmax_n(nfreqs, fourier_transformed_matrix[i,:])
plt.show()

