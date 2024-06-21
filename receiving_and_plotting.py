# import time
# import numpy as np
# import matplotlib.pyplot as plt
# from pylsl import StreamInlet, resolve_stream
#
# # Resolve the EEG stream and create an inlet
# streams = resolve_stream('type', 'EEG')
# inlet = StreamInlet(streams[0])
#
# # Get stream information
# info = inlet.info()
# sfreq = info.nominal_srate()
# buffer_length = int(sfreq * 0.5)  # 1 second buffer
#
# # Initialize plot
# plt.ion()  # Turn on interactive mode
# fig, ax = plt.subplots()
# x = np.arange(buffer_length)  # x-axis for plotting (1 second worth of data)
# y_data = np.zeros((buffer_length, info.channel_count()))  # Initial y data
#
# lines = []
# for ch in range(info.channel_count()):
#     line, = ax.plot(x, y_data[:, ch])
#     lines.append(line)
#
# ax.set_title('Simulated EEG Data')
# ax.set_xlabel('Time (s)')
# ax.set_ylabel('EEG Value')
# ax.set_xlim(0, buffer_length)
# ax.set_ylim(-2e-05, 2e-05)  # Adjust ylim based on your simulated data range
#
# # Start receiving and plotting
# print("Now receiving and plotting data... Press Ctrl+C to stop.")
# refresh_interval = 0.01  # Plot refresh interval in seconds
# last_update_time = time.time()
#
# try:
#     while True:
#         # Receive EEG data from the inlet
#         sample, timestamp = inlet.pull_sample()
#         y_data = np.roll(y_data, -1, axis=0)  # Shift data left
#         y_data[-1, :] = sample  # Insert new sample at the end
#
#         # Update plot with new data if the refresh interval has passed
#         current_time = time.time()
#         if current_time - last_update_time >= refresh_interval:
#             for ch in range(info.channel_count()):
#                 lines[ch].set_ydata(y_data[:, ch])
#             ax.set_ylim(y_data.min() * 1.1, y_data.max() * 1.1)  # Dynamic y-limits
#             fig.canvas.draw()
#             fig.canvas.flush_events()
#             last_update_time = current_time
#
# except KeyboardInterrupt:
#     print("\nPlotting stopped.")
# except Exception as e:
#     print(f"\nAn error occurred: {e}")
#
# print("Plotting finished.")

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
buffer_length = int(sfreq * 0.5)  # 0.5 second buffer
total_channels = min(info.channel_count(), 19)  # Use only the first 19 channels

# Retrieve channel names
ch = info.desc().child("channels").child("channel")
ch_names = [ch.child_value("label")]
for _ in range(1, total_channels):
    ch = ch.next_sibling()
    ch_names.append(ch.child_value("label"))

# Initialize plot
plt.ion()  # Turn on interactive mode
fig, axes = plt.subplots(total_channels, 1, sharex=True, figsize=(10, 10))
x = np.arange(buffer_length)  # x-axis for plotting (0.5 seconds worth of data)
y_data = np.zeros((buffer_length, total_channels))  # Initial y data

lines = []
for i, ax in enumerate(axes):
    line, = ax.plot(x, y_data[:, i])
    lines.append(line)
    ax.set_ylabel(ch_names[i], rotation=0, labelpad=40, ha='right', va='center')
    ax.set_ylim(-2e-05, 2e-05)  # Adjust ylim based on your simulated data range
    ax.yaxis.set_ticklabels([])  # Hide y-axis tick labels

axes[-1].set_xlabel('Time (s)')  # Set x-axis label only for the bottom plot
fig.suptitle('Simulated EEG Data')

# Start receiving and plotting
print("Now receiving and plotting data... Press Ctrl+C to stop.")
refresh_interval = 0.01  # Plot refresh interval in seconds
last_update_time = time.time()

try:
    while True:
        # Receive EEG data from the inlet
        sample, timestamp = inlet.pull_sample()
        y_data = np.roll(y_data, -1, axis=0)  # Shift data left
        y_data[-1, :] = sample[:total_channels]  # Insert new sample at the end, only for first 19 channels

        # Update plot with new data if the refresh interval has passed
        current_time = time.time()
        if current_time - last_update_time >= refresh_interval:
            for i, line in enumerate(lines):
                line.set_ydata(y_data[:, i])
                axes[i].set_ylim(y_data[:, i].min() * 1.1, y_data[:, i].max() * 1.1)  # Dynamic y-limits
            fig.canvas.draw()
            fig.canvas.flush_events()
            last_update_time = current_time

except KeyboardInterrupt:
    print("\nPlotting stopped.")
except Exception as e:
    print(f"\nAn error occurred: {e}")

print("Plotting finished.")
