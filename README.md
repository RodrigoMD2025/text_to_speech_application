# 🎤 Text-to-Speech Application

Uma aplicação Python para conversão de texto em fala com interface gráfica intuitiva.

## 📋 Funcionalidades

- ✅ **Conversão Texto para Fala**: Transforme qualquer texto em áudio utilizando Google Text-to-Speech
- ✅ **Interface Gráfica Amigável**: Interface simples e intuitiva usando PySimpleGUI  
- ✅ **Reprodução de Áudio**: Reprodução automática do áudio gerado
- ✅ **Suporte ao Português**: Configurado para gerar áudio em português brasileiro
- 🔧 **Transcrição de Áudio**: Funcionalidade de speech-to-text usando Whisper (em desenvolvimento)

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **gTTS** - Google Text-to-Speech para geração de áudio
- **FreeSimpleGUI** - Interface gráfica
- **Pygame** - Reprodução de áudio
- **Faster-Whisper** - Transcrição de áudio (funcionalidade futura)

## 📦 Instalação

### Pré-requisitos
- Python 3.7 ou superior
- Conexão com internet (necessária para o gTTS)

### Instalando as dependências

```bash
pip install pygame FreeSimpleGUI gtts faster-whisper
```

## 🚀 Como usar

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/text-to-speech-app.git
cd text-to-speech-app
```

2. **Execute a aplicação:**
```bash
python main.py
```

3. **Usando a interface:**
   - Digite ou cole o texto desejado na área de texto
   - Clique em "Gerar Áudio" 
   - O áudio será gerado e reproduzido automaticamente
   - O arquivo `audio_ia.mp3` será salvo no diretório do projeto

## 📁 Estrutura do Projeto

```
text-to-speech-app/
│
├── main.py                 # Arquivo principal da aplicação
├── audio_ia.mp3           # Arquivo de áudio gerado (criado automaticamente)
├── requirements.txt        # Dependências do projeto
└── README.md              # Documentação do projeto
```

## 🔧 Configuração

O idioma padrão está configurado para português (`pt`). Para alterar:

```python
tts = TextToSpeech(lang="en")  # Para inglês
tts = TextToSpeech(lang="es")  # Para espanhol
```

## 📋 Requirements.txt

Crie um arquivo `requirements.txt` com as seguintes dependências:

```txt
pygame==2.5.2
FreeSimpleGUI==5.0.0
gtts==2.4.0
faster-whisper==0.10.0
```

## 🐛 Resolução de Problemas

### Erro de conexão com internet
- Verifique sua conexão com a internet, pois o gTTS requer conectividade

### Erro de áudio no Linux
```bash
sudo apt-get install python3-pygame
```

### Erro no Windows
- Certifique-se de que o pygame está corretamente instalado
- Em alguns casos, pode ser necessário instalar dependências adicionais do sistema

## 🔮 Funcionalidades Futuras

- [ ] Implementar interface para transcrição de áudio
- [ ] Adicionar mais opções de idiomas na interface
- [ ] Salvar configurações do usuário
- [ ] Suporte a diferentes formatos de áudio
- [ ] Controle de velocidade e tom da fala

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adicionando nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

Seu Nome - [seu-email@exemplo.com](mailto:seu-email@exemplo.com)

Link do Projeto: [https://github.com/seu-usuario/text-to-speech-app](https://github.com/seu-usuario/text-to-speech-app)

## 🙏 Agradecimentos

- [gTTS](https://github.com/pndurette/gTTS) - Pela excelente biblioteca de text-to-speech
- [FreeSimpleGUI](https://github.com/spyoungtech/FreeSimpleGUI) - Pela interface gráfica gratuita e open-source
- [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) - Pela implementação eficiente do Whisper