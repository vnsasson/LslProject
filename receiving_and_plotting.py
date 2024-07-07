import time
import numpy as np
import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_stream

# Resolve the EEG stream and create an inlet
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

# Get stream information
info = inlet.info()
sfreq = info.nominal_srate()
buffer_length = int(sfreq * 0.5)  # 1 second buffer

# Initialize plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
x = np.arange(buffer_length)  # x-axis for plotting (1 second worth of data)
y_data = np.zeros((buffer_length, info.channel_count()))  # Initial y data

lines = []
for ch in range(info.channel_count()):
    line, = ax.plot(x, y_data[:, ch])
    lines.append(line)

ax.set_title('Simulated EEG Data')
ax.set_xlabel('Time (s)')
ax.set_ylabel('EEG Value')
ax.set_xlim(0, buffer_length)
ax.set_ylim(-2e-05, 2e-05)  # Adjust ylim based on your simulated data range

# Start receiving and plotting
print("Now receiving and plotting data... Press Ctrl+C to stop.")
refresh_interval = 0.01  # Plot refresh interval in seconds
last_update_time = time.time()

try:
    while True:
        # Receive EEG data from the inlet
        sample, timestamp = inlet.pull_sample()
        y_data = np.roll(y_data, -1, axis=0)  # Shift data left
        y_data[-1, :] = sample  # Insert new sample at the end

        # Update plot with new data if the refresh interval has passed
        current_time = time.time()
        if current_time - last_update_time >= refresh_interval:
            for ch in range(info.channel_count()):
                lines[ch].set_ydata(y_data[:, ch])
            ax.set_ylim(y_data.min() * 1.1, y_data.max() * 1.1)  # Dynamic y-limits
            fig.canvas.draw()
            fig.canvas.flush_events()
            last_update_time = current_time

except KeyboardInterrupt:
    print("\nPlotting stopped.")
except Exception as e:
    print(f"\nAn error occurred: {e}")

print("Plotting finished.")
