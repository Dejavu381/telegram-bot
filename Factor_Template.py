import os
import shutil
import win32com.client
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
from tkinter import ttk  # Import ttk for more modern widgets

class WordTemplateFillerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("پر کردن قالب Word")

        # LabelFrame برای انتخاب فایل Word
        file_frame = tk.LabelFrame(self.root, text="انتخاب فایل Word", padx=10, pady=10)
        file_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.EW)

        # Button برای باز کردن فایل Word
        self.open_button = tk.Button(file_frame, text="انتخاب فایل", command=self.open_word_file)
        self.open_button.grid(row=0, column=0, padx=10, pady=10)

        # Label برای نمایش نام فایل انتخاب شده
        self.filename_label = tk.Label(file_frame, text="", wraplength=300, justify=tk.RIGHT)
        self.filename_label.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Button برای انتخاب عکس جدید
        self.select_image_button = tk.Button(file_frame, text="انتخاب عکس", command=self.select_image,
                                             state=tk.DISABLED)
        self.select_image_button.grid(row=1, column=0, padx=10, pady=10)

        # Label برای نمایش نام عکس انتخاب شده
        self.image_label = tk.Label(file_frame, text="", wraplength=300, justify=tk.RIGHT)
        self.image_label.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # LabelFrame برای ورودی‌ها
        input_label_frame = tk.LabelFrame(self.root, text="ورودی‌ها", padx=10, pady=10)
        input_label_frame.grid(row=2, column=0, padx=10, pady=10, sticky=tk.EW)

        # Label و Entry برای هر ورودی
        self.inputs = {}
        placeholders = [
            'تاریخ', 'نام و نام خانوادگی', 'شماره', 'code', 'نوع', 'vazn', 'سنگ اول', 'sang1', 'سنگ دوم', 'sang2',
            'سنگ سوم', 'sang3', 'gheymat', 'جنس', 'گرم', 'dolar'
        ]

        stone_options = [
            'برلیان تمام تراش سفید', 'باگت برلیان سفید', 'اشک برلیان سفید', 'مارکیز برلیان سفید', 'تری انگل برلیان سفید',
            'سنگ زمرد کلمبیا', 'سنگ زمرد زامبیا', 'تخمه برلیان سفید', 'سنگ یاقوت کبود', 'سنگ سانچیا', 'سنگ جیپسون',
            'سنگ زیرکونیوم', 'سنگ آمیتیست', '...'
        ]

        for idx, placeholder in enumerate(placeholders):
            if placeholder == 'جنس':
                label = tk.Label(input_label_frame, text=f"{placeholder}:", justify=tk.RIGHT, anchor="e")
                label.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.E)
                self.fee_var = StringVar()
                self.fee_var.set("")  # Ensure the default value is empty
                option_menu = ttk.Combobox(input_label_frame, textvariable=self.fee_var, values=["طلا", "پلاتین"], state="readonly")
                option_menu.grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
                self.inputs[placeholder] = self.fee_var
            elif placeholder in ['سنگ اول', 'سنگ دوم', 'سنگ سوم']:
                label = tk.Label(input_label_frame, text=f"{placeholder}:", justify=tk.RIGHT, anchor="e")
                label.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.E)
                var = StringVar()
                var.set("")  # Ensure the default value is empty
                option_menu = ttk.Combobox(input_label_frame, textvariable=var, values=stone_options, state="readonly")
                option_menu.grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
                self.inputs[placeholder] = var
                option_menu.bind("<<ComboboxSelected>>", self.check_other_option)
            else:
                label = tk.Label(input_label_frame, text=f"{placeholder}:", justify=tk.RIGHT, anchor="e")
                label.grid(row=idx, column=1, padx=10, pady=5, sticky=tk.E)
                entry = tk.Entry(input_label_frame, width=30)
                entry.grid(row=idx, column=0, padx=10, pady=5, sticky=tk.W)
                self.inputs[placeholder] = entry

        # Button برای اجرای جایگزینی و ذخیره فایل
        self.fill_button = tk.Button(self.root, text="پر کردن قالب و ذخیره", command=self.fill_and_save,
                                     state=tk.DISABLED)
        self.fill_button.grid(row=3, column=0, padx=10, pady=20)

        # Variable برای ذخیره عکس انتخاب شده
        self.selected_image_path = None
        # Variable برای ذخیره مسیر فایل انتخاب شده
        self.template_file = None

    def open_word_file(self):
        # باز کردن فایل قالب Word
        self.template_file = filedialog.askopenfilename(filetypes=[("فایل‌های Word", "*.docx")])
        if self.template_file:
            self.filename_label.config(text=f"فایل انتخاب شده: {self.template_file}")
            self.fill_button.config(state=tk.NORMAL)
            self.select_image_button.config(state=tk.NORMAL)

    def select_image(self):
        # باز کردن فایل تصویر
        self.selected_image_path = filedialog.askopenfilename(
            filetypes=[("فایل‌های تصویر", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if self.selected_image_path:
            self.image_label.config(text=f"عکس انتخاب شده: {self.selected_image_path}")

    def check_other_option(self, event):
        """
        If the '...' option is selected, allow the user to enter custom text.
        """
        widget = event.widget
        selected_option = widget.get()
        if selected_option == "...":
            custom_text = tk.simpledialog.askstring("ورود متن سفارشی", "لطفاً متن دلخواه را وارد کنید:")
            if custom_text:
                widget.set(custom_text)

    def replace_text_and_shapes_with_pywin32(self, doc_path, data):
        """
        Replace placeholders in textboxes and replace square shapes with the selected image.
        """
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        try:
            doc_path = os.path.abspath(doc_path)  # Ensure the path is absolute
            doc = word.Documents.Open(doc_path)

            # Replace text in textboxes
            for shape in doc.Shapes:
                try:
                    if shape.Type == 17:  # Check if shape is a textbox
                        for placeholder, replacement in data.items():
                            if placeholder in shape.TextFrame.TextRange.Text:
                                # Explicitly encode the replacement to ensure correct characters
                                replacement = replacement.encode('utf-8').decode('utf-8')
                                shape.TextFrame.TextRange.Text = shape.TextFrame.TextRange.Text.replace(placeholder, replacement)
                except Exception as shape_error:
                    print(f"Error processing textbox shape: {shape_error}")

            # Replace images in square shapes
            new_image_path = self.selected_image_path
            if new_image_path:
                temp_image_path = os.path.join(os.getenv('TEMP'), 'temp_image.png')
                shutil.copy(new_image_path, temp_image_path)
                for shape in doc.Shapes:
                    if shape.Fill.Type == 6:  # msoFillPicture indicates the shape has a picture fill
                        if shape.Width == shape.Height:  # Check if shape is square
                            shape.Fill.UserPicture(temp_image_path)

            # Get the directory of the original file
            original_file_path = os.path.dirname(self.template_file)

            # Save changes with the name provided by user and .docx extension
            filename = self.inputs['نام و نام خانوادگی'].get() + ".docx"
            save_as_path = os.path.join(original_file_path, filename)

            # Save the document with Save As dialog
            doc.SaveAs(save_as_path)

            # Close the document
            doc.Close()

            messagebox.showinfo("تکمیل و ذخیره شد", f'فایل "{filename}" با موفقیت ذخیره شد.')
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در اجرای عملیات: {e}")
        finally:
            word.Quit()

    def fill_and_save(self):
        if not self.template_file:
            messagebox.showerror("خطا", "لطفاً ابتدا یک فایل Word را انتخاب کنید.")
            return

        if not self.selected_image_path:
            messagebox.showerror("خطا", "لطفاً یک عکس را انتخاب کنید.")
            return

        # دریافت ورودی‌های کاربر از تمام Entry ها
        data = {}
        for placeholder, entry in self.inputs.items():
            data[placeholder] = entry.get() if isinstance(entry, tk.Entry) else entry.get()

        # جایگزینی متن‌ها در فایل Word و جایگزینی عکس در شیپ‌های مربع
        self.replace_text_and_shapes_with_pywin32(self.template_file, data)


if __name__ == "__main__":
    root = tk.Tk()
    app = WordTemplateFillerApp(root)
    root.mainloop()