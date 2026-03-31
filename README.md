# Tripatouilleur

`Tripatouilleur` is a Python package to create, open, extend, and animate `.tripa` files.

License: MIT
Author: Cognet Benjamin

## Installation

```bash
pip install tripatouilleur
```

For local development:

```bash
pip install -e .
```

## Quick start

```python
from tripatouilleur import FileTripa

tripa = FileTripa.open("example.tripa")
tripa.extend(2)
tripa.save("example_extended.tripa")
tripa.close()
```

## Package contents

- `tripatouilleur.Tripa`: base class
- `tripatouilleur.FileTripa`: work with `.tripa` archives on disk
- `tripatouilleur.ImageTripa`: image-oriented helpers
- `tripatouilleur.VirtualTripa`: in-memory triangle generation

## Build a distribution

```bash
py -m build
```

This generates a source distribution and a wheel in `dist/`.
