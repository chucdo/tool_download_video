import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup


def get_paragraph_texts(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        texts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        return texts
    except Exception as e:
        return [f"[LỖI] {str(e)}"]


def fetch_and_display():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Thiếu URL", "Vui lòng nhập đường link trang web.")
        return

    result_box.delete(1.0, tk.END)  # Xóa nội dung cũ
    paragraphs = get_paragraph_texts(url)

    if paragraphs:
        for para in paragraphs:
            result_box.insert(tk.END, para + "\n")
    else:
        result_box.insert(tk.END, "[Không tìm thấy thẻ <p> nào hoặc lỗi tải trang.]")


# Tạo giao diện GUI
root = tk.Tk()
root.title("Lấy đoạn văn từ Website")
root.geometry("800x600")

# Ô nhập URL
tk.Label(root, text="Nhập đường link trang web:", font=("Arial", 12)).pack(pady=5)
url_entry = tk.Entry(root, width=80, font=("Arial", 12))
url_entry.pack(pady=5)

# Nút lấy nội dung
tk.Button(root, text="Lấy nội dung", font=("Arial", 12), command=fetch_and_display).pack(pady=10)

# Khung hiển thị kết quả
result_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 11))
result_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Khởi động ứng dụng
root.mainloop()
