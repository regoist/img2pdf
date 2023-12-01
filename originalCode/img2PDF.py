import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image

# リサイズの選択肢
resize_options = [
    (700, 1000),
    (800, 1280),
    (1080, 1920),
    (1440, 2560)
]

# GUIの作成
root = tk.Tk()
root.withdraw()

# ディレクトリの選択
messagebox.showinfo('注意', '結合する画像ファイルが含まれているディレクトリを選択してください。')
dir_path = filedialog.askdirectory(title='ディレクトリを選択してください')
if not dir_path:
    messagebox.showinfo('エラー', 'ディレクトリが選択されませんでした。プログラムを終了します。')
    exit()

# PDFの結合と保存
def merge_and_save_pdf():
    save_path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF ファイル', '*.pdf')], title='保存先とファイル名を指定してください')
    if not save_path:
        messagebox.showinfo('エラー', '保存先とファイル名が指定されませんでした。')
        return

    selected_option = resize_var.get()
    resize_width, resize_height = resize_options[selected_option]

    c = canvas.Canvas(save_path, pagesize=letter)
    
    # ディレクトリ内の画像ファイルを取得
    image_files = [f for f in os.listdir(dir_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # 画像ファイルを結合してPDFに描画
    for image_file in image_files:
        image_path = os.path.join(dir_path, image_file)
        img = Image.open(image_path)
        img = img.resize((resize_width, resize_height), Image.LANCZOS)
        img_width, img_height = img.size
        c.setPageSize((img_width, img_height))
        c.drawImage(image_path, 0, 0, img_width, img_height)
        c.showPage()
    
    # PDFを保存
    c.save()
    
    messagebox.showinfo('完了', 'PDFの結合が完了し、ファイルが保存されました。')
    root.quit()

# GUIの表示
root = tk.Tk()
root.title('PDF 結合とリサイズ')
root.geometry('300x200')

# リサイズ選択のラジオボタン
resize_var = tk.IntVar()
for i, option in enumerate(resize_options):
    resize_radio = tk.Radiobutton(root, text=f'{option[0]} × {option[1]}', value=i, variable=resize_var)
    resize_radio.pack(anchor='w')

# 結合ボタン
merge_button = tk.Button(root, text='結合と保存', command=merge_and_save_pdf)
merge_button.pack()

root.mainloop()