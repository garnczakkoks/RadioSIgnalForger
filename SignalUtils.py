import numpy as np
import scipy.signal as sig


def signal_absolute(samples):
    return np.abs(samples)


def signal_filter(samples):
    a = 5
    b = np.ones(a) / a
    return sig.filtfilt(b, 1, samples)


def transform_signal_to_binary(samples):
    detector_value = calculate_detector_value(samples)
    return (samples > detector_value).astype(int)


def calculate_detector_value(samples):
    bins_number = 200

    min_amplitude = np.min(samples)
    max_amplitude = np.max(samples)

    threshold = (max_amplitude - min_amplitude) / 2

    hist, bins = np.histogram(samples, bins=bins_number)
    middle_bin = int((threshold/max_amplitude) * bins_number)

    index_of_max_amplitude_right = np.argmax(hist[middle_bin:]) + middle_bin
    most_occurring_max_amplitude = index_of_max_amplitude_right / bins_number * (max_amplitude - min_amplitude)

    return most_occurring_max_amplitude/2


def calculate_frequency_shift(samples, samples_bandwidth):
    psd = np.abs(np.fft.fftshift(np.fft.fft(samples))) ** 2
    psd_db = 10 * np.log10(psd)
    max_psd = np.argmax(psd)
    return max_psd - samples_bandwidth / 2
