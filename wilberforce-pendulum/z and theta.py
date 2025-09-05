import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load data from CSV (Replace with your file path)
data = pd.read_csv('/Users/andrewwu/Downloads/wilberforce pendulum - trial.csv')
data.fillna(value = 0, inplace = True)
    # Extract time, angular displacement (theta), and vertical displacement (z)
time = data['time'].values  # Time in seconds
theta = data['rdisp'].values  # Angular displacement (theta)
z = data['vdisp'].values  # Vertical displacement

# Remove DC offset
theta -= np.mean(theta)
z -= np.mean(z)

# Compute Fourier Transforms
theta_fft = np.fft.fft(theta)
z_fft = np.fft.fft(z)

# Compute frequency spectrum
n = len(time)
dt = np.mean(np.diff(time))  # Time step
frequencies = np.fft.fftfreq(n, d=dt)
angular_frequencies = 2 * np.pi * frequencies  # Convert to rad/s

# Find the two dominant frequencies (normal modes)
def find_two_largest_peaks(freqs, fft_values):
    magnitude_spectrum = np.abs(fft_values)
    peak_indices = np.argsort(magnitude_spectrum)[-2:]  # Find two highest peaks
    omega_1, omega_2 = np.sort(freqs[peak_indices])
    return omega_1, omega_2, peak_indices

omega_1, omega_2, peak_indices = find_two_largest_peaks(angular_frequencies[:n//2], theta_fft[:n//2])

# Create Bandpass Filters for Normal Modes
def bandpass_filter(fft_values, freqs, target_freq, bandwidth=0.5):
    """Keeps only frequencies within ±bandwidth of target_freq."""
    filtered_fft = np.zeros_like(fft_values, dtype=complex)
    mask = (np.abs(freqs - target_freq) < bandwidth)
    filtered_fft[mask] = fft_values[mask]
    return filtered_fft

# Filter FFT for both normal modes
theta_fft_mode1 = bandpass_filter(theta_fft, angular_frequencies, omega_1)
theta_fft_mode2 = bandpass_filter(theta_fft, angular_frequencies, omega_2)
z_fft_mode1 = bandpass_filter(z_fft, angular_frequencies, omega_1)
z_fft_mode2 = bandpass_filter(z_fft, angular_frequencies, omega_2)

# Compute inverse FFT to reconstruct normal mode motion
theta_mode1 = np.fft.ifft(theta_fft_mode1).real
theta_mode2 = np.fft.ifft(theta_fft_mode2).real
z_mode1 = np.fft.ifft(z_fft_mode1).real
z_mode2 = np.fft.ifft(z_fft_mode2).real

# Plot Normal Modes in z-θ Space
plt.figure(figsize=(8, 6))
plt.plot(z_mode1, theta_mode1, label=f"Mode 1 ({omega_1:.3f} rad/s)", color='blue')
plt.plot(z_mode2, theta_mode2, label=f"Mode 2 ({omega_2:.3f} rad/s)", color='red')

plt.xlabel('Vertical Displacement z (m)')
plt.ylabel('Angular Displacement θ (radians)')
plt.title('Wilberforce Pendulum: Normal Modes in z-θ Space')
plt.grid()
plt.legend()
plt.show()
