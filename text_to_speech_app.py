
import sys
import os
import pygame
from gtts import gTTS
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QTextEdit, QPushButton, QFileDialog, QMessageBox,
    QProgressBar, QSlider, QStyle
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from faster_whisper import WhisperModel

# --- Estilo da Aplicação (Tema Vidro Jateado) ---
STYLESHEET = """
    QMainWindow {
        background-color: #2c3e50;
    }
    QWidget {
        color: #ecf0f1;
        font-family: "Segoe UI", sans-serif;
        font-size: 10pt;
    }
    QTabWidget::pane {
        background-color: rgba(28, 40, 51, 0.85);
        border: 1px solid #3498db;
        border-top: 2px solid #3498db;
        border-radius: 5px;
    }
    QTabBar::tab {
        background: #34495e;
        color: #ecf0f1;
        padding: 10px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        min-width: 120px;
    }
    QTabBar::tab:selected {
        background: #3498db;
        color: #ffffff;
    }
    QTabBar::tab:hover {
        background: #4e6d8c;
    }
    QPushButton {
        background-color: #3498db;
        color: #ffffff;
        border-radius: 4px;
        padding: 8px;
        border: 1px solid #2980b9;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
    QPushButton:pressed {
        background-color: #1f618d;
    }
    QPushButton:disabled {
        background-color: #566573;
        color: #aab7c4;
    }
    #StopButton {
        background-color: #e74c3c;
        border: 1px solid #c0392b;
    }
    #StopButton:hover {
        background-color: #c0392b;
    }
    #StopButton:pressed {
        background-color: #a93226;
    }
    QTextEdit {
        background-color: rgba(28, 40, 51, 0.95);
        color: #ecf0f1;
        border: 1px solid #34495e;
        border-radius: 4px;
    }
    QLabel {
        color: #ecf0f1;
        font-weight: bold;
        background-color: transparent;
    }
    QProgressBar {
        border: 1px solid #34495e;
        border-radius: 4px;
        text-align: center;
        background-color: #1c2833;
        color: #ecf0f1;
    }
    QProgressBar::chunk {
        background-color: #3498db;
    }
    QStatusBar {
        background-color: #1c2833;
        font-weight: bold;
    }
    QSlider::groove:horizontal {
        border: 1px solid #34495e;
        height: 8px;
        background: #1c2833;
        margin: 2px 0;
        border-radius: 4px;
    }
    QSlider::handle:horizontal {
        background: #3498db;
        border: 1px solid #2980b9;
        width: 18px;
        margin: -5px 0;
        border-radius: 9px;
    }
"""

# --- Lógica de Negócio (reaproveitada e adaptada) ---

class TextToSpeech:
    def __init__(self, lang="pt"):
        self.lang = lang
        pygame.mixer.init()

    def speak(self, text):
        try:
            tts = gTTS(text=text, lang=self.lang)
            temp_audio_file = "temp_audio_ia.mp3"
            tts.save(temp_audio_file)

            pygame.mixer.music.load(temp_audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.music.unload()
            return True, "Áudio reproduzido com sucesso!"
        except Exception as e:
            return False, f"Erro ao gerar o áudio: {e}"

    def stop(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            print("Reprodução de áudio interrompida.")

class SpeechToText:
    def __init__(self):
        self.model = None

    def initialize_model(self):
        print("Inicializando o modelo Whisper...")
        self.model = WhisperModel(
            "small",
            compute_type="int8",
            cpu_threads=os.cpu_count(),
            num_workers=os.cpu_count()
        )
        print("Modelo Whisper carregado.")

    def transcribe(self, audio_file):
        if not self.model:
            raise RuntimeError("O modelo de transcrição não foi inicializado.")
        
        segments, info = self.model.transcribe(audio_file, beam_size=5)
        print(f"Idioma detectado: '{info.language}' com probabilidade {info.language_probability}")
        transcribed_text = "".join(segment.text for segment in segments).strip()
        return transcribed_text

# --- Thread para tarefas em segundo plano ---

class WorkerThread(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

# --- Interface Gráfica com PyQt6 ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor Multimídia")
        self.setWindowIcon(QIcon("megafone.png"))
        self.setGeometry(100, 100, 550, 500)
        self.setStyleSheet(STYLESHEET)

        self.tts = TextToSpeech(lang="pt")
        self.stt = SpeechToText()
        self.worker = None
        self.is_muted = False
        self.last_volume = 75

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Controles de Volume
        volume_controls_layout = self.create_volume_controls()
        main_layout.addLayout(volume_controls_layout)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.status_bar = self.statusBar()
        self.progress_bar = QProgressBar()
        self.status_bar.addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()

        self.create_text_to_speech_tab()
        self.create_speech_to_text_tab()

        self.load_whisper_model()
        self.set_volume(self.last_volume)

    def create_volume_controls(self):
        layout = QHBoxLayout()
        self.mute_button = QPushButton()
        self.mute_button.setFixedSize(32, 32)
        self.mute_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
        self.mute_button.clicked.connect(self.toggle_mute)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(self.last_volume)
        self.volume_slider.valueChanged.connect(self.set_volume)

        layout.addWidget(QLabel("Volume:"))
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.mute_button)
        return layout

    def create_text_to_speech_tab(self):
        tts_widget = QWidget()
        layout = QVBoxLayout(tts_widget)
        
        label = QLabel("Digite o texto que deseja transformar em áudio:")
        self.text_input = QTextEdit()
        
        button_layout = QHBoxLayout()
        self.generate_audio_button = QPushButton("Gerar Áudio")
        self.stop_audio_button = QPushButton("Interromper")
        self.stop_audio_button.setObjectName("StopButton")
        self.stop_audio_button.setEnabled(False)
        
        button_layout.addWidget(self.generate_audio_button)
        button_layout.addWidget(self.stop_audio_button)
        
        layout.addWidget(label)
        layout.addWidget(self.text_input)
        layout.addLayout(button_layout)
        
        self.tabs.addTab(tts_widget, "Texto para Áudio")
        self.generate_audio_button.clicked.connect(self.handle_generate_audio)
        self.stop_audio_button.clicked.connect(self.handle_stop_audio)

    def create_speech_to_text_tab(self):
        self.stt_widget = QWidget()
        layout = QVBoxLayout(self.stt_widget)
        
        file_selection_layout = QHBoxLayout()
        self.audio_file_path = QTextEdit()
        self.audio_file_path.setReadOnly(True)
        self.audio_file_path.setMaximumHeight(30)
        
        browse_button = QPushButton("Selecionar Arquivo")
        browse_button.clicked.connect(self.browse_for_audio_file)
        
        file_selection_layout.addWidget(self.audio_file_path)
        file_selection_layout.addWidget(browse_button)

        self.transcribe_button = QPushButton("Transcrever Áudio")
        self.transcription_output = QTextEdit()
        self.transcription_output.setReadOnly(True)

        layout.addLayout(file_selection_layout)
        layout.addWidget(self.transcribe_button)
        layout.addWidget(QLabel("Texto Transcrito:"))
        layout.addWidget(self.transcription_output)

        self.tabs.addTab(self.stt_widget, "Áudio para Texto")
        self.transcribe_button.clicked.connect(self.handle_transcribe_audio)
        
        self.stt_widget.setEnabled(False)

    def load_whisper_model(self):
        self.status_bar.showMessage("Carregando modelo de IA... Por favor, aguarde.")
        self.progress_bar.setRange(0, 0)
        self.progress_bar.show()

        self.worker = WorkerThread(self.stt.initialize_model)
        self.worker.finished.connect(self.on_model_loaded)
        self.worker.error.connect(self.on_task_error)
        self.worker.start()

    def on_model_loaded(self):
        self.stt_widget.setEnabled(True)
        self.status_bar.showMessage("Modelo carregado com sucesso!", 5000)
        self.progress_bar.hide()

    def browse_for_audio_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo de Áudio", "", "Arquivos de Áudio (*.mp3 *.wav *.m4a)")
        if file_path:
            self.audio_file_path.setText(file_path)

    def handle_generate_audio(self):
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Atenção", "Por favor, insira algum texto para gerar o áudio.")
            return

        self.generate_audio_button.setEnabled(False)
        self.stop_audio_button.setEnabled(True)
        self.generate_audio_button.setText("Gerando...")

        self.worker = WorkerThread(self.tts.speak, text)
        self.worker.finished.connect(self.on_audio_generation_finished)
        self.worker.error.connect(self.on_task_error)
        self.worker.start()

    def handle_stop_audio(self):
        self.tts.stop()

    def on_audio_generation_finished(self, result):
        success, message = result
        if "interrompida" not in message and success:
            QMessageBox.information(self, "Sucesso", message)
        elif not success:
            QMessageBox.critical(self, "Erro", message)
        
        self.generate_audio_button.setEnabled(True)
        self.stop_audio_button.setEnabled(False)
        self.generate_audio_button.setText("Gerar Áudio")

    def handle_transcribe_audio(self):
        audio_file = self.audio_file_path.toPlainText().strip()
        if not audio_file:
            QMessageBox.warning(self, "Atenção", "Por favor, selecione um arquivo de áudio.")
            return

        self.transcribe_button.setEnabled(False)
        self.transcribe_button.setText("Transcrevendo...")
        self.transcription_output.setText("Transcrevendo, por favor aguarde...")

        self.worker = WorkerThread(self.stt.transcribe, audio_file)
        self.worker.finished.connect(self.on_transcription_finished)
        self.worker.error.connect(self.on_task_error)
        self.worker.start()

    def on_transcription_finished(self, transcribed_text):
        self.transcription_output.setText(transcribed_text)
        QMessageBox.information(self, "Sucesso", "Transcrição concluída!")
        
        self.transcribe_button.setEnabled(True)
        self.transcribe_button.setText("Transcrever Áudio")

    def on_task_error(self, error_message):
        QMessageBox.critical(self, "Erro na Execução", error_message)
        self.generate_audio_button.setEnabled(True)
        self.generate_audio_button.setText("Gerar Áudio")
        self.stop_audio_button.setEnabled(False)
        self.transcribe_button.setEnabled(True)
        self.transcribe_button.setText("Transcrever Áudio")
        self.status_bar.showMessage("Ocorreu um erro.", 5000)
        self.progress_bar.hide()

    def set_volume(self, value):
        self.last_volume = value
        volume_float = value / 100.0
        pygame.mixer.music.set_volume(volume_float)
        if self.is_muted and value > 0:
            self.is_muted = False
            self.mute_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            pygame.mixer.music.set_volume(0)
            self.mute_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolumeMuted))
        else:
            self.set_volume(self.last_volume)
            self.mute_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaVolume))
            self.volume_slider.setValue(self.last_volume)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
