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
    pasta_destino = configurar_pasta_downloads()
    titulo_video = puxar_titulo_video(url)
    video_arquivo = os.path.join(pasta_destino, f"{titulo_video}.mp4")
    ydl_opts = {
        'format': 'bestvideo',
        'outtmpl': video_arquivo,
        'quiet':True,
        'no_warnings': True,
        'retries': 10,
        'extractor_retries': 3,
        'noplaylist': True,
        'verbose': True
    } 
    print("\nBaixando melhor video disponivel...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\nVídeo baixado com sucesso! Salvo em: {video_arquivo}")
        return titulo_video
    except Exception as e:
        print(f"\nErro ao baixar o vídeo: {e}")
        return None

def baixar_audio(url):
    pasta_destino = configurar_pasta_downloads()
    titulo_audio = puxar_titulo_video(url)
    audio_arquivo = os.path.join(pasta_destino, f"{titulo_audio}.%(ext)s")
    ydl_opts = {
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
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0'
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

def merge(titulo_video):
    pasta_destino = configurar_pasta_downloads()
    video_file = os.path.join(pasta_destino, f"{titulo_video}.mp4")
    audio_file = os.path.join(pasta_destino, f"{titulo_video}.mp3")
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
        titulo_final = limpar_nome_arquivo(titulo_video)
        base, ext = os.path.splitext(titulo_final)
        caminho_final = os.path.join(pasta_destino, f"{base}.mp4")
        contador = 1
        while os.path.exists(caminho_final):
            caminho_final = os.path.join(pasta_destino, f"{base}_{contador}.mp4")
            contador += 1
        os.rename(merged_file, caminho_final)
        print(f"\n✅ Merge completo! Arquivo renomeado como: {caminho_final}")
        os.remove(video_file)
        os.remove(audio_file)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao combinar arquivos: {e}")
    except FileNotFoundError:
        print("\n❌ Certifique-se de que o FFmpeg está instalado e no PATH do sistema.")

def puxar_titulo_video(url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            titulo = info.get('title', 'sem_titulo')
            return limpar_nome_arquivo(titulo)
    except Exception as e:
        print(f"Erro ao obter título do vídeo: {e}")
        return 'sem_titulo'

def menu_principal():
    while True:
        print("\n" + "=" * 50)
        print("🎬 YOUTUBE DOWNLOADER teste")
        print("=" * 50)
        print("1. Baixar Vídeo")
        print("2. Áudio")
        print("3. Playlist")
        print("4. Múltiplos Downloads")
        print("5. Sair")
        try:
            opcao = int(input('Sua escolha: '))
            if opcao in [1, 2]:
                url = input("\nCole a URL do Vídeo: ").strip()
                if opcao == 1:
                    titulo_video = baixar_video(url)
                    baixar_audio(url)
                    merge(titulo_video)
                    if titulo_video:
                        print(f"\nTítulo do vídeo: {titulo_video}")
                if opcao == 2:
                    baixar_audio(url)
            elif opcao == 3:
                print("Recurso desabilitado no momento.")
            elif opcao == 4:
                quantidade = int(input("\nQuantos vídeos deseja baixar? "))
                urls = [input(f"Cole a URL do vídeo {i+1}: ").strip() for i in range(quantidade)]
                for url in urls:
                    titulo_video = baixar_video(url)
                    baixar_audio(url)
                    merge(titulo_video)
            elif opcao == 5:
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
