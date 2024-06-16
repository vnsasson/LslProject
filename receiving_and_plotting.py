import time
import numpy as np
import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_stream

# Resolve the EEG stream and create an inlet
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])

# Initialize plot
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
x = np.arange(0, 35)  # x-axis for plotting
line, = ax.plot(x, np.zeros_like(x))  # Initial plot, y values are zeros

ax.set_title('Simulated EEG Data')
ax.set_xlabel('Channel')
ax.set_ylabel('EEG Value')
ax.set_ylim(-20e-05, 20e-5)  # Adjust ylim based on your simulated data range

# Start receiving and plotting
print("Now receiving and plotting data... Press Ctrl+C to stop.")
try:
    while True:
        # Receive EEG data from the inlet
        sample, timestamp = inlet.pull_sample()
        print("sample", sample)
        print("timestamp", timestamp)
        # Update plot with new data
        line.set_ydata(sample)
        fig.canvas.draw()
        fig.canvas.flush_events()

except KeyboardInterrupt:
    print("\nPlotting stopped.")
