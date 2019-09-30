import pandas as pd
import matplotlib.pyplot as plt

def print_message():
    """
    baøala
    """
    print("Iam awesome")

def print_message2():
    """
    function with a varible
    """
    message = "I am awesome and cool"
    print(message)

def function_with_argument(message):
    """
    A function with one argument
    """
    print(message)

def plot_spectrum(file_name):
    """
    This function plots
    a frequency spectrum
    """
    table = pd.read_csv(file_name)
    #print(table)
    frequency = table["frequency"].values
    amplitude = table["amplitude"].values
    plt.plot(frequency, amplitude,color="red")
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.title("A frequency spectrum")
    plt.show()

def new_frequency_spectrum(file_name,xlabel):
    """
    frequency spectrum with three
    arguments
    """
    table = pd.read_csv(file_name,x_label)
    #print(table)
    frequency = table["frequency"].values
    amplitude = table["amplitude"].values
    plt.plot(frequency, amplitude,color="red")
    plt.xlabel(x_label)
    plt.ylabel()
    plt.title()
    plt.show()


if __name__ == '__main__':
    file_name = "frequency_spectrum.csv"
    plot_spectrum(file_name)
