import re
import cv2
import os

# Lista de palavras do vocabulário básico de Libras com links para os vídeos (exemplo fictício)
VIDEOS_LIBRAS = {
    "EU": "gifs/euSm_Prog001.mp4",
    "M-I-S-T-U-R-A": "gifs/misturar1Sm_Prog001.mp4",
    "N-A@o": "gifs/nao2Sm_Prog001.mp4",
    "M-E-X-E-R" : "gifs/mexerSm_Prog001.mp4",    
}

VOCABULARIO_LIBRAS = {
    "EU": "EU",
    "TE": "T-E",
    "OUÇO": "ouC@",
    "ESSA": "E-S-S-A",
    "MISTURA": "M-I-S-T-U-R-A",
    "NÃO": "N-A@o",
    "DEU": "D-E-U",
    "CERTO": "C-E-R-T-O",
    "ISSO": "I-S-S-O",
    "DEVE": "D-E-V-E",
    "DOER": "D-O-E-R",
    "CHORAR": "C-H-O-R-A-R",
    "MISTURAR": "M-I-S-T-U-R-A-R",
    "MEXER": "M-E-X-E-R",
    "JÁ": "J-A@",
    "ERA": "E-R-A",
    "HORA": "H-O-R-A",
    "OU": "O-U",
    "ESTOU": "E-S-T-O-U",
    "CAMINHO": "C-A-M-I-N-H-O",
    "ESTÁ": "E-S-T-A@",
    "AGRADAR": "A-G-R-A-D-O",
    "BATIDO": "B-A-T-I-D-O",
    "MISTURAR": "M-I-S-T-U-R-A-D-O",
}

# Substituir caracteres especiais (acentos e tils)
def substituir_caracteres(texto):
    return (
        texto.replace("á", "a@")
        .replace("ã", "a@")
        .replace("â", "a@")
        .replace("é", "e@")
        .replace("ê", "e@")
        .replace("í", "i@")
        .replace("ó", "o@")
        .replace("õ", "o@")
        .replace("ô", "o@")
        .replace("ú", "u@")
        .replace("ç", "c@")
        .replace("Á", "A@")
        .replace("Ã", "A@")
        .replace("Â", "A@")
        .replace("É", "E@")
        .replace("Ê", "E@")
        .replace("Í", "I@")
        .replace("Ó", "O@")
        .replace("Õ", "O@")
        .replace("Ô", "O@")
        .replace("Ú", "U@")
        .replace("Ç", "C@")
    )

# Traduzir uma palavra para glosa
def traduzir_palavra(palavra):
    palavra = substituir_caracteres(palavra)
    if palavra in VOCABULARIO_LIBRAS:
        return VOCABULARIO_LIBRAS[palavra]
    return palavra.upper()

# Mostrar o vídeo do sinal usando OpenCV
def mostrar_video_sinal(sinal):
    video_path = VIDEOS_LIBRAS.get(sinal)
    if video_path and os.path.exists(video_path):
        print(f"Mostrando o vídeo para o sinal: {sinal}")
        
        # Abrir o vídeo com OpenCV
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print("Erro ao abrir o vídeo.")
            return
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Mostrar o vídeo na tela
            cv2.imshow(f"Sinal: {sinal}", frame)
            
            # Aguardar por uma tecla para continuar
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Pressione 'q' para fechar
                break
        
        cap.release()
        cv2.destroyAllWindows()
    else:
        print(f"Vídeo para o sinal {sinal} não encontrado.")

# Traduzir uma frase inteira para glosa e mostrar os vídeos
def traduzir_frase_com_videos(frase):
    palavras = re.findall(r"\b\w+\b", frase)
    traducao = []
    
    # Traduzir palavra por palavra e mostrar vídeos correspondentes
    for palavra in palavras:
        glosa = traduzir_palavra(palavra)
        traducao.append(glosa)
        mostrar_video_sinal(glosa)  # Exibir o vídeo correspondente ao sinal
        
    return " ".join(traducao)
