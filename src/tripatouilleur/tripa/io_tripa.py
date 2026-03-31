from pathlib import Path
import zipfile
import shutil
from PIL import Image
import os


def unzip_tripa(tripa_path: str | Path, workspace: str | Path):
    tripa_path = Path(tripa_path)
    workspace = Path(workspace)

    workspace.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(tripa_path, "r") as z:
        z.extractall(workspace)

    return workspace


def rezip_tripa(workspace: str | Path, out_tripa: str | Path):
    workspace = Path(workspace)
    out_tripa = Path(out_tripa)

    with zipfile.ZipFile(out_tripa, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for f in workspace.rglob("*"):
            if f.is_file():
                z.write(f, arcname=f.relative_to(workspace))


def delete_workspace(workspace: str | Path):
    shutil.rmtree(Path(workspace), ignore_errors=True)

def raw_animate(out_path: str | Path ,workspace:str|Path,triangle,format_exe,height,nom,divisor=2):
    img=[]
    dur=height*(height+1)/divisor
    out=Path(out_path)/f"image_{nom}"
    out_gif=Path(out_path)/(nom+".gif")
    out.mkdir(parents=True,exist_ok=True)
    Image.open(workspace/triangle[f"{0}_{0}"]).resize((300,300)).save(os.path.join(out, f"seed{0}_{0}" + '.png'))
    im0=Image.open(out/f"seed0_0.png")

    for i in range(height):
        for j in range(i+1):
            #im1=Image.open(seed_path/f"seed{i}{j}{format_seed}")
            #f"seed{i}{j}{format_seed}"
            Image.open(workspace/triangle[f"{i}_{j}"]).resize((300,300)).save(os.path.join(out, f"seed{i}_{j}" + '.png'))
            im2=Image.open(out/f"seed{i}_{j}.png").convert("RGBA")
            img.append(im2)
    im2.save(out_gif, save_all=True, append_images=img, duration=dur, loop=0)
    print("gif fait ")
