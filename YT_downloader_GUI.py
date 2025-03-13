import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from downloader import download_and_convert  

FORMATS = ["mp3", "mp4", "webm", "mkv"]

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_var.set(folder_selected)

# Create main window
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x250")

# URL entry space
tk.Label(root, text="Video URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Directory selection
tk.Button(root, text="Select Directory", command=select_folder).pack()
folder_var = tk.StringVar()
tk.Label(root, textvariable=folder_var).pack()

# Format selection
tk.Label(root, text="Format:").pack()
format_var = tk.StringVar(value="")
format_menu = ttk.Combobox(root, textvariable=format_var, values=FORMATS, state="readonly")
format_menu.pack()

# Download Button
tk.Button(root, text="Download", command=lambda: download_and_convert(url_entry.get(), folder_var.get(), format_var.get())).pack()


# Center window
root.update_idletasks()
window_width = root.winfo_width()
window_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

root.mainloop()