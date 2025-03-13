import yt_dlp
import os
from tkinter import messagebox

def download_and_convert(url, save_path, format):
    if not url or not save_path or not format:
        messagebox.showerror("Error", "Fill every field")
        return
    
    ydl_opts = {
        'outtmpl': f"{save_path}/%(title)s.%(ext)s",
        'format': 'bestaudio' if format == "mp3" else (
            'bestvideo[ext=webm]+bestaudio[ext=webm]/best' if format == "webm" else 'bestvideo+bestaudio/best'
        ),
        'merge_output_format': format if format != "webm" else None,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': format
        }] if format != "webm" else [],
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download finished!")
    except Exception as e:
        messagebox.showerror("Error", f"Download failed: {e}")