import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os
import re
from docx import Document
from faster_whisper import WhisperModel
import traceback

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def download_audio_and_transcribe():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập link YouTube")
        return

    try:
        # B1: Lấy thông tin video
        ydl_opts_info = {
            'quiet': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = sanitize_filename(info_dict.get('title', 'video'))

        # B2: Tải audio (MP3)
        status_label.config(text="🔊 Đang tải audio...")
        mp3_filename = f"{title}.mp3"
        ydl_opts_download = {
            'format': 'bestaudio/best',
            'outtmpl': f'{title}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts_download) as ydl:
            ydl.download([url])
        status_label.config(text=f"✅ Đã tải audio: {mp3_filename}")

        # B3: Dùng faster-whisper để chuyển audio thành text
        status_label.config(text="🧠 Đang xử lý audio bằng AI...")
        model = WhisperModel("base")  # hoặc "small", "medium"
        segments, _ = model.transcribe(mp3_filename, beam_size=5)

        text = ""
        for segment in segments:
            text += segment.text + "\n"

        # B4: Lưu file TXT
        with open(f"{title}.txt", "w", encoding="utf-8") as f:
            f.write(text)

        status_label.config(text="✅ Đã lưu văn bản từ audio!")
        messagebox.showinfo("Thành công", f"Đã lưu {title}.txt và {title}.docx")

    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Lỗi", str(e))
        status_label.config(text="❌ Đã xảy ra lỗi.")

# GUI setup
root = tk.Tk()
root.title("YouTube to MP3 & Text")

tk.Label(root, text="Nhập link YouTube:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=10)

download_button = tk.Button(root, text="🎧 Tải Audio & Chuyển Văn Bản", command=download_audio_and_transcribe)
download_button.pack(pady=10)

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
