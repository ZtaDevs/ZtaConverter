echo off
:: File: prerequisites.bat
:: Verifica si Python está instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python no está instalado. Descargando e instalando Python...
    call :install_python
) ELSE (
    echo Python ya está instalado.
)

:: Verifica si pip está instalado
python -m ensurepip --upgrade >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo pip no está instalado. Instalando pip...
    python -m ensurepip --upgrade
) ELSE (
    echo pip ya está instalado.
)

:: Instalar las dependencias necesarias
echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install requests customtkinter pillow

:: Verificar si 7-Zip está instalado y disponible en el PATH
7z >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo 7-Zip no está instalado o no está en el PATH. Descargando e instalando 7-Zip...
    call :install_7zip
) ELSE (
    echo 7-Zip ya está instalado.
)

:: Verificar si FFmpeg está instalado
ffmpeg -version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo FFmpeg no está instalado. Descargando FFmpeg...
    call :download_ffmpeg
) ELSE (
    echo FFmpeg ya está instalado.
)

:: Finalización
echo Todo listo. Puedes ejecutar tu aplicación ahora.
exit /b

:install_python
:: Descargar e instalar Python si no está instalado
set PYTHON_URL=https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe
set PYTHON_INSTALL_PATH=%~dp0python_installer.exe

:: Descargar el instalador de Python
echo Descargando Python...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%PYTHON_URL%', '%PYTHON_INSTALL_PATH%')"

:: Instalar Python de forma silenciosa (incluye pip)
echo Instalando Python...
start /wait %PYTHON_INSTALL_PATH% /quiet InstallAllUsers=1 PrependPath=1

:: Eliminar el instalador de Python después de la instalación
del "%PYTHON_INSTALL_PATH%"

echo Python y pip instalados correctamente.

exit /b

:install_7zip
:: Descargar e instalar 7-Zip si no está instalado
set ZIP_URL=https://www.7-zip.org/a/7z1900-x64.exe
set ZIP_INSTALL_PATH=%~dp07z_installer.exe

:: Descargar el instalador de 7-Zip
echo Descargando 7-Zip...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%ZIP_URL%', '%ZIP_INSTALL_PATH%')"

:: Instalar 7-Zip de forma silenciosa
echo Instalando 7-Zip...
start /wait %ZIP_INSTALL_PATH% /S

:: Agregar 7-Zip al PATH
echo Agregando 7-Zip al PATH...
setx PATH "%PATH%;C:\Program Files\7-Zip"

:: Eliminar el instalador de 7-Zip después de la instalación
del "%ZIP_INSTALL_PATH%"

echo 7-Zip instalado y agregado al PATH correctamente.

exit /b

:download_ffmpeg
:: Descargar y extraer FFmpeg si no está instalado
set FFmpeg_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z
set DOWNLOAD_DIR=%~dp0ffmpeg

:: Crear carpeta para FFmpeg si no existe
if not exist "%DOWNLOAD_DIR%" mkdir "%DOWNLOAD_DIR%"

:: Descargar FFmpeg
echo Descargando FFmpeg...
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('%FFmpeg_URL%', '%DOWNLOAD_DIR%\\ffmpeg-git-essentials.7z')"

:: Extraer FFmpeg utilizando 7-Zip
echo Extrayendo FFmpeg...
"%ProgramFiles%\7-Zip\7z.exe" x "%DOWNLOAD_DIR%\\ffmpeg-git-essentials.7z" -o"%DOWNLOAD_DIR%"

:: Limpiar archivo comprimido
del "%DOWNLOAD_DIR%\\ffmpeg-git-essentials.7z"

:: Agregar FFmpeg al PATH
echo Agregando FFmpeg al PATH...
setx PATH "%PATH%;%DOWNLOAD_DIR%\ffmpeg-git-essentials\bin"

:: Confirmar instalación
echo FFmpeg instalado correctamente y agregado al PATH.

exit
