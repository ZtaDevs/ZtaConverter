import os
import subprocess
from tkinter import filedialog, StringVar, messagebox, Tk, Label, Button, OptionMenu
import customtkinter as ctk
import threading

class FileConverterApp:
    def __init__(self, root):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Zta Converter")
        self.root.geometry("900x600")  # Ampliado para incluir información lateral
        self.root.resizable(False, False)

        # Variables de selección
        self.input_format = StringVar(value="mkv")
        self.output_format = StringVar(value="mp4")
        self.fps = StringVar(value="30")
        self.quality = StringVar(value="Media")
        self.resolution = StringVar(value="1920x1080")
        self.input_file = None

        # Frame principal
        self.frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.frame.pack(padx=20, pady=20, fill="both", expand=True, side="left")

        # Etiquetas y menús
        ctk.CTkLabel(self.frame, text="Formato de entrada:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.input_menu = ctk.CTkOptionMenu(self.frame, variable=self.input_format, values=["mp4", "avi", "mov", "mkv", "mp3", "wav", "aac", "flv", "wmv", "webm"])
        self.input_menu.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        ctk.CTkLabel(self.frame, text="Formato de salida:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.output_menu = ctk.CTkOptionMenu(self.frame, variable=self.output_format, values=["mp4", "avi", "mov", "mkv", "mp3","wav", "aac", "flv", "wmv", "webm"])
        self.output_menu.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        ctk.CTkLabel(self.frame, text="FPS (Cuadros por Segundo):", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.fps_menu = ctk.CTkOptionMenu(self.frame, variable=self.fps, values=["30", "60", "120"], command=self.fps_warning)
        self.fps_menu.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        ctk.CTkLabel(self.frame, text="Calidad de conversión:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.quality_menu = ctk.CTkOptionMenu(self.frame, variable=self.quality, values=["Baja", "Media", "Alta"])
        self.quality_menu.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        ctk.CTkLabel(self.frame, text="Resolución de salida:", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.resolution_menu = ctk.CTkOptionMenu(self.frame, variable=self.resolution, values=["1920x1080", "1280x720", "854x480"])
        self.resolution_menu.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        # Botón para seleccionar archivo
        self.select_file_button = ctk.CTkButton(self.frame, text="Seleccionar archivo", command=self.select_file)
        self.select_file_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Botón para iniciar la conversión
        self.convert_button = ctk.CTkButton(self.frame, text="Convertir", command=self.start_conversion, state="disabled")
        self.convert_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Barra de progreso
        self.progress = ctk.CTkProgressBar(self.frame, width=300)
        self.progress.set(0)
        self.progress.grid(row=8, column=0, columnspan=2, pady=20)

        self.status_label = ctk.CTkLabel(self.frame, text="Estado: Esperando selección de archivo", font=("Arial", 12))
        self.status_label.grid(row=9, column=0, columnspan=2, pady=10)
        
        self.file_size_label = ctk.CTkLabel(self.frame, text="Tamaño del archivo seleccionado: N/A", font=("Arial", 12))
        self.file_size_label.grid(row=10, column=0, columnspan=2, pady=5)

        self.estimated_size_label = ctk.CTkLabel(self.frame, text="Tamaño estimado del archivo convertido: N/A", font=("Arial", 12))
        self.estimated_size_label.grid(row=11, column=0, columnspan=2, pady=5)

        # Información del desarrollador
        self.info_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.info_frame.pack(padx=20, pady=20, fill="both", expand=True, side="right")

        ctk.CTkLabel(self.info_frame, text="📌 Zta Converter", font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(self.info_frame, text="Desarrollado por: ztadev", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(self.info_frame, text="Este programa permite convertir archivos de video entre diferentes formatos "
                                           "utilizando FFmpeg. Puedes ajustar la calidad, resolución y FPS para "
                                           "optimizar la conversión según tus necesidades.",
                     wraplength=250, font=("Arial", 12), text_color="gray").pack(pady=10)
        ctk.CTkLabel(self.info_frame, text="⚙️ Características:", font=("Arial", 14, "bold")).pack(pady=5)
        ctk.CTkLabel(self.info_frame, text="✔ Conversión entre MKV, MP4, AVI, MOV\n"
                                           "✔ Ajuste de FPS y resolución\n"
                                           "✔ Estimación del tamaño de salida\n"
                                           "✔ Progreso de conversión en tiempo real", wraplength=250,
                     font=("Arial", 12), text_color="gray").pack(pady=10)
    
    def fps_warning(self, fps_value):
        if int(fps_value) > 30:
            messagebox.showwarning("Advertencia", "Seleccionar FPS mayores que los originales puede causar inestabilidad.")

    def select_file(self):
        filetypes = [(f"Archivos {self.input_format.get().upper()}", f"*.{self.input_format.get()}")]
        self.input_file = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=filetypes)
        if self.input_file:
            self.status_label.configure(text=f"Archivo seleccionado: {os.path.basename(self.input_file)}")
            self.convert_button.configure(state="normal")
        else:
            self.status_label.configure(text="Estado: No se seleccionó ningún archivo")
    def estimate_output_size(self, input_file):
        """Estima el tamaño del archivo convertido usando FFmpeg."""
        try:
            command = ["ffmpeg", "-i", input_file, "-f", "null", "-"]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
            size_line = [line for line in result.stderr.split("\n") if "bitrate:" in line]
            if size_line:
                bitrate_str = size_line[0].split("bitrate:")[1].strip().split(" ")[0]
                bitrate_kbps = float(bitrate_str)  # En kbps
                duration_line = [line for line in result.stderr.split("\n") if "Duration" in line]
                duration_str = duration_line[0].split(",")[0].split("Duration:")[1].strip()
                hours, minutes, seconds = map(float, duration_str.split(":"))
                total_seconds = hours * 3600 + minutes * 60 + seconds
                estimated_size_mb = (bitrate_kbps * total_seconds) / (8 * 1024)
                return estimated_size_mb
        except Exception as e:
            print(f"Error al estimar el tamaño: {e}")
        return None

    def start_conversion(self):
        threading.Thread(target=self.convert_file).start()

    def convert_file(self):
        if not self.input_file:
            self.status_label.configure(text="Error: No se seleccionó ningún archivo.")
            return
        videos_folder = os.path.expanduser("~\\Videos")  # Obtiene la carpeta Videos del usuario
        convert_folder = os.path.join(videos_folder, "ZtaConverter")  # Carpeta 'convert' dentro de 'Videos'
        output_file = os.path.join(convert_folder, os.path.basename(self.input_file).replace(os.path.splitext(self.input_file)[1], f".{self.output_format.get()}"))
        if not os.path.exists(convert_folder):
            os.makedirs(convert_folder)

        self.status_label.configure(text="Iniciando conversión...")
        self.progress.set(0)
        self.root.update_idletasks()
        
        estimated_size = self.estimate_output_size(self.input_file)
        if estimated_size:
            self.estimated_size_label.configure(text=f"Tamaño estimado del archivo convertido: {estimated_size:.2f} MB")
        try:
            # Obtener la duración del archivo
            command_duration = [
                "ffmpeg",
                "-i", self.input_file,
                "-hide_banner",
                "-f", "null",
                "-"
            ]
            result = subprocess.run(command_duration, stderr=subprocess.PIPE, text=True)
            duration_line = [line for line in result.stderr.split("\n") if "Duration" in line]
            if not duration_line:
                raise ValueError("No se pudo obtener la duración del archivo.")
            duration_str = duration_line[0].split(",")[0].split("Duration:")[1].strip()
            hours, minutes, seconds = map(float, duration_str.split(":"))
            total_seconds = int(hours * 3600 + minutes * 60 + seconds)

            # Comando de conversión
            quality_map = {"Baja": "23", "Media": "20", "Alta": "18"}
            fps_value = self.fps.get()
            crf_value = quality_map[self.quality.get()]

            command_convert = [
                "ffmpeg",
                "-i", self.input_file,
                "-crf", crf_value,
                "-r", fps_value,
                "-s", self.resolution.get(),
                output_file
            ]
            process = subprocess.Popen(command_convert, stderr=subprocess.PIPE, text=True)
            for line in process.stderr:
                if "time=" in line:
                    time_str = line.split("time=")[1].split(" ")[0]
                    h, m, s = map(float, time_str.split(":"))
                    current_time = int(h * 3600 + m * 60 + s)
                    progress = (current_time / total_seconds)
                    self.progress.set(progress)
                    self.root.update_idletasks()
            process.wait()

            self.progress.set(1)
            self.status_label.configure(text=f"Conversión completada: {output_file}")
            messagebox.showinfo("Éxito", f"Archivo convertido correctamente: {output_file}")
        except Exception as e:
            self.status_label.configure(text=f"Error: {e}")
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
        
        

if __name__ == "__main__":
    root = ctk.CTk()
    app = FileConverterApp(root)
    root.mainloop()
