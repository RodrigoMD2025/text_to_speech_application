import os
import pygame
import FreeSimpleGUI as sg
from gtts import gTTS
from faster_whisper import WhisperModel

# Inicializando o modelo Whisper para transcrição de voz
whisper_model = WhisperModel(
    "small", 
    compute_type="int8", 
    cpu_threads=os.cpu_count(), 
    num_workers=os.cpu_count()
)

class TextToSpeech:
    def __init__(self, lang="pt"):
        self.lang = lang  # Defina o idioma, 'pt' para português

    def speak(self, text):
        try:
            # Gerar o áudio com gTTS
            tts = gTTS(text=text, lang=self.lang)
            tts.save("audio_ia.mp3")  # Salva o áudio em formato MP3

            # Reproduzir o áudio gerado usando pygame
            pygame.mixer.init()
            pygame.mixer.music.load("audio_ia.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Aguarda a música terminar
                pass
            print("Áudio reproduzido com sucesso!")

        except Exception as e:
            print(f"Erro ao gerar o áudio: {e}")

# Função para transcrever áudio utilizando o modelo Whisper
def transcribe_audio(audio_file):
    try:
        # Carregar o arquivo de áudio e transcrever com Whisper
        result = whisper_model.transcribe(audio_file)
        
        # A resposta do Whisper é uma lista de tuplas
        # Exibimos o texto transcrito corretamente com o índice correto
        print("Texto transcrito:", result[0]['text'])  # A resposta pode ser uma lista de resultados
        return result[0]['text']  # Pegando o primeiro item da lista de transcrição
    except Exception as e:
        print(f"Erro ao transcrever o áudio: {e}")
        return None

# Função para criar a interface gráfica com PySimpleGUI
def create_gui():
    layout = [
        [sg.Text('Digite o texto que deseja transformar em áudio:')],
        [sg.Multiline(size=(50, 5), key='input_text')],
        [sg.Button('Gerar Áudio'), sg.Button('Sair')]
    ]
    
    # Criar a janela
    window = sg.Window('Texto para Áudio', layout)
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        
        if event == 'Gerar Áudio':
            text = values['input_text']
            if text:
                tts = TextToSpeech(lang="pt")
                tts.speak(text)  # Gera e reproduz o áudio
            else:
                sg.popup("Erro", "Por favor, insira algum texto para gerar o áudio.")

    window.close()

# Exemplo de uso da interface
if __name__ == "__main__":
    create_gui()