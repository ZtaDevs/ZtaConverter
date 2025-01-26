import os
import subprocess
import customtkinter as ctk

class ZtaConverter:
    def __init__(self, root):
        ctk.set_appearance_mode("System")  # Modo oscuro/claro automático
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("ZtaConverter")
        self.root.geometry("700x400")
        self.root.resizable(False, False)

        # Crear un frame de navegación lateral
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.title_label = ctk.CTkLabel(self.sidebar, text="Seleccion: ", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=20)

        # Botones del menú
        self.image_button = ctk.CTkButton(self.sidebar, text="Convertir Imágenes",
                                          command=self.run_image_converter, height=40)
        self.image_button.pack(pady=10, fill="x", padx=10)

        self.media_button = ctk.CTkButton(self.sidebar, text="Convertir Videos/Audio",
                                          command=self.run_media_converter, height=40)
        self.media_button.pack(pady=10, fill="x", padx=10)

        self.exit_button = ctk.CTkButton(self.sidebar, text="Salir",
                                         command=self.root.quit, height=40)
        self.exit_button.pack(pady=20, fill="x", padx=10)

        # Panel de información
        self.info_frame = ctk.CTkFrame(self.root)
        self.info_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.info_frame, text="📌 Zta Converter", font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(self.info_frame, text="Desarrollado por: ztadev", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(self.info_frame, text="Este programa permite convertir archivos de imagen, video y audio "
                                           "utilizando FFmpeg. Puedes ajustar la calidad, resolución y FPS para "
                                           "optimizar la conversión según tus necesidades.",
                     wraplength=400, font=("Arial", 12), text_color="gray").pack(pady=10)
        ctk.CTkLabel(self.info_frame, text="⚙️ Características:", font=("Arial", 14, "bold")).pack(pady=5)
        ctk.CTkLabel(self.info_frame, text="✔ Conversión entre múltiples formatos\n"
                                           "✔ Ajuste de calidad, FPS y resolución\n"
                                           "✔ Estimación del tamaño de salida\n"
                                           "✔ Progreso de conversión en tiempo real",
                     wraplength=400).pack(pady=5)

    def run_image_converter(self):
        """ Ejecuta el Convertidor de Imágenes. """
        image_converter_path = os.path.join(os.getcwd(), "image_converter", "image_converter.py")
        subprocess.Popen(["python", image_converter_path], creationflags=subprocess.CREATE_NO_WINDOW)

    def run_media_converter(self):
        """ Ejecuta el Convertidor de Video y Audio. """
        media_converter_path = os.path.join(os.getcwd(), "media_converter", "media_converter.py")
        subprocess.Popen(["python", media_converter_path], creationflags=subprocess.CREATE_NO_WINDOW)



if __name__ == "__main__":
    root = ctk.CTk()
    app = ZtaConverter(root)
    root.mainloop()
