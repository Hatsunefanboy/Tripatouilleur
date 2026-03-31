import json
from pathlib import Path
from tempfile import TemporaryDirectory
from .io_tripa import *
from .create import *
from .reference import *



TRIPA_TYPES={"ImageTripa":{

    ".bmp",
    ".dib",

    ".gif",

    ".jpeg",
    ".jpg",
    ".jpe",

    ".png",

    ".tiff",
    ".tif",

    ".webp",

    ".ico",

    ".ppm",
    ".pgm",
    ".pbm",

    ".pcx",

    ".dds",

    ".sgi",

    ".tga",

    ".xbm",

    ".icns",

    ".jp2",     # jpeg2000 (si support)

    ".psd",

    ".eps",

    ".pdf", }    # lecture image PDF possible

}

class Tripa:
    def __init__(self):
        self.height=1

    def extend(self,n:int):
        raise NotImplementedError



class FileTripa(Tripa):
    def __init__(self, path: Path|str, workspace: Path|str):
        self.path = Path(path) # chemin du .tripa original

        self.workspace = Path(workspace)        # dossier dézippé

        self.manifest_path = self.workspace / "manifest.json"

        self._manifest = None             # lazy-loaded

        self._tmp=None

    @property
    def manifest(self)-> dict:
        if self._manifest is None:
            with open(self.manifest_path,"r",encoding="utf8") as f:
                self._manifest=json.load(f)
        return self._manifest

    @property
    def name(self):
        return self.manifest.get("name")

    @property
    def dim(self):
        return self.manifest.get("dim")

    @property
    def height(self):
        return self.manifest.get("height")

    @property
    def forward(self):
        return self.manifest.get("forward")

    @property
    def seed(self):
        return self.manifest.get("seed")

    @property
    def format(self):
        return self.seed.get("format")

    @property
    def executable_format(self):
        if self.seed.get("io")=="format":
            return self.format
        else:
            return ".bin"



    @property
    def triangle(self):
        return self.manifest.get("triangle")

    @property
    def engine(self):
        return self.manifest.get("engine")

    @property
    def default(self):
        return self.manifest.get("default")

    @property
    def dynamic(self):
        return self.default.get("type")=="dynamic"


    @classmethod
    def open(cls, tripa_path: str| Path):
        tripa_path=Path(tripa_path)

        tmp = TemporaryDirectory()
        workspace = Path(tmp.name)

        unzip_tripa(tripa_path, workspace)

        obj=cls(tripa_path,workspace)

        obj._tmp = tmp


        return obj

    @classmethod
    def create(cls,name: str,
    dim: int,
    forward_path: list[str],
    seed0_path: str | None,
    default_path: str,
    out_tripa: str=saved_tripa,
    format_bool:bool =False,
    dynamic:bool=False):
        t=init_tripa(name,dim,forward_path,seed0_path,default_path,out_tripa,format_bool,dynamic)

        return cls.open(t)
    def reload_manifest(self):
        self._manifest=None

    def save(self,out: Path| str| None=None):
        #si non specifier ecrase sinon créer un nouveaux
        out_path=Path(out) if out is not None else self.path

        rezip_tripa(self.workspace, out_path)
        self.path=out_path

    def close(self):
        if self._tmp is not None:
            self._tmp.cleanup()
            self._tmp=None


    def extract(self, out: Path | str):
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)

        for f in self.workspace.rglob("*"):
            if f.is_file():
                target = out / f.relative_to(self.workspace)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(f.read_bytes())
        return out

    def extract_seed(self, i=0, j=0, out=None):
        seed_name = f"seed{i}_{j}.bin"
        seed_path = self.workspace / "seeds" / seed_name

        if not seed_path.exists():
            raise FileNotFoundError(seed_name)

        fmt = self.format
        out = Path(out) if out else Path.cwd()
        out = out / f"{self.name}_seed{i}_{j}"
        out = out.with_suffix(fmt)

        out.write_bytes(seed_path.read_bytes())
        return out

    def extract_forward(self, out):
        out = Path(out)
        out.mkdir(parents=True, exist_ok=True)

        paths = []
        for f in self.forward:
            src = self.workspace / f
            suffix = Path(f).suffix
            dst = out / f"{self.name}_forward_{len(paths)}{suffix}"
            dst.write_bytes(src.read_bytes())
            paths.append(dst)

        return paths

    def extend(self,n=1):
        rawextend(self.workspace ,self.dynamic,self.executable_format,self.forward,self.height, n)
        self.reload_manifest()




class VirtualTripa(Tripa):
    def __init__(self,seed0,forward,dynamic=False,default=None):
        self.seeds={(0,0):seed0}
        self.forward=forward
        self.default= [default]
        self.height=1
        self.dynamic=dynamic

    def _read_seed(self,i,j):
        return self.seeds[(i,j)]

    def extend(self,n):
        height=self.height
        for i in range(height-1 ,height+n-1):
            if self.dynamic:
                self.default.append(self.forward(self.default[i],self.default[i]))
                self.seeds[(i+1,0)]=self.forward(self.default[i],self.seeds[(i,0)])
            else:
                self.seeds[(i+1,0)]=self.forward(self.default[0],self.seeds[(i,0)])
            for j in range(i):
                self.seeds[(i+1,j+1)]=self.forward(self.seeds[(i,j)],self.seeds[(i,j+1)])
            if self.dynamic:
                self.seeds[(i+1,i+1)]=self.forward(self.seeds[(i,i)],self.default[i])
            else:
                self.seeds[(i+1,i+1)]=self.forward(self.seeds[(i,i)],self.default[0])


class ImageTripa(FileTripa):
    def animate(self,out,divisor=2):
        #(out_path: str | Path ,workspace:str|Path,triangle,format_exe,height,nom,divisor=2
        out_arc=Path(out)
        raw_animate(out_arc,self.workspace,self.triangle,self.format,self.height,self.name,divisor)













