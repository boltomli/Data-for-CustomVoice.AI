import argparse

import numpy as np
import soundfile as sf
from nara_wpe.utils import istft, stft
from nara_wpe.wpe import wpe

parser = argparse.ArgumentParser(description='de-reverb audio wave.')
parser.add_argument('wavefile', metavar='WaveFile', type=str)
args = parser.parse_args()

stft_options = dict(size=512, shift=128)
sampling_rate = 16000
delay = 3
iterations = 5
taps = 10

signal_list = [
    sf.read('WaveDir/'+args.wavefile)[0]
]
y = np.stack(signal_list, axis=0)

Y = stft(y, **stft_options).transpose(2, 0, 1)

Z = wpe(
    Y,
    taps=taps,
    delay=delay,
    iterations=iterations,
    statistics_mode='full'
).transpose(1, 2, 0)
z = istft(Z, size=stft_options['size'], shift=stft_options['shift'])

sf.write('WPEDir/'+args.wavefile, z[0], sampling_rate)
