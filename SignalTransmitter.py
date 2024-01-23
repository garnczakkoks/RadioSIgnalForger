import adi


class SignalTransmitter:
    def __init__(
            self,
            ip_address,
            sample_rate,
            center_freq,
            hardware_gain):
        self.sdr = adi.Pluto(ip_address)
        self.sdr.gain_control_mode_chan0 = 'manual'
        self.sdr.tx_hardwaregain_chan0 = hardware_gain  # dB
        self.sdr.tx_lo = int(center_freq)
        self.sdr.sample_rate = int(sample_rate)
        self.sdr.tx_rf_bandwidth = int(sample_rate)

    def transmit_samples(self, samples):
        for i in range(3):
            self.sdr.tx(samples)

