import os
import pygame
import FreeSimpleGUI as sg
from gtts import gTTS
from faster_whisper import WhisperModel

# Inicializando o modelo Whisper para transcrição de voz
# Movido para dentro da função create_gui para carregar apenas quando a GUI é iniciada
whisper_model = None

def initialize_whisper():
    global whisper_model
    if whisper_model is None:
        print("Inicializando o modelo Whisper... Isso pode levar um momento.")
        # Mostra um popup enquanto o modelo carrega
        sg.popup_quick_message('Carregando modelo de IA, por favor aguarde...', auto_close_duration=5, background_color='blue', text_color='white', font=('Helvetica', 12))
        whisper_model = WhisperModel(
            "small",
            compute_type="int8",
            cpu_threads=os.cpu_count(),
            num_workers=os.cpu_count()
        )
        print("Modelo Whisper carregado.")

class TextToSpeech:
    def __init__(self, lang="pt"):
        self.lang = lang  # Defina o idioma, 'pt' para português

    def speak(self, text):
        try:
            # Gerar o áudio com gTTS
            tts = gTTS(text=text, lang=self.lang)
            # Usar um nome de arquivo temporário para evitar conflitos
            temp_audio_file = "temp_audio_ia.mp3"
            tts.save(temp_audio_file)

            # Reproduzir o áudio gerado usando pygame
            pygame.mixer.init()
            pygame.mixer.music.load(temp_audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)  # Evita uso excessivo de CPU
            
            pygame.mixer.music.unload() # Libera o arquivo
            print("Áudio reproduzido com sucesso!")
            
            # Opcional: remover o arquivo de áudio temporário
            # os.remove(temp_audio_file)

        except Exception as e:
            print(f"Erro ao gerar o áudio: {e}")
            sg.popup_error(f"Erro ao gerar áudio: {e}")

# Função para transcrever áudio utilizando o modelo Whisper
def transcribe_audio(audio_file):
    try:
        # A resposta do whisper é um iterador de segmentos
        segments, info = whisper_model.transcribe(audio_file, beam_size=5)
        
        # Juntar os segmentos de texto transcritos
        print(f"Idioma detectado: '{info.language}' com probabilidade {info.language_probability}")
        transcribed_text = "".join(segment.text for segment in segments).strip()
        
        print("Texto transcrito:", transcribed_text)
        return transcribed_text
    except Exception as e:
        print(f"Erro ao transcrever o áudio: {e}")
        return None

# Função para criar a interface gráfica
def create_gui():
    sg.theme('DarkBlue3')
    
    # Layout da aba de Texto para Áudio
    text_to_speech_layout = [
        [sg.Text('Digite o texto que deseja transformar em áudio:')],
        [sg.Multiline(size=(60, 5), key='-INPUT_TEXT-')],
        [sg.Button('Gerar Áudio', button_color=('white', 'green'))]
    ]

    # Layout da aba de Transcrição de Áudio
    speech_to_text_layout = [
        [sg.Text('Selecione um arquivo de áudio para transcrever:')],
        [sg.Input(key='-AUDIO_FILE-', readonly=True, size=(40, 1)), sg.FileBrowse('Selecionar', file_types=(("Arquivos de Áudio", "*.mp3 *.wav *.m4a"),))],
        [sg.Button('Transcrever Áudio', button_color=('white', 'green'))],
        [sg.Text('Texto Transcrito:')],
        [sg.Multiline(size=(60, 5), key='-TRANSCRIPTION_OUTPUT-', disabled=True, autoscroll=True, background_color='lightgrey', text_color='black')]
    ]

    # Layout principal com abas
    layout = [
        [sg.TabGroup([
            [sg.Tab('Texto para Áudio', text_to_speech_layout, key='-TAB1-'),
             sg.Tab('Áudio para Texto', speech_to_text_layout, key='-TAB2-')]
        ], key='-TABGROUP-')],
        [sg.Button('Sair', button_color=('white', 'red'))]
    ]
    
    window = sg.Window('Conversor Multimídia', layout, finalize=True)
    
    # Carrega o modelo Whisper depois que a janela principal é criada
    # para que o popup de carregamento possa ser exibido.
    initialize_whisper()

    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Sair':
            break
        
        if event == 'Gerar Áudio':
            text = values['-INPUT_TEXT-']
            if text and text.strip():
                tts = TextToSpeech(lang="pt")
                tts.speak(text)
            else:
                sg.popup("Atenção", "Por favor, insira algum texto para gerar o áudio.")

        if event == 'Transcrever Áudio':
            audio_file = values['-AUDIO_FILE-']
            if audio_file:
                # Feedback visual para o usuário
                window['-TRANSCRIPTION_OUTPUT-'].update("Transcrevendo, por favor aguarde...", text_color='darkorange')
                window.refresh() # Força a atualização da janela

                transcribed_text = transcribe_audio(audio_file)
                
                if transcribed_text is not None:
                    window['-TRANSCRIPTION_OUTPUT-'].update(transcribed_text, text_color='black')
                else:
                    window['-TRANSCRIPTION_OUTPUT-'].update("Falha na transcrição.", text_color='red')
                    sg.popup("Erro", "Não foi possível transcrever o áudio. Verifique o console para mais detalhes.")
            else:
                sg.popup("Atenção", "Por favor, selecione um arquivo de áudio primeiro.")

    window.close()

# Exemplo de uso da interface
if __name__ == "__main__":
    create_gui()