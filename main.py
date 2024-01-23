import time
import numpy as np
import SignalReceiver
import SignalForger
import matplotlib.pyplot as plt
import SignalTransmitter
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    running = 1

    while running:
        try:
            print("\nWac ju wana du:\n1. Pobrac sygnal i zapisac do pliku.\n2. Wczytac z pliku i nadac.\n3. Pobrac i nadac.\n4. Wyjsc z programu.\n")
            input1 = int(input("Wybierz opcje: "))

            if input1 == 1:
                print("Pobieranie danych za")
                time.sleep(1)
                print("3")
                time.sleep(1)
                print("2")
                time.sleep(1)
                print("1")
                time.sleep(1)
                print("pobieram...")

                receiver = SignalReceiver.SignalReceiver(
                    "ip:192.168.2.1",
                    8e6,
                    4349e5,
                    40.0,
                    1000000
                )
                samples = receiver.record_samples()

                signal_forger = SignalForger.SignalForger(samples, int(8e6), int(8e6))

                plt.figure(0)

                bins_number = 200  # na ile ma być podzielony histogram
                histo, bins, _ = plt.hist(signal_forger.samples_filtered, bins=bins_number, color='blue', alpha=0.7)
                plt.title('Histogram Rozkładu Amplitud')
                plt.xlabel('Wartości Amplitudy')

                min_amplitude = np.min(signal_forger.samples_filtered)
                max_amplitude = np.max(signal_forger.samples_filtered)
                threshold = (max_amplitude - min_amplitude) / 2
                plt.axvline(threshold, color='red', linestyle='dashed', linewidth=2)

                plt.figure(1)
                plt.plot(signal_forger.samples_absolute, c='#404040')
                plt.plot(signal_forger.samples_filtered)
                plt.xlabel("Time")
                plt.title("Moduł sygnału wraz z filtracją")

                plt.figure(2)
                plt.plot(signal_forger.samples_binary)
                plt.xlabel("Time")
                plt.title("Sygnał binarny")

                psd = np.fft.fft(signal_forger.samples)
                psd_dB = 10 * np.log10(psd)
                max_psd = np.argmax(psd)
                freq_shift = -signal_forger.samples_bandwidth / 2 + (max_psd / len(signal_forger.samples)) * signal_forger.samples_bandwidth

                f = np.linspace(signal_forger.samples_bandwidth / -2, signal_forger.samples_bandwidth / 2, len(psd))
                plt.figure(3)
#                                                                                                                                                                                                                       print("Chujek")

                plt.plot(f / 1e6, psd_dB)
                plt.xlabel("Frequency [MHz]")
                plt.ylabel("PSD")
                plt.title("Sygnał w dziedzinie częstotliwości")


                plt.figure(4)
                plt.plot(signal_forger.samples)
                plt.plot(signal_forger.forged_signal)
                plt.title("Sygnał pierwotny oraz sygnał przeprocesowany")
                plt.xlabel('Czas')
                plt.ylabel('Amplituda')
                plt.grid(True)

                plt.show()

                samples_forged = signal_forger.forged_signal.astype(np.complex64)  # Convert to 64
                file_name = str(input("Podaj nazwe pliku:"))
                file_name = file_name + ".iq"
                samples_forged.tofile(file_name)
                print(f"Zapisano do pliku {file_name}")

            elif input1 == 2:
                file_name = str(input("Podaj nazwe pliku:"))
                file_name = file_name + ".iq"
                samples_forged = np.fromfile(file_name, np.complex64)

                print("Sygnal pobrany. Wcisnij 1 aby nadac.\n")
                input3 = int(input("Wybierz opcje: "))
                if input3 == 1:
                    transmitter = SignalTransmitter.SignalTransmitter("ip:192.168.2.1",
                                                                      8e6,
                                                                      4349e5,
                                                                      0)
                    print("Nadawanie.")
                    transmitter.transmit_samples(samples_forged * 2 ** 14)

                    print("Sygnal zostal nadany.")



            elif input1 == 3:
                print("Czy chcesz wyswietlic wykresy? 1. tak, 2. nie\n")
                input2 = int(input("Wybierz opcje: "))

                if input2 == 1:
                    print("Pobieranie danych za")
                    time.sleep(1)
                    print("3")
                    time.sleep(1)
                    print("2")
                    time.sleep(1)
                    print("1")
                    time.sleep(1)
                    print("pobieram...")

                    receiver = SignalReceiver.SignalReceiver(
                        "ip:192.168.2.1",
                        8e6,
                        4349e5,
                        40.0,
                        1000000
                    )
                    samples = receiver.record_samples()

                    signal_forger = SignalForger.SignalForger(samples, int(8e6), int(8e6))

                    plt.figure(0)

                    bins_number = 200  # na ile ma być podzielony histogram
                    histo, bins, _ = plt.hist(signal_forger.samples_filtered, bins=bins_number, color='blue', alpha=0.7)
                    plt.title('Histogram Rozkładu Amplitud')
                    plt.xlabel('Wartości Amplitudy')

                    min_amplitude = np.min(signal_forger.samples_filtered)
                    max_amplitude = np.max(signal_forger.samples_filtered)
                    threshold = (max_amplitude - min_amplitude) / 2
                    plt.axvline(threshold, color='red', linestyle='dashed', linewidth=2)

                    plt.figure(1)
                    plt.plot(signal_forger.samples_absolute, c='#404040')
                    plt.plot(signal_forger.samples_filtered)
                    plt.xlabel("Time")
                    plt.title("Moduł sygnału wraz z filtracją")

                    plt.figure(2)
                    plt.plot(signal_forger.samples_binary)
                    plt.xlabel("Time")
                    plt.title("Sygnał binarny")

                    psd = np.fft.fft(signal_forger.samples)
                    psd_dB = 10 * np.log10(psd)
                    max_psd = np.argmax(psd)
                    freq_shift = -signal_forger.samples_bandwidth / 2 + (
                                max_psd / len(signal_forger.samples)) * signal_forger.samples_bandwidth

                    f = np.linspace(signal_forger.samples_bandwidth / -2, signal_forger.samples_bandwidth / 2, len(psd))
                    plt.figure(3)
                    #                                                                                                                                                                                                                       print("Chujek")

                    plt.plot(f / 1e6, psd_dB)
                    plt.xlabel("Frequency [MHz]")
                    plt.ylabel("PSD")
                    plt.title("Sygnał w dziedzinie częstotliwości")

                    plt.figure(4)
                    plt.plot(signal_forger.samples)
                    plt.plot(signal_forger.forged_signal)
                    plt.title("Sygnał pierwotny oraz sygnał przeprocesowany")
                    plt.xlabel('Czas')
                    plt.ylabel('Amplituda')
                    plt.grid(True)

                    plt.show()
                    print("Sygnal pobrany. Wcisnij 1 aby nadac.\n")
                    input3 = int(input("Wybierz opcje: "))
                    if input3 == 1:
                        transmitter = SignalTransmitter.SignalTransmitter("ip:192.168.2.1",
                                                                          8e6,
                                                                          4349e5,
                                                                          0)
                        print("Nadawanie.")
                        transmitter.transmit_samples(signal_forger.forged_signal * 2 ** 14)


                        print("Sygnal zostal nadany.")



                else:
                    print("Pobieranie danych za")
                    time.sleep(1)
                    print("3")
                    time.sleep(1)
                    print("2")
                    time.sleep(1)
                    print("1")
                    time.sleep(1)
                    print("pobieram...")

                    receiver = SignalReceiver.SignalReceiver(
                        "ip:192.168.2.1",
                        8e6,
                        4349e5,
                        40.0,
                        1000000
                    )
                    samples = receiver.record_samples()

                    signal_forger = SignalForger.SignalForger(samples, int(8e6), int(8e6))

                    print("Sygnal pobrany. Wcisnij 1 aby nadac.\n")
                    input3 = int(input("Wybierz opcje: "))
                    if input3 == 1:
                        transmitter = SignalTransmitter.SignalTransmitter("ip:192.168.2.1",
                                                                          8e6,
                                                                          4349e5,
                                                                          0)
                        print("Nadawanie.")
                        transmitter.transmit_samples(signal_forger.forged_signal * 2 ** 14)

                        print("Sygnal zostal nadany.")
            elif input1 == 4:
                running = 0
            else:
                print("Niepoprawny wybor.")
        except ValueError:
            print("problem")


