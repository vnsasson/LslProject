import time
import numpy as np
from pylsl import StreamInfo, StreamOutlet

# Define stream parameters
info = StreamInfo('SimulatedEEG', 'EEG', 8, 100, 'float32', 'myuid34234')

# Create an outlet to stream data
outlet = StreamOutlet(info)

print("Now sending data...")

try:
    while True:
        # Generate random EEG data
        sample = np.random.rand(8) * 100  # Example: random numbers scaled for EEG-like values

        # Stream the data
        outlet.push_sample(sample)

        # Wait a bit before sending the next sample (adjust as needed)
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nData simulation stopped.")
