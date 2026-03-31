# Tripa

`Tripa` is a Python package to create, open, extend, and animate `.tripa` files.

License: MIT
Author: Cognet Benjamin

## Installation

```bash
pip install tripa
```

For local development:

```bash
pip install -e .
```

## Quick start

```python
from tripa import FileTripa

tripa = FileTripa.open("example.tripa")
tripa.extend(2)
tripa.save("example_extended.tripa")
tripa.close()
```

## Package contents

- `tripa.Tripa`: base class
- `tripa.FileTripa`: work with `.tripa` archives on disk
- `tripa.ImageTripa`: image-oriented helpers
- `tripa.VirtualTripa`: in-memory triangle generation

## Build a distribution

```bash
py -m build
```

This generates a source distribution and a wheel in `dist/`.
