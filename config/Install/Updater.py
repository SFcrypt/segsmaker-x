import subprocess
import os
from IPython.display import clear_output, Image, display
from nenen88 import say

clear_output()
def run_update():
    base = os.path.expanduser("~/SwarmUI")
    img = os.path.expanduser("~/.gutris1/loading.png")

    display(Image(filename=img))
    say("<b>【{red} Updating SwarmUI{d} 】{red}</b>")

    os.makedirs(f"{base}/dlbackend", exist_ok=True)
    os.makedirs(f"{base}/Models/diffusion_models", exist_ok=True)

    subprocess.run([
        "git", "clone",
        "https://github.com/SFcrypt/ComfyUI",
        f"{base}/dlbackend/ComfyUI"])

    subprocess.run([
        "git", "clone",
        "https://github.com/SFcrypt/SwarmUI",
        f"{base}/SwarmUI_tmp"])

    subprocess.run(
        f"cp -r {base}/SwarmUI_tmp/* {base}/",
        shell=True)

    subprocess.run(
        f"rm -rf {base}/SwarmUI_tmp",
        shell=True)

    clear_output()
    say("<b>【{red} SwarmUI Instalado{d} 】{red}</b>")

if __name__ == "__main__":
    run_update()
