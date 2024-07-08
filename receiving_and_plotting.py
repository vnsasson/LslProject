import time
import numpy as np
import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_stream
from scipy.fft import fft

# Predefined list of channel names for the streamed data
default_channel_names = [
    'Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2',
    'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'Fz', 'Cz', 'Pz'
]

# Resolve the EEG stream and create an inlet
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

# Get stream information
info = inlet.info()
sfreq = info.nominal_srate()
channel_count = min(info.channel_count(), 19)  # Limit to first 19 channels

# Use predefined channel names since the LSL stream names are empty
channel_names = default_channel_names[:channel_count]

# Define buffer lengths
buffer_length = int(sfreq)  # 1 second of data for time domain plotting
analysis_buffer_length = int(sfreq * 120)  # 2 minutes of data for FFT analysis

# Initialize buffers
time_buffer = np.zeros((buffer_length, channel_count))
analysis_buffer = np.zeros((analysis_buffer_length, channel_count))

# Initialize time domain plot
plt.ion()  # Turn on interactive mode
fig_time, axs_time = plt.subplots(channel_count, 1, figsize=(10, 2 * channel_count), sharex=True)
x_time = np.arange(buffer_length) / sfreq  # Time axis for plotting (1 second worth of data)
time_lines = []
for ch in range(channel_count):
    line_time, = axs_time[ch].plot(x_time, time_buffer[:, ch])
    time_lines.append(line_time)
    axs_time[ch].set_ylabel(channel_names[ch], rotation=0, labelpad=50, fontsize=10, va='center')
    axs_time[ch].yaxis.set_label_position("left")  # Position labels on the right side
    axs_time[ch].set_yticks([])  # Remove y-ticks as we only need the labels
axs_time[-1].set_xlabel('Time (s)')
plt.suptitle('EEG Time Domain')
plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05)

# Initialize frequency domain plot
fig_fft, axs_fft = plt.subplots(channel_count, 1, figsize=(10, 2 * channel_count), sharex=True)
x_fft = np.linspace(0, sfreq / 2, analysis_buffer_length // 2)  # Frequency axis for plotting
fft_lines = []
for ch in range(channel_count):
    line_fft, = axs_fft[ch].plot(x_fft, np.zeros(analysis_buffer_length // 2))
    fft_lines.append(line_fft)
    axs_fft[ch].set_ylabel(channel_names[ch], rotation=0, labelpad=50, fontsize=10, va='center')
    axs_fft[ch].yaxis.set_label_position("left")  # Position labels on the right side
    axs_fft[ch].set_yticks([])  # Remove y-ticks as we only need the labels
axs_fft[-1].set_xlabel('Frequency (Hz)')
plt.suptitle('EEG Frequency Domain (Magnitude)')
plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.05)

# Start receiving and plotting data
print("Now receiving and plotting data... Press Ctrl+C to stop.")
refresh_interval = 10  # Plot refresh interval in seconds
last_update_time = time.time()
samples_collected = 0

try:
    while True:
        # Receive EEG data from the inlet
        sample, timestamp = inlet.pull_sample()
        time_buffer = np.roll(time_buffer, -1, axis=0)  # Shift data left in time buffer
        time_buffer[-1, :] = sample[:channel_count]  # Insert new sample at the end of time buffer
        analysis_buffer = np.roll(analysis_buffer, -1, axis=0)  # Shift data left in analysis buffer
        analysis_buffer[-1, :] = sample[:channel_count]  # Insert new sample at the end of analysis buffer
        samples_collected += 1

        # Update time domain plot with new data if the refresh interval has passed
        current_time = time.time()
        if current_time - last_update_time >= refresh_interval:
            for ch in range(channel_count):
                time_lines[ch].set_ydata(time_buffer[:, ch])
                axs_time[ch].set_ylim(time_buffer[:, ch].min() * 1.1,
                                      time_buffer[:, ch].max() * 1.1)  # Dynamic y-limits

            fig_time.canvas.draw()
            fig_time.canvas.flush_events()
            last_update_time = current_time

        # Perform FFT analysis after 2 minutes (120 seconds) of data
        if samples_collected >= analysis_buffer_length:
            samples_collected = 0  # Reset sample counter

            # Calculate FFT and magnitude for each channel
            for ch in range(channel_count):
                yf = fft(analysis_buffer[:, ch])
                magnitude = np.abs(yf[:analysis_buffer.shape[0] // 2]) ** 2  # Magnitude of FFT
                fft_lines[ch].set_ydata(magnitude)

            fig_fft.canvas.draw()
            fig_fft.canvas.flush_events()

            # Freeze the frequency domain plot after plotting once
            plt.ioff()

except KeyboardInterrupt:
    print("\nPlotting stopped.")
except Exception as e:
    print(f"\nAn error occurred: {e}")

print("Plotting finished.")

