import numpy as np
from scipy.io.wavfile import read, write
from pydub import AudioSegment

def qam_constellation(M):
    """ Define uma constelação QAM para M-QAM. Exemplo com 16-QAM. """
    sqrt_M = int(np.sqrt(M))
    real_part = np.arange(-sqrt_M + 1, sqrt_M, 2)
    imag_part = np.arange(-sqrt_M + 1, sqrt_M, 2)
    constellation = np.array([complex(r, i) for r in real_part for i in imag_part])
    return constellation

def map_audio_to_qam(audio_samples, constellation):
    """ Mapeia amostras de áudio para uma constelação QAM. """
    num_symbols = len(audio_samples) // 2
    symbols = []
    for i in range(num_symbols):
        I = audio_samples[2 * i]
        Q = audio_samples[2 * i + 1]
        distances = np.abs(I + 1j * Q - constellation)
        nearest_symbol = constellation[np.argmin(distances)]
        symbols.append(nearest_symbol)
    return np.array(symbols)

def demodulate_qam_to_audio(demodulated_symbols):
    """ Converte símbolos QAM de volta para amostras de áudio. """
    audio_samples = []
    for symbol in demodulated_symbols:
        audio_samples.extend([np.real(symbol), np.imag(symbol)])
    return np.array(audio_samples).astype(np.int16)

# Carregar áudio e converter para mono e array de amostras
audio = AudioSegment.from_file("audio.wav").set_channels(1)
audio = audio.set_frame_rate(44100)
samples = np.array(audio.get_array_of_samples())

# Normalizar amostras de áudio
samples = samples / np.max(np.abs(samples))

# Constelação 16-QAM
M = 16
constellation = qam_constellation(M)

# Modulação
qam_symbols = map_audio_to_qam(samples, constellation)

# Demodulação (conversão de volta para áudio)
reconstructed_audio_samples = demodulate_qam_to_audio(qam_symbols)

# Converter de volta para um áudio wav
reconstructed_audio = (reconstructed_audio_samples * 32767).astype(np.int16)
write("reconstructed_audio.wav", audio.frame_rate, reconstructed_audio)