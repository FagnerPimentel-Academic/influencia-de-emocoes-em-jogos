from bids import BIDSLayout
import mne
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

bids_dir = r'C:\Users\Vinicius\Documents\TCC\EEG'

layout = BIDSLayout(bids_dir, validate=False)

eeg_files = layout.get(suffix='eeg', extension='set')
if not eeg_files:
    raise FileNotFoundError("Nenhum arquivo EEG encontrado no diretório BIDS especificado.")

raw = mne.io.read_raw_eeglab(eeg_files[0].path, preload=True)

events, event_ids = mne.events_from_annotations(raw)

tmin, tmax = -0.2, 0.5 

epochs = mne.Epochs(raw, events, event_id=event_ids, tmin=tmin, tmax=tmax, baseline=(None, 0), preload=True)

def band_power(epochs, band):
    data = epochs.get_data() 
    sfreq = epochs.info['sfreq']
    psd, freqs = mne.time_frequency.psd_array_welch(data, sfreq=sfreq, fmin=band[0], fmax=band[1], n_fft=data.shape[2])
    return psd

bands = {
    "Delta": (0.5, 4),
    "Theta": (4, 8),
    "Alpha": (8, 12),
    "Beta": (12, 30),
    "Gamma": (30, 100)
}

all_band_powers = pd.DataFrame()

for band_name, band_range in bands.items():
    power = band_power(epochs, band_range) 
    
    n_epochs, n_channels, n_times = power.shape
    reshaped_power = power.reshape(n_epochs * n_times, n_channels)
    
    power_df = pd.DataFrame(reshaped_power, columns=[f"{band_name}_{ch}" for ch in epochs.ch_names])
    
    power_df['epoch'] = np.repeat(np.arange(n_epochs), n_times)
    
    all_band_powers = pd.concat([all_band_powers, power_df], axis=1)


inverted_event_ids = {v: k for k, v in event_ids.items()}

event_series = np.repeat([inverted_event_ids.get(event_id, 'Evento desconhecido') for event_id in epochs.events[:, 2]], n_times)

all_band_powers['event'] = event_series

all_band_powers.to_excel('band_powers1.xlsx', index=False)

print(all_band_powers.head())
