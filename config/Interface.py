import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from IPython import get_ipython
import os
import urllib.request

def launch_interface():

    # --- Nueva función para clonar los scripts ---
    def clonar_scripts():
        """
        Descarga los scripts Install.py, Uninstall.py y Updater.py
        desde GitHub y los guarda en ~/.swar/Install/
        """
        # Rutas
        base_dir = os.path.expanduser("~/.swar")
        install_dir = os.path.join(base_dir, "Install")
        os.makedirs(install_dir, exist_ok=True)

        # URLs de los archivos raw en GitHub
        urls = {
            "Install.py": "https://raw.githubusercontent.com/SFcrypt/segsmaker-x/main/config/Install/Install.py",
            "Uninstall.py": "https://raw.githubusercontent.com/SFcrypt/segsmaker-x/main/config/Install/Uninstall.py",
            "Updater.py": "https://raw.githubusercontent.com/SFcrypt/segsmaker-x/main/config/Install/Updater.py"
        }

        print("Clonando scripts necesarios...")
        for nombre, url in urls.items():
            ruta_destino = os.path.join(install_dir, nombre)
            try:
                urllib.request.urlretrieve(url, ruta_destino)
                print(f"  - {nombre} descargado correctamente.")
            except Exception as e:
                print(f"  - Error al descargar {nombre}: {e}")
        print("---")
    # --- Fin de la nueva función ---

    process_out = widgets.Output()
    css_url = "https://raw.githubusercontent.com/gutris1/segsmaker/refs/heads/main/script/SM/setup.css"
    display(HTML(f'<link rel="stylesheet" type="text/css" href="{css_url}">'))

    instalar_img    = "https://raw.githubusercontent.com/SFcrypt/Segsmaker/main/cover/003219.png"
    desinstalar_img = "https://raw.githubusercontent.com/SFcrypt/Segsmaker/main/cover/092918.png"

    # ... (el estilo HTML se mantiene exactamente igual) ...
    display(HTML(f"""
    <style>
    .setup-box {{
        padding: 10px;
        border-radius: 16px;
        background: #000000;
        overflow: hidden;}}

    .custom-btn {{
        width: 100%;
        height: 100%;
        border: 2px solid #111 !important;
        border-radius: 14px;
        background-size: cover;
        background-position: center;
        color: white !important;
        font-size: 18px;
        font-weight: 700;
        text-transform: lowercase;
        text-shadow: 0 2px 6px rgba(0,0,0,.95);
        padding-top: 10px;
        align-items: flex-start;
        justify-content: center;
        box-shadow: inset 0 0 0 1px #222;
        transition: all .15s ease-in-out;
        overflow: hidden;}}

    .custom-btn:hover {{
        border-color: #00aaff !important;
        box-shadow: 0 0 0 2px #00aaff;
        transform: translateY(-2px);}}

    .instalar {{
        background-image: url('{instalar_img}');}}

    .desinstalar {{
        background-image: url('{desinstalar_img}');}}

    .widget-button {{
        min-width: 0 !important;}}

    .widget-box, .output_wrapper, .output {{
        overflow: hidden !important;
        max-height: none !important;}}
    </style>
    """))

    # --- Funciones actualizadas para ejecutar los scripts clonados ---
    def run_instalar(_):
        # Ocultar el panel y ejecutar Install.py desde la nueva ruta
        panel.layout.display = "none"
        with process_out:
            clear_output()
            # 1. Asegurar que los scripts están descargados
            clonar_scripts()
            # 2. Ejecutar Install.py
            ip = get_ipython()
            if ip:
                ip.run_line_magic("run", "~/.swar/Install/Install.py")
                # Nota: Install.py ya incluye la ejecución de Updater.py internamente

    def run_desinstalar(_):
        # Ocultar el panel y ejecutar Uninstall.py desde la nueva ruta
        panel.layout.display = "none"
        with process_out:
            clear_output()
            # 1. Asegurar que los scripts están descargados
            clonar_scripts()
            # 2. Ejecutar Uninstall.py
            ip = get_ipython()
            if ip:
                ip.run_line_magic("run", "~/.swar/Install/Uninstall.py")
    # --- Fin de las funciones actualizadas ---

    # ... (la creación de botones y la interfaz se mantiene igual) ...
    btn_instalar = widgets.Button(description="instalar")
    btn_desinstalar = widgets.Button(description="desinstalar")

    for btn, clase in [
        (btn_instalar, "instalar"),
        (btn_desinstalar, "desinstalar")]:
        btn.add_class("custom-btn")
        btn.add_class(clase)

    btn_instalar.on_click(run_instalar)
    btn_desinstalar.on_click(run_desinstalar)

    row = widgets.HBox(
        [btn_instalar, btn_desinstalar],
        layout=widgets.Layout(
            width="100%",
            height="240px",
            gap="10px"))

    global panel
    panel = widgets.VBox(
        [row],
        layout=widgets.Layout(width="100%"))

    panel.add_class("setup-box")

    display(panel, process_out)

launch_interface()
