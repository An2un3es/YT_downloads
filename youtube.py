from multiprocessing.connection import wait
import yt_dlp
import os
import re
import tkinter as tk 
from tkinter import filedialog

FORMATS=["mp3", "mp4", "webm", "mkv"]

def sanitize_filename(filename):
    #Remove caracteres inválidos para nomes de arquivos.
    return re.sub(r'[\/:*?"<>|]', '_', filename)

def download_and_convert(url, save_path, format):
    # Configuração do yt-dlp
    ydl_opts = {
        'outtmpl': f"{save_path}/%(title)s.%(ext)s",
        'format': 'bestaudio' if format == "mp3" else (
            'bestvideo[ext=webm]+bestaudio[ext=webm]/best' if format == "webm" else 'bestvideo+bestaudio/best'
        ),
        'merge_output_format': format if format != "webm" else None,  # WebM precisa de conversão manual
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': format
        }] if format != "webm" else [],
    }

    # Baixar o vídeo/áudio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info_dict)

    print(f"\n \n \n PRIMEIRO DOWNLOAD SALVO COMO: {downloaded_file} \n \n \n ")

    '''if not os.path.exists(downloaded_file):
        print(f"Erro: Arquivo {downloaded_file} não encontrado!")
        return'''

    # Se o formato for WebM e não estiver em WebM, converter
    if format == "webm" and not downloaded_file.endswith(".webm"):
        webm_file = downloaded_file.rsplit(".", 1)[0] + ".webm"
        os.system(f'ffmpeg -i "{downloaded_file}" -c:v libvpx-vp9 -c:a libopus "{webm_file}"')
        os.remove(downloaded_file)  # Apaga o original após converter
        print(f"Conversão concluída! Arquivo salvo como: {webm_file}")


    print(f"Download concluído! Arquivo salvo como: {downloaded_file}")
    print("Processo finalizado! ✅")


    
def open_file_dialogue():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    folder= filedialog.askdirectory()

    if folder:
        print(f"Selected folder: {folder}")
    return folder


if __name__ == "__main__":

    while True:
        url = input("Enter the link or URL of the YT video: ")
        while True:  
            format= input("Enter the desired format (mp3, mp4, mkv or webm): ")
            if format.lower() == "exit":
                exit()
            if format.lower() in FORMATS:
                break
            else:
                print("Format not available.\n If you want to continue please choose between mp3, mp4, mkv or webm.\n If not type 'exit'")

        save_dir = open_file_dialogue()
        if save_dir:
            download_and_convert(url, save_dir, format.lower())
        else:
            print("Invalid save location.")
        while True:  
            ans = input("Want to download more? (y/n): ")
            match ans.lower():  # Converte para minúsculas para simplificar
                case "y":
                    break 
                case "n":
                    exit()  
                case _:
                    print("Invalid response. Please enter 'y' for yes or 'n' for no.\n")
        




