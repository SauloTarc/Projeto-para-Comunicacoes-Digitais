import re
import cv2
import os
import time

# Lista de vídeos das letras do alfabeto (exemplo fictício, use o caminho correto)
VIDEOS_LETRAS = {
    "A": "gifs/aSm_Prog001.mp4",
    "B": "gifs/bSm_Prog001.mp4",
    "C": "gifs/cSm_Prog001.mp4",
    "D": "gifs/dSm_Prog001.mp4",
    "E": "gifs/eSm_Prog001.mp4",
    "F": "gifs/fSm_Prog001.mp4",
    "G": "gifs/gSm_Prog001.mp4",
    "H": "gifs/hSm_Prog001.mp4",
    "I": "gifs/iSm_Prog001.mp4",
    "J": "gifs/jSm_Prog001.mp4",
    "K": "gifs/kSm_Prog001.mp4",
    "L": "gifs/lSm_Prog001.mp4",
    "M": "gifs/mSm_Prog001.mp4",
    "N": "gifs/nSm_Prog001.mp4",
    "O": "gifs/oSm_Prog001.mp4",
    "P": "gifs/pSm_Prog001.mp4",
    "Q": "gifs/qSm_Prog001.mp4",
    "R": "gifs/rSm_Prog001.mp4",
    "S": "gifs/sSm_Prog001.mp4",
    "T": "gifs/tSm_Prog001.mp4",
    "U": "gifs/uSm_Prog001.mp4",
    "V": "gifs/vSm_Prog001.mp4",
    "W": "gifs/wSm_Prog001.mp4",
    "X": "gifs/xSm_Prog001.mp4",
    "Z": "gifs/zSm_Prog001.mp4",
}

VIDEOS_LIBRAS = {
    "EU": "gifs/euSm_Prog001.mp4",
    "MISTURAR": "gifs/misturar1Sm_Prog001.mp4",
    "NÃO": "gifs/nao2Sm_Prog001.mp4",
    "MEXER": "gifs/mexerSm_Prog001.mp4",    
    "AGRADAR": "gifs/agradarSm_Prog001.mp4",
    "CAMINHO": "gifs/caminhoSm_Prog001.mp4",
    "DOER": "gifs/doerSm_Prog001.mp4",
    "HORA": "gifs/hora1Sm_Prog001.mp4",
    "OUÇO": 'gifs/ouvirSm_Prog001.mp4',
    "MISTURA": 'gifs/misturaSm_Prog001.mp4',
    "ESCURO": 'gifs/escuroSm_Prog001.mp4',
    "ESTRELAS": 'gifs/estrelaSm_Prog001.mp4',
    "BILHANTE": 'gifs/brilharSm_Prog001.mp4',
    "NOITE": 'gifs/noite1Sm_Prog001.mp4',
}

VOCABULARIO_LIBRAS = {
    "EU": "E-U",
    "TE": "T-E",
    "OUCO": "O-U-Ç-O",
    "ESSA": "E-S-S-A",
    "MISTURA": "M-I-S-T-U-R-A",
    "NÃO": "N-Ã-O",
    "DEU": "D-E-U",
    "CERTO": "C-E-R-T-O",
    "ISSO": "I-S-S-O",
    "DEVE": "D-E-V-E",
    "DOER": "D-O-E-R",
    "CHORAR": "C-H-O-R-A-R",
    "MISTURAR": "M-I-S-T-U-R-A-R",
    "MEXER": "M-E-X-E-R",
    "JÁ": "J-Á",
    "ERA": "E-R-A",
    "HORA": "H-O-R-A",
    "OU": "O-U",
    "ESTOU": "E-S-T-O-U",
    "CAMINHO": "C-A-M-I-N-H-O",
    "ESTÁ": "E-S-T-Á",
    "AGRADAR": "A-G-R-A-D-O",
    "BATIDO": "B-A-T-I-D-O",
}

# Traduzir uma palavra para glosa
def traduzir_palavra(palavra):
    if palavra in VOCABULARIO_LIBRAS:
        return VOCABULARIO_LIBRAS[palavra]
    return palavra.upper()

# Mostrar o vídeo do sinal usando OpenCV
def mostrar_video_sinal(sinal):
    video_path = VIDEOS_LIBRAS.get(sinal)
    if video_path and os.path.exists(video_path):
        print(f"Mostrando o vídeo para o sinal: {sinal}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Erro ao abrir o vídeo.")
            return
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.imshow(f"Sinal: {sinal}", frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):  # Pressione 'q' para fechar
                break
            
        cap.release()
        cv2.destroyAllWindows()
    else:
        print(f"Vídeo para o sinal {sinal} não encontrado.")

# Mostrar o vídeo da letra
def mostrar_video_letra(letra):
    video_path = VIDEOS_LETRAS.get(letra)
    if video_path and os.path.exists(video_path):
        print(f"Mostrando o vídeo para a letra: {letra}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Erro ao abrir o vídeo.")
            return
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.imshow(f"Letra: {letra}", frame)
            if cv2.waitKey(100) & 0xFF == ord('q'):  # Pressione 'q' para fechar
                break
            
        cap.release()
        cv2.destroyAllWindows()
    else:
        print(f"Vídeo para a letra {letra} não encontrado.")

# Soletrar a palavra
def soletrar_palavra(palavra):
    letras = list(palavra)
    glosa = " ".join(letras)  # Soletra a palavra
    print(f"Soletrando: {glosa}")
    
    for letra in letras:
        mostrar_video_letra(letra.upper())  # Exibe o vídeo de cada letra
        
    return glosa

# Traduzir uma frase inteira para glosa e mostrar os vídeos
def traduzir_frase_com_videos(frase):
    palavras = re.findall(r"\b\w+\b", frase.upper())
    traducao = []

    # Traduzir palavra por palavra e mostrar vídeos correspondentes
    for palavra in palavras:
        glosa = traduzir_palavra(palavra)  # Obtém a tradução ou soletra a palavra
        traducao.append(glosa)

        if palavra in VIDEOS_LIBRAS:  # Verifica se existe vídeo para a palavra
            mostrar_video_sinal(palavra)
        else:
            print(f"Vídeo para o sinal '{palavra}' não encontrado. Soletrando...")
            for letra in palavra:
                mostrar_video_letra(letra.upper())  # Exibe vídeos das letras da palavra

    return " ".join(traducao)