import time
import numpy as np
from pylsl import StreamInfo, StreamOutlet
import mne

file_path = r"C:\Users\SassonVaknin\Documents\PycharnProjects\data\ZE-030-021-530-EC.edf"
raw = mne.io.read_raw_edf(file_path, preload=True)

# Get data info
ch_names = raw.info['ch_names']
sfreq = int(raw.info['sfreq'])

# Define stream parameters
info = StreamInfo('EDFStream', 'EEG', channel_count=len(ch_names), nominal_srate=sfreq,
                  channel_format='float32', source_id='myuid34234')
# info = StreamInfo('SimulatedEEG', 'EEG', 8, 100, 'float32', 'myuid34234')


# Adjust the channel count to match the LSL stream's expected number of channels
# info.channel_count = 35  # Update this number according to your LSL stream's configuration

# Create an outlet to stream data
outlet = StreamOutlet(info)

print(f"Now streaming {file_path}...")

# Stream data in chunks
chunk_size = 10  # Number of seconds per chunk
total_samples = raw.n_times
start_idx = 0

try:
    while start_idx < total_samples:
        end_idx = start_idx + chunk_size * sfreq
        if end_idx > total_samples:
            end_idx = total_samples

        # Read chunk of data
        data_chunk, times_chunk = raw[:, start_idx:end_idx]

        # Stream the chunk
        for sample in data_chunk.T:
            outlet.push_sample(sample)

        start_idx = end_idx
        time.sleep(chunk_size)  # Wait for next chunk

except KeyboardInterrupt:
    print("\nStreaming stopped.")
