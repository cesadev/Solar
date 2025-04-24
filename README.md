# Solar - YouTube Video Downloader (CLI)

Solar é uma ferramenta de linha de comando (CLI) que baixa vídeos e áudios do YouTube com alta qualidade.
Atualmente funciona por prompt, e realiza o merge entre vídeo e áudio separadamente para melhor qualidade final.

## Funcionalidades

Baixa vídeo na melhor qualidade do youtube

Baixa o áudio de qualquer vídeo do youtube

## Tecnologias utilizadas

yt-dlp - para download dos arquivos

ffmpeg - para combinar vídeo e áudio

Python 3 - linguagem usada no projeto

## Como usar

Clone o repositório:

Instale as dependências:

pip install yt-dlp
Certifique-se de que o ffmpeg está instalado e no PATH.

Execute o programa:

Siga as instruções no terminal para baixar vídeo, áudio ou ambos.

## Roadmap (Planos Futuros)

 Interface gráfica (GUI)

 Suporte a playlists

 Suporte a outras redes (Twitter, Instagram, TikTok)

 Download de legendas e transcrições

 Seleção de qualidade manual

## Organização dos Arquivos

main.py: arquivo principal com a lógica da CLI

Downloads são salvos automaticamente em ~/Solar

### Licença

Esse projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
