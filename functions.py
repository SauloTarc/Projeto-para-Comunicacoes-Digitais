import numpy as np
from pydub import AudioSegment
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
from scipy.signal import resample

# Função para calcular a frequência de Nyquist baseada no máximo da frequência do sinal
def calcular_frequencia_nyquist(f_max):
    return 2 * f_max

# Função para realizar a modulação PCM
def modula_pcm(audio, fs, bit_depth=16):
    # Normalizando o áudio para o intervalo [-1, 1]
    audio_normalizado = np.array(audio) / np.max(np.abs(audio))
    
    # Quantizando o áudio para a profundidade de bits desejada
    max_int = 2**(bit_depth - 1) - 1  # valor máximo para um número com sinal de 16 bits
    audio_quantizado = np.round(audio_normalizado * max_int).astype(np.int16)
    
    return audio_quantizado

# Função para realizar a demodulação (reconstrução do sinal)
def demodula_pcm(sinal_pcm, original_fs, novo_fs):
    # Ajustando o tamanho das amostras para corresponder à nova taxa de amostragem
    sinal_reconstruido = resample(sinal_pcm, int(len(sinal_pcm) * novo_fs / original_fs))
    return sinal_reconstruido

# Carregando o arquivo de áudio MP3
audio = AudioSegment.from_mp3("Falas do Singed - [Português Brasileiro].mp3")  # Substitua pelo seu arquivo MP3

# Convertendo para um array NumPy (mono)
audio = audio.set_channels(1).set_sample_width(2).set_frame_rate(44100)
samples = np.array(audio.get_array_of_samples(), dtype=np.float32)

# Aqui você pode definir a frequência máxima do áudio (exemplo: 22 kHz)
f_max = 22000  # Frequência máxima do áudio

# Calculando a frequência de Nyquist
f_s = calcular_frequencia_nyquist(f_max)
print(f"Frequência de amostragem (de acordo com Nyquist): {f_s} Hz")

# Modulação PCM (Amostragem e Quantização)
sinal_modulado_pcm = modula_pcm(samples, f_s)

# Salvando o áudio modulado em um arquivo WAV
write("audio_modulado_pcm_nyquist.wav", f_s, sinal_modulado_pcm)

# Agora, vamos realizar a demodulação do sinal PCM modulado
# Lendo o arquivo PCM modulado
fs_modulado, sinal_modulado = read("audio_modulado_pcm_nyquist.wav")

# A taxa de amostragem original (antes da modulação)
fs_original = 44100  # Pode ser ajustado para o valor que você usou na modulação

# A taxa de amostragem com base na frequência de Nyquist
fs_nyquist = fs_modulado  # A taxa de amostragem do arquivo PCM modulado

# Demodulando o sinal PCM (reconstruindo o sinal)
sinal_demodulado = demodula_pcm(sinal_modulado, fs_nyquist, fs_original)

# Plotando o sinal demodulado para visualização
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(sinal_modulado[:5000])
plt.title("Sinal Modulado PCM")
plt.xlabel("Amostras")
plt.ylabel("Amplitude")

plt.subplot(2, 1, 2)
plt.plot(sinal_demodulado[:5000])
plt.title("Sinal Demodulado (Reconstrução)")
plt.xlabel("Amostras")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()

# Salvando o áudio demodulado em um novo arquivo WAV
write("audio_demodulado.wav", fs_original, np.int16(sinal_demodulado))