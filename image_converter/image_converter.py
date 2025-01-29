import os, sys
import subprocess
from tkinter import filedialog, StringVar, messagebox, Tk
import customtkinter as ctk
from customtkinter import CTkImage
import threading
from PIL import Image
import time


class ImageConverterApp:
    def __init__(self, root, theme_appearance, color_theme):
        ctk.set_appearance_mode(theme_appearance)  # 'Dark', 'Light', 'System'
        ctk.set_default_color_theme(color_theme)

        self.root = root
        self.root.title("Zta Image Converter")
        self.root.geometry("900x450")
        self.root.resizable(False, False)

        # Variables de selección
        self.input_format = StringVar(value="jpg")
        self.output_format = StringVar(value="png")
        self.input_file = None
        self.quality = StringVar(value="Alta")

        # Formatos disponibles
        self.formats = ["jpg", "png", "bmp", "gif", "jpeg", "ico", "tiff", "webp", "tga"]

        # Frame principal
        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True, side="left")

        # Menús de selección
        ctk.CTkLabel(self.frame, text="Formato de entrada:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.input_menu = ctk.CTkOptionMenu(self.frame, variable=self.input_format, values=self.formats)
        self.input_menu.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        ctk.CTkLabel(self.frame, text="Formato de salida:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.output_menu = ctk.CTkOptionMenu(self.frame, variable=self.output_format, values=self.formats)
        self.output_menu.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        ctk.CTkLabel(self.frame, text="Calidad de conversión:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.quality_menu = ctk.CTkOptionMenu(self.frame, variable=self.quality, values=["Baja", "Media", "Alta"])
        self.quality_menu.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        # Botones
        self.select_file_button = ctk.CTkButton(self.frame, text="Seleccionar archivo", command=self.select_file)
        self.select_file_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.convert_button = ctk.CTkButton(self.frame, text="Convertir", command=self.start_conversion, state="disabled")
        self.convert_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Estado
        self.status_label = ctk.CTkLabel(self.frame, text="Estado: Esperando selección de archivo", font=("Arial", 12))
        self.status_label.grid(row=8, column=0, columnspan=2, pady=10)

        self.time_estimated_label = ctk.CTkLabel(self.frame, text="Tiempo estimado: N/A", font=("Arial", 12))
        self.time_estimated_label.grid(row=9, column=0, columnspan=2, pady=5)

        # Previsualización de imagen
        self.preview_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.preview_frame.pack(padx=20, pady=20, fill="both", expand=True, side="right")
        self.image_label = ctk.CTkLabel(self.preview_frame, text="📌 Image Converter", font=("Arial", 18, "bold"))
        self.image_label.pack(pady=10)
        self.image_label2 = ctk.CTkLabel(self.preview_frame, text="Este programa permite convertir imagenes entre diferentes formatos\n"
                                         "utilizando FFmpeg. Puedes ajustar la calidad para \n"
                                        "optimizar la conversión según tus necesidades.\n", font=("Arial", 12))
        self.image_label2.pack(pady=10)
        self.image_label3 = ctk.CTkLabel(self.preview_frame, text="Previsualizacion", font=("Arial", 18, "bold"))
        self.image_label3.pack(pady=7)
        
        self.image_preview = ctk.CTkLabel(self.preview_frame, text="", font=("Arial", 11))
        self.image_preview.pack(padx=10, pady=10)

    def select_file(self):
        filetypes = [(f"Archivos {self.input_format.get().upper()}", f"*.{self.input_format.get()}")]
        self.input_file = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=filetypes)
        if self.input_file:
            self.status_label.configure(text=f"Archivo seleccionado: {os.path.basename(self.input_file)}")
            self.convert_button.configure(state="normal")
            self.preview_image(self.input_file)

    def preview_image(self, file_path):
        try:
            img = Image.open(file_path)
            img.thumbnail((250, 250))
            ctk_img = CTkImage(light_image=img, size=(250, 250))
            self.image_preview.configure(image=ctk_img)
            self.image_preview.image = ctk_img
        except Exception as e:
            messagebox.showerror("Error", f"No se puede cargar la imagen: {e}")

    def start_conversion(self):
        threading.Thread(target=self.convert_file).start()

    def convert_file(self):
        if not self.input_file:
            self.status_label.configure(text="Error: No se seleccionó ningún archivo.")
            return

        start_time = time.time()
        images_folder = os.path.expanduser("~\\Pictures")
        convert_folder = os.path.join(images_folder, "ZtaImageConverter")
        output_file = os.path.join(convert_folder, os.path.basename(self.input_file).rsplit(".", 1)[0] + f".{self.output_format.get()}")
        if not os.path.exists(convert_folder):
            os.makedirs(convert_folder)

        self.status_label.configure(text="Iniciando conversión...")

        quality_map = {"Baja": "31", "Media": "20", "Alta": "2"}
        quality_value = quality_map[self.quality.get()]

        try:
            command_convert = ["ffmpeg", "-i", self.input_file, "-q:v", quality_value, output_file]
            process = subprocess.Popen(command_convert, stderr=subprocess.PIPE, text=True)
            while process.poll() is None:
                elapsed_time = time.time() - start_time
                estimated_time_remaining = max(1, 5 - int(elapsed_time))
                self.time_estimated_label.configure(text=f"Tiempo estimado: {estimated_time_remaining}s")
                self.root.update_idletasks()

            self.status_label.configure(text=f"Conversión completada: {output_file}")
            messagebox.showinfo("Éxito", f"Imagen convertida correctamente: {output_file}")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


if __name__ == "__main__":
    theme_appearance = sys.argv[1] if len(sys.argv) > 1 else "System"  # Default: 'System'
    color_theme = sys.argv[2] if len(sys.argv) > 2 else "blue"  # Default: 'blue'
    root = ctk.CTk()
    app = ImageConverterApp(root, theme_appearance, color_theme)
    root.mainloop()
