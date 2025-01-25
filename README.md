# Zta Converter - Conversor de Archivos de Video

**Zta Converter** es una herramienta de conversión de archivos de video de código abierto que permite convertir fácilmente archivos entre diferentes formatos, ajustar la resolución, el FPS y la calidad de los videos utilizando **FFmpeg**. El programa tiene una interfaz gráfica intuitiva creada con **CustomTkinter** que facilita su uso incluso para usuarios sin experiencia técnica.

## Características:
- Conversión entre múltiples formatos de video como MP4, AVI, MOV, MKV, y más.
- Ajuste de la resolución de salida (por ejemplo, 1920x1080, 1280x720, 854x480).
- Configuración de FPS (Frames por segundo) para ajustar la fluidez del video.
- Opciones de calidad de conversión (Baja, Media, Alta).
- Progreso de conversión en tiempo real.
- Estimación del tamaño de archivo de salida.
- Instalación automática de dependencias necesarias como **FFmpeg** y **7zip**.

## Requisitos:
- Python 3.x
- **FFmpeg** (se instala automáticamente durante la instalación del programa).
- **7zip** (se instala automáticamente si no está presente).

## Instalación:
1. Descarga el instalador desde el [repositorio de releases](#).
2. Ejecuta el instalador y sigue los pasos de instalación.
3. El instalador configurará **FFmpeg** y **7zip** automáticamente si no los tienes instalados.
4. El programa creará un acceso directo en el escritorio para iniciar el conversor de video.

## Cómo usar:
1. Abre el programa.
2. Selecciona el archivo de entrada.
3. Elige el formato de salida, FPS, calidad y resolución.
4. Haz clic en "Convertir" y espera mientras se procesa el archivo.
5. El progreso de la conversión se muestra en tiempo real.

## Tecnologías usadas:
- **Python 3.x** para la programación del conversor.
- **CustomTkinter** para la interfaz gráfica.
- **FFmpeg** para la conversión de videos.
- **7zip** para la extracción de archivos comprimidos.

## Contribuciones:
Las contribuciones son bienvenidas. Si encuentras algún error o tienes una sugerencia para mejorar el programa, no dudes en abrir un **issue** o enviar un **pull request**.
