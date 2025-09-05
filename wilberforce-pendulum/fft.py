import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def find_two_largest_peaks(freqs, amplitudes):
    """
    Finds the two largest local maxima in the amplitude spectrum.

    Parameters:
        freqs (numpy array): Array of angular frequencies.
        amplitudes (numpy array): Array of corresponding amplitude values.

    Returns:
        tuple: (omega_1, omega_2) the two dominant angular frequencies.
    """
    from scipy.signal import find_peaks

    peaks, _ = find_peaks(amplitudes)  # Find all local maxima
    peak_frequencies = freqs[peaks]  # Get corresponding frequencies
    peak_amplitudes = amplitudes[peaks]  # Get their amplitudes

    # Sort peaks by amplitude (descending order) and take the top two
    sorted_indices = np.argsort(peak_amplitudes)[-2:]  # Get indices of two largest peaks
    sorted_indices = sorted_indices[::-1]  # Sort from highest to lowest

    return peak_frequencies[sorted_indices[0]], peak_frequencies[sorted_indices[1]]

# Define file paths for each initial spring length (replace with actual file names)
file_paths = {
    "35 cm": "/Users/andrewwu/Downloads/wilberforce pendulum - 35 trial.csv",
    "30 cm": "/Users/andrewwu/Downloads/wilberforce pendulum - 30 trial.csv",
    "25 cm": "/Users/andrewwu/Downloads/wilberforce pendulum - 25 trial.csv",
    "20 cm": "/Users/andrewwu/Downloads/wilberforce pendulum - 20 trial.csv",
    "15 cm": "/Users/andrewwu/Downloads/wilberforce pendulum - 15 trial.csv"
}

plt.figure(figsize=(10, 6))  # Set figure size

# Loop through each dataset and compute FFT
for label, file in file_paths.items():
    # Load experimental data
    data = pd.read_csv(file)
    time = data['t'].values
    displacement = data['radians'].values

    # Remove DC offset
    displacement = displacement - np.mean(displacement)

    # Compute Fourier Transform
    n = len(time)
    dt = np.mean(np.diff(time))  # Compute time step
    fft_values = np.fft.fft(displacement)

    # Compute the magnitude spectrum and normalize
    magnitude_spectrum = (2 / n) * np.abs(fft_values[:n // 2])

    # Compute corresponding angular frequencies
    frequencies = np.fft.fftfreq(n, d=dt)
    angular_frequencies = 2 * np.pi * frequencies[:n // 2]  # Convert to rad/s

    # Find the two largest peaks (normal modes)
    omega_1, omega_2 = find_two_largest_peaks(angular_frequencies, magnitude_spectrum)
    print(f"Trial {label}: \\omega_1 = {omega_1:.3f}, \\omega_2 = {omega_2:.3f}")
    # Plot each dataset on the same graph
    plt.plot(angular_frequencies, magnitude_spectrum, label=f"{label}")

# Formatting the plot
plt.xlabel('Angular Frequency (rad/s)')
plt.ylabel('Amplitude (m)')
plt.title('FFT Analysis of Wilberforce Pendulum ')
plt.xlim(0, 6)
plt.grid()
plt.legend(title="Initial Height")
plt.show()
