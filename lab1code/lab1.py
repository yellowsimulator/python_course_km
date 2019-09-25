import matplotlib.pyplot as plt
import pandas as pd


def plot_spectrum(path):
    """
    This function plots a frequency
    spectrum.
    """
    data = pd.read_csv(path)
    frequency = data["frequency"].values
    amplitude = data["amplitude"].values
    #plotting starts
    plt.plot(frequency, amplitude)
    plt.xlabel("Frequency in Hz")
    plt.ylabel("Amplitude in G")
    plt.title("A frequency spectrum with BPFO and harmonics")
    plt.show()




if __name__ == '__main__':
    path = "data.csv"
    plot_spectrum(path)
