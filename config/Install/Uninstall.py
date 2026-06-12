import subprocess
import os
from IPython.display import clear_output, Image, display
from IPython import get_ipython
from nenen88 import say

clear_output()

def uninstall_webui():
    base_paths = [
        os.path.expanduser("~/SwarmUI"),
        os.path.expanduser("~/ComfyUI"),
        os.path.expanduser("~/Forge"),
        os.path.expanduser("~/stable-diffusion-webui"),
        os.path.expanduser("~/tmp"),
        os.path.expanduser("~/.cache")
    ]

    img = os.path.expanduser("~/.gutris1/loading.png")
    display(Image(filename=img))
    say("<b>【{red} Uninstalling WebUI{d} 】{red}</b>")

    for path in base_paths:
        if os.path.exists(path):
            subprocess.run(f"rm -rf {path}", shell=True)

    clear_output()
    say("<b>【{red} SwarmUI desinstalado{d} 】{red}</b>")

    ipy = get_ipython()
    if ipy:
        ipy.kernel.do_shutdown(True)

if __name__ == "__main__":
    uninstall_webui()
