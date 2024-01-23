import SignalForger
import matplotlib.pyplot as plt
import numpy as np

import SignalTransmitter as signalTransmitter

NUM_SAMPLES = 1e6


def run():
    samples = np.fromfile("../Samples/gniazdko3.iq", np.complex64)

    print(samples)
    signal_forger = SignalForger.SignalForger(samples, int(8e6), int(1e6))

    plt.figure(0)
    plt.plot(signal_forger.samples_absolute[20000:30000])

    plt.figure(1)
    plt.plot(signal_forger.samples_filtered[20000:30000])

    # signal_binary = signal_forger.binary_signal()
    plt.figure(2)
    plt.plot(signal_forger.samples_binary[20000:30000])

    plt.figure(3)
    plt.plot(signal_forger.forged_signal[20000:30000])

    plt.show()

    transmitter = signalTransmitter.SignalTransmitter("ip:192.168.2.1",
                                                      NUM_SAMPLES,
                                                      4349e5,
                                                      0)

    transmitter.transmit_samples(signal_forger.forged_signal)