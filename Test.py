import win32com.client as win32
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image


def replace_text_in_photoshop(psd_file_path, number1, number2, output_file_path):
    try:
        # باز کردن فتوشاپ
        photoshop_app = win32.Dispatch("Photoshop.Application")
        photoshop_app.Open(psd_file_path)

        # دریافت سند فعال
        doc = photoshop_app.Application.ActiveDocument

        # پیدا کردن لایه‌های متن
        for layer in doc.Layers:
            if layer.Kind == 2:  # اگر نوع لایه متن بود
                if '1' in layer.TextItem.Contents:
                    layer.TextItem.Contents = layer.TextItem.Contents.replace('1', str(number1))
                elif '2' in layer.TextItem.Contents:
                    layer.TextItem.Contents = layer.TextItem.Contents.replace('2', str(number2))

        # ذخیره فایل با فرمت JPG
        jpg_options = win32.Dispatch('Photoshop.ExportOptionsSaveForWeb')
        jpg_options.Format = 6  # فرمت JPG
        jpg_options.Quality = 100  # کیفیت بالا

        doc.Export(ExportIn=output_file_path, ExportAs=2, Options=jpg_options)

        # بستن سند
        doc.Close()

        messagebox.showinfo("موفقیت", f'تصویر با موفقیت ذخیره شد: {output_file_path}')

    except Exception as e:
        messagebox.showerror("خطا", f"خطایی رخ داد: {str(e)}")


def open_psd_file():
    return filedialog.askopenfilename(title="انتخاب فایل PSD", filetypes=[("PSD Files", "*.psd")])


def save_output_file():
    return filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG Files", "*.jpg")])


def on_submit():
    psd_file_path = open_psd_file()
    if not psd_file_path:
        return

    number1 = entry_number1.get()
    number2 = entry_number2.get()

    output_file_path = save_output_file()
    if not output_file_path:
        return

    replace_text_in_photoshop(psd_file_path, number1, number2, output_file_path)


# ساخت رابط کاربری با tkinter
root = tk.Tk()
root.title("جایگزینی اعداد در فتوشاپ")
root.geometry("400x200")

# ایجاد لیبل و ورودی برای عدد اول
label_number1 = tk.Label(root, text="عدد اول:")
label_number1.pack(pady=5)
entry_number1 = tk.Entry(root)
entry_number1.pack(pady=5)

# ایجاد لیبل و ورودی برای عدد دوم
label_number2 = tk.Label(root, text="عدد دوم:")
label_number2.pack(pady=5)
entry_number2 = tk.Entry(root)
entry_number2.pack(pady=5)

# دکمه تایید
submit_button = tk.Button(root, text="تایید و ذخیره", command=on_submit)
submit_button.pack(pady=20)

# اجرای رابط کاربری
root.mainloop()