import json
import subprocess
import sys
import zipfile
from pathlib import Path


def init_tripa(
    name: str,
    dim: int,
    forward_path: list[str],
    seed0_path: str | None,
    default_path: str,
    out_tripa: str,
    format_bool: bool = True,
    dynamic: bool = False,
):
    if len(forward_path) != dim:
        raise ValueError(f"Forward doit contenir {dim} chemins ")
    if not Path(default_path).exists():
        raise FileNotFoundError(default_path)

    reel_forward = [f"forward/{i}{Path(forward_path[i]).suffix}" for i in range(dim)]
    seed_io = "format" if format_bool else "bytes"

    if format_bool:
        seed_format = Path(seed0_path).suffix if seed0_path is not None else Path(default_path).suffix
    else:
        seed_format = ".bin"

    seed0_0 = f"seeds/seed0_0{seed_format}" if seed0_path else f"seeds/default0{seed_format}"
    dynamics = "dynamic" if dynamic else "static"

    manifest = {
        "name": name,
        "dim": dim,
        "height": 1,
        "forward": reel_forward,
        "default": {"type": dynamics, "default0": f"seeds/default0{seed_format}"},
        "engine": "unsafe_exec",
        "seed": {
            "io": seed_io,
            "format": seed_format,
        },
        "triangle": {
            "0_0": seed0_0,
        },
    }

    out_dir = Path(out_tripa)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{name}.tripa"

    with zipfile.ZipFile(out_file, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))

        for src, arc in zip(forward_path, reel_forward):
            z.write(src, arcname=arc)

        if seed0_path:
            z.write(seed0_path, arcname=Path("seeds/seed0_0").with_suffix(seed_format))
        z.write(default_path, arcname=Path("seeds/default0").with_suffix(seed_format))

    print(f"fichier fait : {out_file}")
    return str(out_file)


def run_on_seeds(exe_path: str | Path, seed1_path: str | Path, seed2_path: str | Path, out_path: str | Path, name: str):
    exe_arc = Path(exe_path)
    in1 = Path(seed1_path)
    in2 = Path(seed2_path)
    out = (Path(out_path) / name).with_suffix(in2.suffix)

    if exe_arc.suffix.lower() == ".py":
        cmd = [sys.executable, str(exe_arc), in1, in2, out]
    else:
        cmd = [str(exe_arc), in1, in2, out]

    proc = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))

    if not out.exists():
        raise RuntimeError("L'executable n'a pas produit de fichier de sortie")

    return out


def rawextend(unzip_path: str | Path, dynamic_bool, format_seed, forward, height, n: int = 1):
    # Le manifest est recalcule puis reecrit apres extension.
    unzip_path = Path(unzip_path)
    forward_suffix = Path(forward[0]).suffix
    forward_path = unzip_path / "forward"
    seed_path = unzip_path / "seeds"
    manifest_path = unzip_path / "manifest.json"
    manifest = json.loads(manifest_path.read_text("utf-8"))

    for i in range(height - 1, height + n - 1):
        if dynamic_bool:
            run_on_seeds(
                forward_path / f"0{forward_suffix}",
                seed_path / f"default{i}{format_seed}",
                seed_path / f"default{i}{format_seed}",
                seed_path,
                f"default{i+1}",
            )
            manifest[f"default{i}"] = f"seeds/default{i}{format_seed}"

            default_path = seed_path / f"default{i}{format_seed}"
            run_on_seeds(
                forward_path / f"0{forward_suffix}",
                default_path,
                seed_path / f"seed{i}_{0}{format_seed}",
                seed_path,
                f"seed{i+1}_{0}",
            )
            manifest["triangle"][f"{i+1}_{0}"] = f"seeds/seed{i+1}_{0}{format_seed}"
        else:
            default_path = seed_path / f"default0{format_seed}"
            run_on_seeds(
                forward_path / f"0{forward_suffix}",
                default_path,
                seed_path / f"seed{i}_{0}{format_seed}",
                seed_path,
                f"seed{i+1}_{0}",
            )
            manifest["triangle"][f"{i+1}_{0}"] = f"seeds/seed{i+1}_{0}{format_seed}"

        for j in range(i):
            run_on_seeds(
                forward_path / f"0{forward_suffix}",
                seed_path / f"seed{i}_{j}{format_seed}",
                seed_path / f"seed{i}_{j+1}{format_seed}",
                seed_path,
                f"seed{i+1}_{j+1}",
            )
            manifest["triangle"][f"{i+1}_{j+1}"] = f"seeds/seed{i+1}_{j+1}{format_seed}"

        run_on_seeds(
            forward_path / f"0{forward_suffix}",
            seed_path / f"seed{i}_{i}{format_seed}",
            default_path,
            seed_path,
            f"seed{i+1}_{i+1}",
        )
        manifest["triangle"][f"{i+1}_{i+1}"] = f"seeds/seed{i+1}_{i+1}{format_seed}"

    manifest["height"] = height + n
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), "utf-8")
