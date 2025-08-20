# Conversor Multimídia com PyQt6

<p align="center">
  <img src="megafone.png" alt="Ícone" width="150"/>
</p>

<p align="center">
  Um aplicativo de desktop moderno construído com PyQt6 que converte texto em fala e transcreve áudio para texto, com uma interface elegante e responsiva com efeito de vidro jateado.
</p>

---

## Visão Geral

Este projeto é uma evolução de um simples conversor de mídia. A interface foi totalmente reconstruída em **PyQt6** para oferecer uma experiência de usuário superior, com design moderno, funcionalidades assíncronas (a interface não trava) e controles de áudio avançados.

### Pré-visualização

*(Você pode adicionar um screenshot da nova interface aqui)*

![placeholder](https://i.imgur.com/gYZrA2g.png)

## Funcionalidades

- **Interface Gráfica Moderna:** Construída com PyQt6, com um tema escuro e efeito de "vidro jateado" para um visual sofisticado.
- **Texto para Áudio (TTS):**
  - Converte texto em áudio usando `gTTS`.
  - **Botão de Interrupção:** Permite parar a reprodução do áudio a qualquer momento.
- **Áudio para Texto (STT):**
  - Transcrição de alta precisão usando o modelo `faster-whisper` da OpenAI.
  - O carregamento do modelo e a transcrição rodam em threads separadas para não congelar a aplicação.
- **Controles de Áudio Globais:**
  - **Controle de Volume:** Ajuste o volume da reprodução em tempo real com um slider.
  - **Botão Mudo:** Ative e desative o som rapidamente com um clique, com feedback visual no ícone.
- **Responsividade:** Feedback visual para o usuário com barras de progresso e desabilitação de botões durante tarefas longas.

## Configuração e Instalação

Para executar este projeto localmente, siga os passos abaixo.

### Pré-requisitos

- Python 3.9+
- Git (opcional, para clonar)

### Passos

1. **Clone ou baixe o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd text_to_speech_application
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   # Criar o ambiente
   python -m venv venv

   # Ativar no Windows (CMD/PowerShell)
   .\venv\Scripts\activate
   ```

3. **Instale as dependências:**
   As bibliotecas necessárias estão listadas no arquivo `requirements.txt`.
   ```bash
   pip install -r requirements.txt
   ```

## Como Usar

Com o ambiente virtual ativado, execute o script principal para iniciar a aplicação:

```bash
python text_to_speech_app.py
```

- Use os controles no topo da janela para ajustar o volume ou silenciar o áudio a qualquer momento.
- **Para converter texto em áudio:** Na aba "Texto para Áudio", digite o texto, clique em "Gerar Áudio" e use o botão "Interromper" se necessário.
- **Para transcrever um áudio:** Na aba "Áudio para Texto", selecione um arquivo de áudio e clique em "Transcrever Áudio".