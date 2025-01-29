import os
import subprocess
import customtkinter as ctk

class ZtaConverter:
    def __init__(self, root):
        self.theme_appearance = "Dark"  
        self.color_theme = "blue"  

        ctk.set_appearance_mode(self.theme_appearance)
        ctk.set_default_color_theme(self.color_theme)

        self.root = root
        self.root.title("ZtaConverter")
        self.root.geometry("700x400")
        self.root.resizable(False, False)

        # Centrar ventana
        self.center_window(self.root, 700, 400)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.title_label = ctk.CTkLabel(self.sidebar, text="Seleccion: ", font=("Arial", 18, "bold"))
        self.title_label.pack(pady=20)

        # Botones
        self.image_button = ctk.CTkButton(self.sidebar, text="Abrir Image Converter",
                                          command=self.run_image_converter, height=40)
        self.image_button.pack(pady=10, fill="x", padx=10)

        self.media_button = ctk.CTkButton(self.sidebar, text="Abrir Video Converter",
                                          command=self.run_media_converter, height=40)
        self.media_button.pack(pady=10, fill="x", padx=10)

        self.editor_button = ctk.CTkButton(self.sidebar, text="Abrir Image Editor",
                                           command=self.run_image_editor, height=40)
        self.editor_button.pack(pady=10, fill="x", padx=10)

        self.config_button = ctk.CTkButton(self.sidebar, text="Configuración", command=self.open_settings, height=40)
        self.config_button.pack(pady=10, fill="x", padx=10)

        self.exit_button = ctk.CTkButton(self.sidebar, text="Salir",
                                         command=self.root.quit, height=40)
        self.exit_button.pack(pady=20, fill="x", padx=10)

        # Guardar los botones en una lista para refrescarlos después
        self.buttons = [self.image_button, self.media_button, self.editor_button, self.config_button, self.exit_button]

        # Info
        self.info_frame = ctk.CTkFrame(self.root)
        self.info_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.info_frame, text="📌 Zta Converter", font=("Arial", 18, "bold")).pack(pady=10)
        ctk.CTkLabel(self.info_frame, text="Desarrollado por: ztadev", font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(self.info_frame, text="Este programa permite convertir archivos de imagen, video y audio "
                                           "utilizando FFmpeg.", wraplength=400, font=("Arial", 12),
                     text_color="gray").pack(pady=10)

    def open_settings(self):
        """ Abrir ventana de configuración """
        self.settings_window = ctk.CTkToplevel(self.root)
        self.settings_window.title("Configuración")
        self.settings_window.geometry("400x300")

        # Centrar ventana
        self.center_window(self.settings_window, 400, 300)

        self.settings_window.attributes("-topmost", True)

        self.theme_switch = ctk.CTkSwitch(self.settings_window, text="Modo Oscuro/Claro",
                                          command=self.toggle_theme)
        self.theme_switch.pack(pady=20)
        self.theme_switch.select() if self.theme_appearance == "Dark" else self.theme_switch.deselect()

        self.color_options = ["blue", "green", "dark-blue"]
        self.color_dropdown = ctk.CTkOptionMenu(self.settings_window, values=self.color_options,
                                                command=self.set_color_theme)
        self.color_dropdown.set(self.color_theme)  
        self.color_dropdown.pack(pady=20)

        self.accept_button = ctk.CTkButton(self.settings_window, text="Aceptar", command=self.apply_settings)
        self.accept_button.pack(pady=20)

    def center_window(self, window, width, height):
        """ Centrar la ventana """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)

        window.geometry(f'{width}x{height}+{position_right}+{position_top}')

    def toggle_theme(self):
        """ Cambiar el modo de apariencia """
        self.theme_appearance = "Dark" if self.theme_switch.get() else "Light"

    def set_color_theme(self, selected_color):
        """ Cambiar el color del tema """
        self.color_theme = selected_color

    def apply_settings(self):
        """ Aplicar cambios y refrescar botones """
        ctk.set_appearance_mode(self.theme_appearance)
        ctk.set_default_color_theme(self.color_theme)

        self.refresh_buttons()

        self.settings_window.destroy()

    def refresh_buttons(self):
        """ Actualizar los colores de los botones manualmente """
        for btn in self.buttons:
            btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

    def run_image_converter(self):
        """ Ejecuta el Convertidor de Imágenes. """
        subprocess.Popen(["python", os.path.join(os.getcwd(), "image_converter", "image_converter.py"),
                          self.theme_appearance, self.color_theme], creationflags=subprocess.CREATE_NO_WINDOW)

    def run_media_converter(self):
        """ Ejecuta el Convertidor de Video y Audio. """
        subprocess.Popen(["python", os.path.join(os.getcwd(), "media_converter", "media_converter.py"),
                          self.theme_appearance, self.color_theme], creationflags=subprocess.CREATE_NO_WINDOW)

    def run_image_editor(self):
        """ Ejecuta el Editor de Imágenes. """
        subprocess.Popen(["python", os.path.join(os.getcwd(), "image_editor", "image_editor.py"),
                          self.theme_appearance, self.color_theme], creationflags=subprocess.CREATE_NO_WINDOW)

if __name__ == "__main__":
    root = ctk.CTk()
    app = ZtaConverter(root)
    root.mainloop()
