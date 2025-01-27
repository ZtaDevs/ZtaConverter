import customtkinter as ctk

# Configuración del tema
class ThemeConfig:
    APPEARANCE_MODE = "System"  # Opciones: "System", "Light", "Dark"
    COLOR_THEME = "blue"  # Opciones: "blue", "green", "dark-blue"

    def apply_theme():
        """Aplica la configuración del tema global."""
        ctk.set_appearance_mode(ThemeConfig.APPEARANCE_MODE)
        ctk.set_default_color_theme(ThemeConfig.COLOR_THEME)
