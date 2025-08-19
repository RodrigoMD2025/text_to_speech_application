# Conversor de Mídia: Texto para Áudio e Áudio para Texto

<img src="megafone.png" alt="Ícone" width="150"/>

Uma aplicação de desktop para Windows que oferece funcionalidades de conversão de texto em fala (Text-to-Speech) e transcrição de áudio para texto (Speech-to-Text) em uma interface gráfica simples e intuitiva.

## Funcionalidades

- **Texto para Áudio (TTS):** Converte qualquer texto inserido em um arquivo de áudio `.mp3` e o reproduz automaticamente. Utiliza a biblioteca `gTTS` do Google.
- **Áudio para Texto (STT):** Transcreve o conteúdo de arquivos de áudio (`.mp3`, `.wav`, `.m4a`) para texto. Utiliza o modelo de IA `Whisper` da OpenAI para alta precisão.
- **Interface Gráfica:** Possui uma interface com abas, construída com `FreeSimpleGUI`, que separa claramente as duas funcionalidades principais.
- **Feedback em Tempo Real:** Exibe notificações para o usuário durante operações demoradas, como o carregamento do modelo de IA e a transcrição de áudio.

## Configuração e Instalação

Para executar este projeto localmente, siga os passos abaixo.

### Pré-requisitos

- Python 3.9+
- Git

### Passos

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd text_to_speech_application-1
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # Criar o ambiente
   python -m venv .venv

   # Ativar no Windows
   .\.venv\Scripts\activate
   ```

3. **Instale as dependências:**
   As bibliotecas necessárias estão listadas no arquivo `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

## Como Usar

Com o ambiente virtual ativado, execute o script principal para iniciar a aplicação:

```bash
python "Text-to-Speech Application.py"
```

- **Para converter texto em áudio:** Vá para a aba "Texto para Áudio", digite o texto desejado e clique em "Gerar Áudio".
- **Para transcrever um áudio:** Vá para a aba "Áudio para Texto", clique em "Selecionar" para escolher um arquivo de áudio e, em seguida, clique em "Transcrever Áudio". O texto aparecerá na caixa de texto abaixo.