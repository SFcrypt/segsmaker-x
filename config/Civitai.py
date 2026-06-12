import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
from IPython import get_ipython

def launch_interface():

    process_out = widgets.Output()

    css_url = "https://raw.githubusercontent.com/gutris1/segsmaker/refs/heads/main/script/SM/setup.css"
    display(HTML(f'<link rel="stylesheet" type="text/css" href="{css_url}">'))

    modelos_img = "https://raw.githubusercontent.com/SFcrypt/Segsmaker/main/cover/003219.png"
    loras_img   = "https://raw.githubusercontent.com/SFcrypt/Segsmaker/main/cover/092918.png"

    display(HTML(f"""
    <style>
    .setup-box {{
        padding: 10px;
        border-radius: 16px;
        background: #000000;
        overflow: hidden;
    }}

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
        overflow: hidden;
    }}

    .custom-btn:hover {{
        border-color: #00aaff !important;
        box-shadow: 0 0 0 2px #00aaff;
        transform: translateY(-2px);
    }}

    .modelos {{
        background-image: url('{modelos_img}');
    }}

    .loras {{
        background-image: url('{loras_img}');
    }}

    .widget-button {{
        min-width: 0 !important;
    }}

    .widget-box, .output_wrapper, .output {{
        overflow: hidden !important;
        max-height: none !important;
    }}
    </style>
    """))

    def run_modelos(_):
        panel.layout.display = "none"
        with process_out:
            clear_output()
            ip = get_ipython()
            if ip:
                ip.run_line_magic("run", ".civitai/Model.py")

    def run_loras(_):
        panel.layout.display = "none"
        with process_out:
            clear_output()
            ip = get_ipython()
            if ip:
                ip.run_line_magic("run", ".civitai/Loras.py")

    btn_modelos = widgets.Button(description="modelos")
    btn_loras   = widgets.Button(description="loras")

    for btn, clase in [
        (btn_modelos, "modelos"),
        (btn_loras, "loras")
    ]:
        btn.add_class("custom-btn")
        btn.add_class(clase)

    btn_modelos.on_click(run_modelos)
    btn_loras.on_click(run_loras)

    row = widgets.HBox(
        [btn_modelos, btn_loras],
        layout=widgets.Layout(
            width="100%",
            height="240px",
            gap="10px"
        )
    )

    global panel
    panel = widgets.VBox(
        [row],
        layout=widgets.Layout(width="100%")
    )

    panel.add_class("setup-box")

    display(panel, process_out)


if __name__ == "__main__":
    launch_interface()
