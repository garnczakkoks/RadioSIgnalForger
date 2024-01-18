import numpy as np
import scipy.signal as sig


class SignalForger:
    HISTOGRAM_BINS_NUMBER = 200

    def __init__(
            self,
            samples: np.ndarray,
            samples_bandwidth: int,
            sample_rate: int):
        self.samples = samples
        self.samples_bandwidth = samples_bandwidth
        self.sample_rate = sample_rate
        self.frequency_shift = self.__calculate_frequency_shift(samples, samples_bandwidth)
        self.samples_absolute = self.__signal_absolute(self.samples)
        self.samples_filtered = self.__signal_filter(self.samples_absolute)
        self.most_occurring_max_amplitude = self.__calculate_most_occurring_max_amplitude(self.samples_filtered)
        self.samples_binary = self.__binary_signal(self.samples_filtered, self.most_occurring_max_amplitude / 2)
        self.forged_signal = self.__construct_sin_signal(self.samples_binary, len(self.samples), self.sample_rate,
                                                         self.most_occurring_max_amplitude, self.frequency_shift)

    @staticmethod
    def __signal_absolute(samples: np.ndarray) -> np.ndarray:
        return np.abs(samples)

    @staticmethod
    def __signal_filter(samples: np.ndarray) -> np.ndarray:
        a = 5
        b = np.ones(a) / a
        return sig.filtfilt(b, 1, samples)

    @staticmethod
    def __binary_signal(samples: np.ndarray, detector_value: float) -> np.ndarray:
        return (samples > detector_value).astype(int)

    @staticmethod
    def __calculate_most_occurring_max_amplitude(samples: np.ndarray) -> float:
        min_amplitude = np.min(samples)
        max_amplitude = np.max(samples)

        threshold = (max_amplitude - min_amplitude) / 2

        hist, bins = np.histogram(samples, bins=SignalForger.HISTOGRAM_BINS_NUMBER)
        middle_bin = int((threshold / max_amplitude) * SignalForger.HISTOGRAM_BINS_NUMBER)

        index_of_max_amplitude_right = np.argmax(hist[middle_bin:]) + middle_bin
        most_occurring_max_amplitude = index_of_max_amplitude_right / SignalForger.HISTOGRAM_BINS_NUMBER \
                                       * (max_amplitude - min_amplitude)

        return most_occurring_max_amplitude

    @staticmethod
    def __calculate_frequency_shift(samples: np.ndarray, samples_bandwidth: int) -> float:
        psd = np.abs(np.fft.fftshift(np.fft.fft(samples))) ** 2
        max_psd = np.argmax(psd)
        return -samples_bandwidth / 2 + (max_psd / len(samples)) * samples_bandwidth

    @staticmethod
    def __construct_sin_signal(binary_vector, number_of_samples, sample_rate, average_max_amplitude, frequency) \
            -> np.ndarray:
        t = np.arange(number_of_samples) / sample_rate
        samples_sin = average_max_amplitude * np.exp(2.0j * np.pi * frequency * t)

        return binary_vector * samples_sin
