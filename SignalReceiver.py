import adi


class SignalReceiver:
    def __init__(
            self,
            ip_address,
            sample_rate,
            center_freq,
            hardware_gain,
            samples_count):
        self.sdr = adi.Pluto(ip_address)
        self.sdr.gain_control_mode_chan0 = 'manual'
        self.sdr.rx_hardwaregain_chan0 = hardware_gain  # dB
        self.sdr.rx_lo = int(center_freq)
        self.sdr.sample_rate = int(sample_rate)
        self.sdr.rx_rf_bandwidth = int(sample_rate)
        self.sdr.rx_buffer_size = samples_count

    def record_samples(self):
        return self.sdr.rx()



