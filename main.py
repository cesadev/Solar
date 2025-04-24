import os #Para escolher as pastas e baixar os arquivos
import yt_dlp
from time import sleep
import subprocess
import re

def configurar_pasta_downloads():
    downloads_pasta = os.path.join(os.path.expanduser('~'), 'Solar')
    os.makedirs(downloads_pasta, exist_ok=True)
    return downloads_pasta

def baixar_video(url):
    #Baixa o melhor vídeo sem áudio e retorna o título
    pasta_destino = configurar_pasta_downloads() #Puxa o diretório da pasta
    video_arquivo = os.path.join(pasta_destino, "video.mp4")
    ydl_opts = { #Opções do yt_dlp
        'format': 'bestvideo',
        'outtmpl': video_arquivo,
        'quiet':True,
        'no_warnings': True,
        'retries': 10,
        'extractor_retries': 3,
        'noplaylist': True,
        'verbose': True
    } 
    print("\nBaixando melhor video disponivel...") #Mensagem de video baixando
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True) #Pega infos do vídeo
            titulo_video = info.get('title', 'sem_titulo') #Pega o título
        print(f"\nVídeo baixado com sucesso! Salvo em: {video_arquivo}")
        return titulo_video
    except Exception as e:
        print(f"\nErro ao baixar o vídeo: {e}")
        return None

def baixar_audio(url):
    pasta_destino = configurar_pasta_downloads()
    audio_arquivo = os.path.join(pasta_destino, "audio")

    ydl_opts = { #Opções do yt_dlp
        'format': 'bestaudio',
        'outtmpl': audio_arquivo,
        'quiet': True,
        'no_warnings': True,
        'retries': 10,
        'extractor_retries': 3,
        'noplaylist': True,
        'verbose': True,
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio', #Extraindo o áudio
                'preferredcodec': 'mp3', #Convertendo para mp3
                'preferredquality': '0' #Qualidade preferida (Melhor)
            }
        ]
    }

    print("\nBaixando o melhor áudio disponível...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\nÁudio baixado. Salvo em {audio_arquivo}")
    except Exception as e:
        print(f"\nErro ao baixar o áudio: {e}")
        return None

def merge(titulo_video): #Mescla vídeo e áudio e renomeia o título.
    pasta_destino = configurar_pasta_downloads()
    video_file = os.path.join(pasta_destino, "video.mp4")
    audio_file = os.path.join(pasta_destino, "audio.mp3")
    merged_file = os.path.join(pasta_destino, "merged_output.mp4") 

    if not os.path.exists(video_file):
        print(f"\n❌ O arquivo de vídeo {video_file} não foi encontrado!")
        return
    if not os.path.exists(audio_file):
        print(f"\n❌ O arquivo de áudio {audio_file} não foi encontrado!")
        return

    print("\n🔄 Realizando o merge do vídeo e áudio...")
    try:
        command = [
            "ffmpeg",
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            merged_file
        ]
        subprocess.run(command, check=True)
        
        # Renomeia o arquivo para o título do vídeo
        titulo_final = limpar_nome_arquivo(titulo_video)
        caminho_final = os.path.join(pasta_destino, f"{titulo_final}.mp4")
        os.rename(merged_file, caminho_final)

        print(f"\n✅ Merge completo! Arquivo renomeado como: {caminho_final}")

        os.remove(video_file)
        os.remove(audio_file)

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao combinar arquivos: {e}")
    except FileNotFoundError:
        print("\n❌ Certifique-se de que o FFmpeg está instalado e no PATH do sistema.")

    return

def menu_principal():
    while True:
        print("\n" + "=" * 50)
        print("🎬 YOUTUBE DOWNLOADER teste")
        print("=" * 50)
        print("1. Baixar vídeo")
        print("2. Playlist")
        print("3. Áudio")
        print("4. Sair")

        try:
            opcao = int(input('Sua escolha: '))
            if opcao ==1:
                url = input("\nCole a URL do Vídeo: ").strip()
                titulo_video = baixar_video(url)
                baixar_audio(url)
                merge(titulo_video)

                if titulo_video:
                    print(f"\nTítulo do vídeo: {titulo_video}")
            elif opcao in [2,3]:
                print("Recurso desabilitado no momento.")
            elif opcao == 4:
                print('\nAté logo!')
                break
            else:
                print("\nOpção inválida! Tente novamente.")
                
        except ValueError:
            print("\nDigite apenas números!")
        sleep(1)

def limpar_nome_arquivo(nome):
    return re.sub(r'[<>:"/\\|?*]', '', nome)

if __name__ == "__main__":
    menu_principal()