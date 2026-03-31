from pathlib import Path
import zipfile
import shutil


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