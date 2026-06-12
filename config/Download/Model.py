import ipywidgets as widgets
from IPython.display import display, clear_output
from IPython import get_ipython
from pathlib import Path
import sys

def launch_model_downloader():
    ipy = get_ipython()
    
    # Cambiar al directorio home
    ipy.run_line_magic("cd", "~")
    
    # Agregar la ruta donde ya están los archivos descargados
    download_dir = Path.home() / ".swar" / "Download"
    if str(download_dir) not in sys.path:
        sys.path.insert(0, str(download_dir))
    
    # Importar box.py desde la ubicación actualizada
    from box import load_style
    
    load_style()
    
    main_container = widgets.VBox()
    output = widgets.Output()
    
    link_input = widgets.Text(
        placeholder="Link de descarga",
        layout=widgets.Layout(width="80%", margin="0 0 6px 0"))
    link_input.add_class("seg-input-html")
    
    nombre_input = widgets.Text(
        placeholder="Nombre del archivo",
        layout=widgets.Layout(width="80%", margin="0 0 6px 0"))
    nombre_input.add_class("seg-input-html")
    
    download_btn = widgets.Button(
        description="Download",
        layout=widgets.Layout(height="35px", padding="0 0px"))
    download_btn.add_class("seg-button")
    
    def descargar_modelo(b):
        if ipy:
            ipy.run_line_magic("cd", "$CKPT")
        main_container.children = [output]
        with output:
            clear_output()
            Link = link_input.value.strip()
            Nombre = "-".join(nombre_input.value.strip().split())
            if not Link or not Nombre:
                return
            try:
                if ipy:
                    ipy.run_line_magic(
                        "download",
                        f"{Link} {Nombre}.safetensors"
                    )
            except:
                pass
    
    download_btn.on_click(descargar_modelo)
    
    form_box = widgets.VBox([
        widgets.HTML("<div class='seg-title'>Descargar Modelo</div>"),
        link_input,
        nombre_input,
        download_btn])
    form_box.add_class("seg-box")
    
    main_container.children = [form_box]
    display(main_container)

# ejecutar
launch_model_downloader()
