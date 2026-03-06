# Installation

## pip (recommended)

```bash
pip install mcp-server-parapilot
```

### Optional dependencies

```bash
# Mesh format conversion (meshio + trimesh)
pip install "mcp-server-parapilot[mesh]"

# Split-pane animations (Pillow + matplotlib)
pip install "mcp-server-parapilot[composite]"

# Everything
pip install "mcp-server-parapilot[all]"
```

## Claude Code Plugin

```bash
claude install kimimgo/parapilot
```

## From source

```bash
git clone https://github.com/kimimgo/parapilot.git
cd parapilot
pip install -e ".[dev]"
```

## Requirements

- Python 3.10+
- VTK (installed automatically via pip)
- For GPU rendering: NVIDIA GPU + driver
- For CPU rendering: OSMesa (included in VTK wheels)
