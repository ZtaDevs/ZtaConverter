import os, sys
import customtkinter as ctk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import time

class ImageEffectsEditor:
    def __init__(self, root, theme_appearance, color_theme):
        ctk.set_appearance_mode(theme_appearance)  # 'Dark', 'Light', 'System'
        ctk.set_default_color_theme(color_theme)

        self.root = root
        self.root.title("Zta Effects")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # Panel lateral izquierdo
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(self.sidebar, text="Zta Image Effects", font=("Arial", 18, "bold")).pack(pady=20)

        self.load_button = ctk.CTkButton(self.sidebar, text="Cargar Imagen", command=self.load_image)
        self.load_button.pack(pady=10, fill="x", padx=10)

        self.save_button = ctk.CTkButton(self.sidebar, text="Guardar Imagen", command=self.save_image)
        self.save_button.pack(pady=20, fill="x", padx=10)

        # Sliders para efectos
        ctk.CTkLabel(self.sidebar, text="Ajustes de Efectos:", font=("Arial", 14, "bold")).pack(pady=10)
        self.brightness_scale = self.create_slider("Brillo", self.adjust_brightness)
        self.contrast_scale = self.create_slider("Contraste", self.adjust_contrast)
        self.saturation_scale = self.create_slider("Saturación", self.adjust_saturation)
        self.sharpness_scale = self.create_slider("Nitidez", self.adjust_sharpness)

        # Panel lateral derecho para switches
        self.filter_panel = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.filter_panel.pack(side="right", fill="y")

        ctk.CTkLabel(self.filter_panel, text="Filtros", font=("Arial", 14, "bold")).pack(pady=20)

        self.sepia_switch = self.create_switch("Sepia", self.toggle_sepia, self.filter_panel)
        self.grayscale_switch = self.create_switch("Escala de Grises", self.toggle_grayscale, self.filter_panel)
        self.invert_switch = self.create_switch("Invertir Colores", self.toggle_invert, self.filter_panel)
        self.posterize_switch = self.create_switch("Posterizar", self.toggle_posterize, self.filter_panel)
        self.emboss_switch = self.create_switch("Emboss", self.toggle_emboss, self.filter_panel)
        self.flip_switch = self.create_switch("Voltear", self.toggle_flip, self.filter_panel)
        self.colorize_switch = self.create_switch("Colorizar", self.toggle_colorize, self.filter_panel)

        # Filtro de eliminar fondo y Dropdown para seleccionar color
        self.remove_bg_switch = self.create_switch("Eliminar Fondo", self.toggle_remove_bg, self.filter_panel)

        # Cuadro de propiedades de la imagen (ubicado en la parte inferior derecha)
        self.properties_label = ctk.CTkLabel(self.filter_panel, text="    Propiedades de la Imagen:     ", font=("Arial", 12, "bold"))
        self.properties_label.pack(pady=10)

        self.properties_text = ctk.CTkLabel(self.filter_panel, text="", font=("Arial", 12))
        self.properties_text.pack(pady=5)

        # Espacio para mostrar la imagen
        self.image_panel = ctk.CTkLabel(self.root, text="Carga una imagen para comenzar", font=("Arial", 14))
        self.image_panel.pack(side="top", expand=True, fill="both", padx=10, pady=10)

        self.image = None
        self.filepath = None
        self.original_image = None  # Guarda la imagen original para restaurar estados
        self.bg_color = (255, 255, 255)  # Color por defecto (blanco)

    def set_remove_color(self, selected_color):
        """Actualiza el color que se eliminará del fondo."""
        colors = {
            "Blanco": (255, 255, 255),
            "Negro": (0, 0, 0),
            "Rojo": (255, 0, 0),
            "Verde": (0, 255, 0),
            "Azul": (0, 0, 255),
        }
        self.bg_color = colors.get(selected_color, (255, 255, 255))  # Por defecto blanco
    def detect_white_background(self, img):
        """Detecta si el fondo de la imagen es blanco predominante."""
        img = img.convert("RGBA")
        data = img.getdata()

        # Contar la cantidad de píxeles que coinciden con el color blanco
        white_pixel_count = sum(1 for item in data if item[:3] == (255, 255, 255))
        total_pixels = len(data)

        # Si más del 80% de los píxeles son blancos, consideramos que el fondo es blanco
        if white_pixel_count / total_pixels > 0.8:
            return True
        return False


    def create_slider(self, label, command):
        """Crea un slider con una etiqueta."""
        ctk.CTkLabel(self.sidebar, text=label, font=("Arial", 12)).pack(pady=5)
        slider = ctk.CTkSlider(self.sidebar, from_=0.5, to=2.0, command=command)
        slider.pack(pady=5, fill="x", padx=10)
        slider.set(1.0)
        return slider

    def create_switch(self, label, command, parent):
        """Crea un switch con una etiqueta."""
        switch = ctk.CTkSwitch(parent, text=label, command=command)
        switch.pack(pady=10, fill="x", padx=10)
        return switch

    def load_image(self):
        """Carga una imagen y la muestra en la interfaz."""
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.filepath = file_path
            self.image = Image.open(file_path).convert("RGBA")
            self.original_image = self.image.copy()  # Copia de la imagen original

            # Detectamos si el fondo es blanco
            if self.detect_white_background(self.image):
                self.remove_bg_switch.select()  # Activamos el switch de eliminar fondo automáticamente
                self.image = self.remove_background(self.image)  # Eliminar el fondo blanco
                messagebox.showinfo("Fondo Blanco Detectado", "Se detectó un fondo blanco y se eliminó automáticamente.")
            
            self.display_image(self.image)

            # Mostrar propiedades de la imagen
            self.update_image_properties(file_path)


    def display_image(self, img):
        """Muestra la imagen en la interfaz."""
        img.thumbnail((400, 400))
        img = ctk.CTkImage(light_image=img, size=img.size)
        self.image_panel.configure(image=img, text="")
        self.image_panel.image = img

    def update_image_properties(self, file_path):
        """Actualiza el cuadro de propiedades de la imagen."""
        try:
            file_size = os.path.getsize(file_path) / 1024  # Tamaño en KB
            file_size = round(file_size, 2)
            file_format = self.image.format
            creation_time = time.ctime(os.path.getctime(file_path))

            properties_text = f"Tamaño: {file_size} KB\nFormato: {file_format}\nFecha de Creación: {creation_time}"
            self.properties_text.configure(text=properties_text)
        except Exception as e:
            self.properties_text.configure(text=f"Error al obtener propiedades: {e}")

    def reset_filters(self):
        """Restaura la imagen original y aplica los filtros activos."""
        if self.original_image:
            self.image = self.original_image.copy()
            if self.sepia_switch.get():
                self.image = self.apply_sepia_filter(self.image)
            if self.grayscale_switch.get():
                self.image = self.apply_grayscale_filter(self.image)
            if self.invert_switch.get():
                self.image = self.apply_invert_filter(self.image)
            if self.posterize_switch.get():
                self.image = self.apply_posterize_filter(self.image)
            if self.emboss_switch.get():
                self.image = self.apply_emboss_filter(self.image)
            if self.flip_switch.get():
                self.image = self.apply_flip_filter(self.image)
            if self.colorize_switch.get():
                self.image = self.apply_colorize_filter(self.image)
            self.display_image(self.image)

    def toggle_sepia(self):
        """Activa o desactiva el filtro sepia."""
        self.reset_filters()

    def toggle_grayscale(self):
        """Activa o desactiva el filtro de escala de grises."""
        self.reset_filters()

    def toggle_invert(self):
        """Activa o desactiva el filtro de inversión de colores."""
        self.reset_filters()

    def toggle_posterize(self):
        """Activa o desactiva el filtro de posterización."""
        self.reset_filters()

    def toggle_emboss(self):
        """Activa o desactiva el filtro de embosse."""
        self.reset_filters()

    def toggle_flip(self):
        """Activa o desactiva el filtro de volteo."""
        self.reset_filters()

    def toggle_colorize(self):
        """Activa o desactiva el filtro de colorización."""
        self.reset_filters()

    def toggle_remove_bg(self):
        """Activa o desactiva el filtro de eliminación del fondo."""
        if self.image is None:
            # Si no se ha cargado ninguna imagen, mostramos un mensaje de advertencia
            messagebox.showwarning("Error", "Por favor, cargue una imagen primero.")
            self.remove_bg_switch.deselect()  # Desmarcamos el switch si no hay imagen cargada
            return

        if self.remove_bg_switch.get():
            # Mostramos el popup de selección de color para elegir el fondo a eliminar
            self.show_color_popup()
        else:
            self.image = self.original_image.copy() if self.original_image else self.image  # Restauramos la imagen original
            self.display_image(self.image)

    def show_color_popup(self):
        """Muestra un popup para seleccionar el color a eliminar."""
        # Creamos una nueva ventana emergente
        popup = ctk.CTkToplevel(self.root)
        popup.title("Selecciona el color a eliminar")

        # Obtener el tamaño de la ventana principal
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Obtener el tamaño de la ventana emergente
        popup_width = 300
        popup_height = 200

        # Calcular las coordenadas para centrar el popup
        x = self.root.winfo_x() + (window_width // 2) - (popup_width // 2)
        y = self.root.winfo_y() + (window_height // 2) - (popup_height // 2)

        # Establecer la geometría de la ventana emergente
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        
        popup.grab_set()  # Hace que el popup esté en primer plano

        # Agregamos una etiqueta para informar al usuario
        label = ctk.CTkLabel(popup, text="Selecciona el color de fondo a eliminar:", font=("Arial", 12))
        label.pack(pady=10)

        # Dropdown para seleccionar el color
        color_dropdown = ctk.CTkOptionMenu(popup, values=["Blanco", "Negro", "Rojo", "Verde", "Azul"], command=self.set_remove_color)
        color_dropdown.set("Blanco")  # Valor por defecto
        color_dropdown.pack(pady=10)

        # Botón Aceptar para aplicar el color seleccionado y eliminar el fondo
        accept_button = ctk.CTkButton(popup, text="Aceptar", command=lambda: self.apply_remove_bg_and_close(popup))
        accept_button.pack(pady=10)

        # Botón Cancelar para cerrar el popup sin aplicar cambios
        cancel_button = ctk.CTkButton(popup, text="Cancelar", command=popup.destroy)
        cancel_button.pack(pady=5)


    def apply_remove_bg_and_close(self, popup):
        """Aplica la eliminación de fondo y cierra el popup."""
        # Eliminar el fondo con el color seleccionado
        self.image = self.remove_background(self.image)
        self.display_image(self.image)
        popup.destroy()  # Cerrar el popup después de aplicar el filtro



    def remove_background(self, img):
        """Elimina el color seleccionado del fondo y lo convierte en transparente."""
        img = img.convert("RGBA")  # Aseguramos que la imagen tiene un canal alfa
        data = img.getdata()

        new_data = []
        for item in data:
            # Compara el color de fondo seleccionado con el color de cada píxel
            if all(abs(val - bg_val) < 100 for val, bg_val in zip(item[:3], self.bg_color)):  # Tolerancia ajustada
                new_data.append((255, 255, 255, 0))  # Fondo transparente
            else:
                new_data.append(item)  # Mantener el píxel original

        img.putdata(new_data)
        return img

    def adjust_brightness(self, value):
        """Ajusta el brillo de la imagen."""
        if self.image:
            enhancer = ImageEnhance.Brightness(self.image)
            enhanced_image = enhancer.enhance(float(value))
            self.display_image(enhanced_image)

    def adjust_contrast(self, value):
        """Ajusta el contraste de la imagen."""
        if self.image:
            enhancer = ImageEnhance.Contrast(self.image)
            enhanced_image = enhancer.enhance(float(value))
            self.display_image(enhanced_image)

    def adjust_saturation(self, value):
        """Ajusta la saturación de la imagen."""
        if self.image:
            enhancer = ImageEnhance.Color(self.image)
            enhanced_image = enhancer.enhance(float(value))
            self.display_image(enhanced_image)

    def adjust_sharpness(self, value):
        """Ajusta la nitidez de la imagen."""
        if self.image:
            enhancer = ImageEnhance.Sharpness(self.image)
            enhanced_image = enhancer.enhance(float(value))
            self.display_image(enhanced_image)

    def save_image(self):
        """Guarda la imagen editada."""
        if self.image:
            # Verificamos si el fondo ha sido removido y solo permitimos guardarlo en formatos con transparencia
            if self.remove_bg_switch.get():
                save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("PNG", "*.png")])  # Solo PNG para transparencia
            else:
                save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                         filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp")])
            
            if save_path:
                self.image.save(save_path)

    def apply_sepia_filter(self, img):
        """Aplica el filtro sepia a la imagen."""
        return ImageOps.colorize(img.convert("L"), "#704214", "#C9C6A1")

    def apply_grayscale_filter(self, img):
        """Aplica el filtro de escala de grises."""
        return img.convert("L").convert("RGBA")

    def apply_invert_filter(self, img):
        """Aplica el filtro de inversión de colores."""
        return ImageOps.invert(img.convert("RGB"))

    def apply_posterize_filter(self, img):
        """Aplica el filtro de posterización."""
        return img.convert("P", palette=Image.ADAPTIVE, colors=8)

    def apply_emboss_filter(self, img):
        """Aplica el filtro de embosse."""
        return img.filter(ImageFilter.EMBOSS)

    def apply_flip_filter(self, img):
        """Aplica el filtro de volteo."""
        return img.transpose(Image.FLIP_LEFT_RIGHT)

    def apply_colorize_filter(self, img):
        """Aplica el filtro de colorización."""
        return ImageOps.colorize(img.convert("L"), "#0000FF", "#00FF00")


if __name__ == "__main__":
    theme_appearance = sys.argv[1] if len(sys.argv) > 1 else "System"  # Default: 'System'
    color_theme = sys.argv[2] if len(sys.argv) > 2 else "blue"  # Default: 'blue'
    root = ctk.CTk()
    app = ImageEffectsEditor(root, theme_appearance, color_theme)
    root.mainloop()
