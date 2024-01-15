import numpy as np
import SignalUtils as signalUtils
import matplotlib.pyplot as plt



if __name__ == '__main__':
    samples = np.fromfile('Samples/gniazdko4.iq', np.complex64)
    absolute_samples = signalUtils.signal_absolute(samples)
    plt.figure()
    plt.plot(absolute_samples[20000:30000])
    plt.xlabel("Time")

    filtered_samples = signalUtils.signal_filter(absolute_samples)

    #shift =

    plt.show()
