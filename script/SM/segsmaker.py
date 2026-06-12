from IPython.display import display, HTML, clear_output
from multiprocessing import Process, Condition, Value
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import argparse
import logging
import json
import yaml
import sys
import os

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
MARK = SRC / 'marking.json'
IMG = SRC / 'loading.png'

SyS = get_ipython().system

R = '\033[31m'
P = '\033[38;5;135m'
RST = '\033[0m'
ERR = f'{P}[{RST}{R}ERROR{RST}{P}]{RST}'

def get_args(ui):
    args_line = {
        'A1111': ('--xformers'),
        'Forge': ('--disable-xformers --opt-sdp-attention --cuda-stream'),
        'ReForge': ('--xformers --cuda-stream'),
        'Forge-Classic': ('--xformers --cuda-stream --persistent-patches'),
        'ComfyUI': ('--dont-print-server --use-pytorch-cross-attention'),
        'SwarmUI': ('--launch_mode none'),
        'FaceFusion': '',
        'SDTrainer': ''
    }

    return args_line.get(ui, '')

def GPU_check():
    return Path('/proc/driver/nvidia').exists()

def load_config():
    global ui
    config = json.loads(MARK.read_text()) if MARK.exists() else {}

    ui = config.get('ui', None)
    arg = config.get('launch_args')
    tunnell = config.get('tunnel')
    zrok_token.value = config.get('zrok_token', '')
    ngrok_token.value = config.get('ngrok_token', '')

    if arg:
        launch_args.value = arg
    else:
        launch_args.value = get_args(ui)

    if tunnell in ['Pinggy', 'ZROK', 'NGROK']:
        tunnel.value = tunnell
    else:
        tunnel.value = 'Pinggy'
        config.update({'tunnel': tunnel.value})
        MARK.write_text(json.dumps(config, indent=4))

    cpu_cb.value = False if GPU_check() else config.get('cpu_usage', False)
    cpu_cb.layout.display = 'none' if ui in ['SDTrainer', 'FaceFusion', 'SwarmUI'] or GPU_check() else 'block'

    ui_titles = {
        'A1111': 'A1111',
        'Forge': 'Forge',
        'ReForge': 'ReForge',
        'Forge-Classic': 'Forge Classic',
        'ComfyUI': 'ComfyUI',
        'SwarmUI': 'SwarmUI',
        'FaceFusion': 'Face Fusion',
        'SDTrainer': 'SD Trainer'
    }

    title.value = f"<div class='seg-title'>{ui_titles.get(ui, 'Unknown UI')}</div>"

def save_config(zrok_token, ngrok_token, launch_args, tunnel):
    config = json.loads(MARK.read_text()) if MARK.exists() else {}

    config.update({
        'zrok_token': zrok_token,
        'ngrok_token': ngrok_token,
        'launch_args': launch_args,
        'tunnel': tunnel,
        'cpu_usage': cpu_cb.value
    })

    MARK.write_text(json.dumps(config, indent=4))

def load_css():
    # Cargar estilo desde box.py
    try:
        os.chdir(os.path.expanduser("~"))
        download_dir = Path.home() / ".swar" / "Download"
        if str(download_dir) not in sys.path:
            sys.path.insert(0, str(download_dir))
        from box import load_style
        load_style()
    except Exception as e:
        # Si no funciona, usar CSS local
        css = """
        .seg-box {
            background: #1E1F21;
            border-radius: 12px;
            padding: 25px;
            width: 100%;           
            max-width: 100%;
            font-family: 'Source Sans Pro', sans-serif;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;    
            justify-content: center;
        }
        .seg-title {
            color: rgba(255,255,255,0.9);
            font-size: 27px;        
            font-weight: 400;       
            margin-bottom: 12px;
        }
        .seg-input-html input {
            background: #333333;  
            border: none;
            border-radius: 12px;
            padding: 12px 0;
            width: 80%;
            margin-bottom: 6px;
            color: rgba(255,255,255,0.85);
            font-size: 18px;       
            text-align: center;
            transition: none;
        }
        .seg-input-html input::placeholder {
            color: rgba(255,255,255,0.7);
            text-align: center;
        }
        .seg-button {
            border: 2px solid #C41564;
            border-radius: 12px;
            background: #C41564;
            color: #fff;
            font-size: 15px;
            padding: 8px 50px;
            margin-top: 4px;
            transition: background 0.3s ease, transform 0.2s ease;
        }
        .seg-button:hover {
            background: #db5a94;
            transform: translateY(-1px);
        }
        """
        display(HTML(f"<style>{css}</style>"))

# ============ NUEVA INTERFAZ ============
title = widgets.HTML()
zrok_token = widgets.Text(placeholder="ZROK Token", layout=widgets.Layout(width="80%", margin="6px 0"))
zrok_token.add_class("seg-input-html")
ngrok_token = widgets.Text(placeholder="NGROK Token", layout=widgets.Layout(width="80%", margin="6px 0"))
ngrok_token.add_class("seg-input-html")
launch_args = widgets.Text(
    placeholder="Launch Arguments (ej: --xformers --opt-sdp-attention)",
    layout=widgets.Layout(width="80%", margin="6px 0")
)
launch_args.add_class("seg-input-html")

cpu_cb = widgets.Checkbox(value=False, description="Modo CPU", layout=widgets.Layout(margin="12px 0 8px 0"))

# Selector de tunel con ToggleButtons
tunnel = widgets.ToggleButtons(
    options=['Pinggy', 'ZROK', 'NGROK'],
    button_style='',
    layout=widgets.Layout(
        display='flex',
        justify_content='center',
        margin='0 0 15px 0'
    )
)

tunnel.style = {'button_width': '100px'}

def update_tunnel_style(change):
    if change['new'] in ['Pinggy', 'ZROK', 'NGROK']:
        tunnel.style = {'button_width': '100px', 'colors': {'selected': '#C41564'}}

tunnel.observe(update_tunnel_style, 'value')

# Botones
launch_button = widgets.Button(description="Iniciar", layout=widgets.Layout(height="35px", padding="0 50px"))
launch_button.add_class("seg-button")

exit_button = widgets.Button(description="Exit", layout=widgets.Layout(height="35px", padding="0 50px"))
exit_button.add_class("seg-button")

button_box = widgets.HBox(
    [launch_button, exit_button],
    layout=widgets.Layout(
        display='flex',
        gap='20px',
        justify_content='center',
        margin='15px 0 0 0'
    )
)

# Formulario completo
form_box = widgets.VBox([
    title,
    tunnel,
    zrok_token,
    ngrok_token,
    launch_args,
    cpu_cb,
    button_box
])
form_box.add_class("seg-box")

launch_panel = form_box
# ============ FIN NUEVA INTERFAZ ============

parser = argparse.ArgumentParser()
parser.add_argument('--skip-comfyui-check', action='store_true', help='Skip checking custom node dependencies for ComfyUI')
parser.add_argument('--skip-widget', action='store_true', help='Skip displaying the widget')
args, unknown = parser.parse_known_args()

condition = Condition()
is_ready = Value('b', False)

def NGROK_ZROK(T):
    P = {
        'zrok': {
            'B': HOME / '.zrok/bin/zrok',
            'C': HOME / '.zrok/environment.json',
            't': zrok_token.value
        },
        'ngrok': {
            'B': HOME / '.ngrok/bin/ngrok',
            'C': HOME / '.config/ngrok/ngrok.yml',
            't': ngrok_token.value
        }
    }

    B, C, t = P[T]['B'], P[T]['C'], P[T]['t']

    if not t:
        print(f'{ERR}: {T.upper()} Token is empty'); sys.exit()
    if not B.exists():
        print(f'{ERR}: {T.upper()} is not installed'); sys.exit()

    E = f'{T} enable {t}' if T == 'zrok' else f'{T} config add-authtoken {t}'

    if C.exists():
        ct = None
        if T == 'zrok':
            ct = json.loads(C.read_text()).get('zrok_token')
        elif T == 'ngrok':
            ct = yaml.safe_load(C.read_text()).get('agent', {}).get('authtoken')

        if ct != t:
            if T == 'zrok':
                SyS(f'{T} disable')
            SyS(E); print()
    else:
        SyS(E); print()

def launching(ui, skip_comfyui_check=False):
    args_launch = f'{launch_args.value}'
    tunnel_name = tunnel.value

    get_ipython().run_line_magic('run', 'venv.py')

    if ui in ['A1111', 'Forge', 'ReForge', 'Forge-Classic']:
        port = 7860
        PY = '/tmp/python311/bin/python3' if ui == 'Forge-Classic' else '/tmp/venv/bin/python3'
        args_launch += ' --enable-insecure-extension-access --disable-console-progressbars --theme dark'

    elif ui in ['ComfyUI', 'SwarmUI']:
        PY = '/tmp/venv-comfy-swarm/bin/python3'

        if ui == 'ComfyUI':
            port = 8188
            skip_comfyui_check or (SyS(f'{PY} apotek.py'), clear_output(wait=True))
        else:
            port = 7801

    elif ui == 'SDTrainer':
        port = 28000
        PY = 'HF_HOME=huggingface /tmp/venv-sd-trainer/bin/python3'

    elif ui == 'FaceFusion':
        port = 7860
        PY = '/tmp/venv-fusion/bin/python3'

    if cpu_cb.value:
        if ui == 'A1111':
            args_launch += ' --use-cpu all --precision full --no-half --skip-torch-cuda-test'
        elif ui in ['Forge', 'ReForge', 'Forge-Classic']:
            args_launch += ' --always-cpu --skip-torch-cuda-test'
        elif ui == 'ComfyUI':
            args_launch += ' --cpu'

    tunnel_config = {
        'Pinggy': {
            'command': f'ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:{port} a.pinggy.io',
            'name': 'PINGGY',
            'pattern': r'https://[\w-]+\.run\.pinggy-free\.link'
        },
        'NGROK': {
            'command': f'ngrok http http://localhost:{port} --log stdout',
            'name': 'NGROK',
            'pattern': r'https://[\w-]+\.ngrok-free\.[\w.-]+'
        },
        'ZROK': {
            'command': f'zrok share public localhost:{port} --headless',
            'name': 'ZROK',
            'pattern': r'https://[\w-]+\.share\.zrok\.[\w.-]+'
        }
    }

    c = f'{PY} Launcher.py {args_launch}'
    cmd = {key: c for key in ['Pinggy', 'ZROK', 'NGROK']}.get(tunnel_name)
    configs = tunnel_config.get(tunnel_name)

    if cmd and configs:
        try:
            from cupang import Tunnel as Alice_Zuberg

            if tunnel_name == 'ZROK': NGROK_ZROK('zrok')
            if tunnel_name == 'NGROK': NGROK_ZROK('ngrok')

            Alice_Synthesis_Thirty = Alice_Zuberg(port)
            Alice_Synthesis_Thirty.logger.setLevel(logging.DEBUG)
            Alice_Synthesis_Thirty.add_tunnel(command=configs['command'], name=configs['name'], pattern=configs['pattern'])

            with Alice_Synthesis_Thirty: SyS(cmd)
        except KeyboardInterrupt:
            pass

def waiting(condition, is_ready):
    with condition:
        while not is_ready.value:
            try:
                condition.wait()
            except KeyboardInterrupt:
                print('')
                clear_output()
                sys.exit()

    load_config()
    launching(ui, skip_comfyui_check=args.skip_comfyui_check)

def launch(b):
    global ui, zrok_token, ngrok_token, launch_args, tunnel
    launch_panel.close()
    save_config(zrok_token.value, ngrok_token.value, launch_args.value, tunnel.value)
    with condition:
        is_ready.value = True
        condition.notify()

def exit(b):
    launch_panel.close()

def display_widgets():
    load_config()
    load_css()
    display(launch_panel)
    launch_button.on_click(launch)
    exit_button.on_click(exit)

if __name__ == '__main__':
    try:
        if args.skip_widget:
            load_config()
            launching(ui, skip_comfyui_check=args.skip_comfyui_check)

        else:
            display_widgets()
            p = Process(target=waiting, args=(condition, is_ready))
            p.start()

    except KeyboardInterrupt:
        pass
