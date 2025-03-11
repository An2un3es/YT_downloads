import yt_dlp
import os
import re

def sanitize_filename(filename):
    """Remove caracteres inválidos para nomes de arquivos."""
    return re.sub(r'[\/:*?"<>|]', '_', filename)

def download_and_convert(url, save_path):
    ydl_opts = {
        'outtmpl': f"{save_path}/%(title)s.%(ext)s",  
        'format': 'bestvideo+bestaudio/best',  
        'merge_output_format': 'mkv' 
    }

    # Baixar o vídeo
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info_dict)  
        downloaded_file = downloaded_file.replace('.webm', '.mkv')

    # Verifica se o arquivo realmente existe antes de continuar
    if not os.path.exists(downloaded_file):
        print(f"Erro: Arquivo {downloaded_file} não encontrado!")
        return

    # Criar nome do MP4
    mp4_file = downloaded_file.replace('.mkv', '.mp4')

    # Converter para MP4
    os.system(f'ffmpeg -i "{downloaded_file}" -c:v copy -c:a copy "{mp4_file}"')

    # Remover o arquivo MKV original
    os.remove(downloaded_file)

    print(f"Download e conversão concluídos! Arquivo salvo como: {mp4_file}")

# URL do vídeo e pasta de destino
url = "https://www.youtube.com/watch?v=S4fWOF6HPuk"
save_path = "/Users/rodrigoantunes/Main/Trabalho/GITHUB"

download_and_convert(url, save_path)
