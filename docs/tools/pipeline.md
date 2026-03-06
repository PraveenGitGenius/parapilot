# Pipeline DSL

The `execute_pipeline` tool accepts a full pipeline definition for complex workflows.

## Structure

```json
{
  "source": {
    "file": "/data/cavity.foam",
    "timestep": "latest"
  },
  "pipeline": [
    {"filter": "Slice", "params": {"origin": [0, 0, 0], "normal": [1, 0, 0]}},
    {"filter": "Calculator", "params": {"expression": "mag(U)", "result_name": "Umag"}}
  ],
  "output": {
    "type": "image",
    "render": {"field": "Umag", "colormap": "Viridis"}
  }
}
```

## Available Filters

| Filter | Description |
|--------|-------------|
| `Slice` | Cut plane through dataset |
| `Clip` | Remove half of dataset |
| `Contour` | Extract iso-surfaces |
| `Threshold` | Filter by scalar range |
| `StreamTracer` | Streamlines from vector field |
| `Calculator` | Compute derived fields |
| `Gradient` | Compute field gradients |
| `IntegrateVariables` | Integrate over domain |
| `GenerateSurfaceNormals` | Compute surface normals |
| `ExtractBlock` | Extract multiblock regions |
| `ExtractSurface` | Extract surface mesh |
| `WarpByVector` | Deform by vector field |
| `WarpByScalar` | Deform by scalar field |
| `CellDatatoPointData` | Convert cell to point data |
| `PlotOverLine` | Sample along a line |
| `Glyph` | Arrow/vector glyphs |
| `ProgrammableFilter` | Custom Python filter |
| `Decimate` | Reduce mesh resolution |
| `Triangulate` | Convert to triangles |

## Output Types

| Type | Description |
|------|-------------|
| `image` | PNG screenshot |
| `data` | JSON data extraction |
| `csv` | CSV file export |
| `animation` | Frame sequence or video |
| `export` | File format conversion |
| `multi` | Multiple outputs |

## Example: Heat Flux Computation

```json
{
  "source": {"file": "/data/thermal.foam", "timestep": "latest"},
  "pipeline": [
    {"filter": "Gradient", "params": {"field": "T", "result_name": "gradT"}},
    {"filter": "Calculator", "params": {"expression": "mag(gradT)", "result_name": "heatFlux"}}
  ],
  "output": {
    "type": "image",
    "render": {"field": "heatFlux", "colormap": "Plasma"}
  }
}
```
