# Rendering Tools

## render

Basic field visualization returning a PNG screenshot.

```json
{
  "file_path": "/data/cavity.foam",
  "field_name": "p",
  "colormap": "Cool to Warm",
  "camera": "isometric",
  "width": 1920,
  "height": 1080
}
```

## cinematic_render

Publication-quality rendering with auto-framing, 3-point lighting, SSAO, and PBR materials.

### Quality Presets

| Preset | Resolution | Effects |
|--------|-----------|---------|
| `draft` | 960x540 | None (fast preview) |
| `standard` | 1920x1080 | SSAO + FXAA |
| `cinematic` | 1920x1080 | All + ground plane |
| `ultra` | 3840x2160 | All + ground plane |
| `publication` | 2400x1800 | Clean lighting, white background |

### Lighting Presets

- `cinematic` — warm key + cool fill + rim (default)
- `dramatic` — strong key, deep shadows
- `studio` — even, professional lighting
- `publication` — clean, minimal shadows
- `outdoor` — natural daylight simulation

## compare

Side-by-side or difference map comparison.

### Side-by-side mode

```json
{
  "file_a": "/data/coarse.foam",
  "file_b": "/data/fine.foam",
  "field_name": "p",
  "mode": "side_by_side"
}
```

### Diff mode

```json
{
  "file_a": "/data/v1.vtu",
  "file_b": "/data/v2.vtu",
  "field_name": "T",
  "mode": "diff"
}
```

## batch_render

Render multiple fields from the same dataset in one call.

```json
{
  "file_path": "/data/cavity.foam",
  "fields": ["p", "U", "T"],
  "quality": "standard"
}
```
