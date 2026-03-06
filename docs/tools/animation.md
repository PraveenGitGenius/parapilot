# Animation Tools

## animate

Create animations from time series data or camera orbits.

### Timestep animation

```json
{
  "file_path": "/data/sloshing.foam",
  "field_name": "alpha.water",
  "mode": "timesteps",
  "colormap": "Blue to Red Rainbow",
  "fps": 24,
  "speed_factor": 0.2,
  "output_format": "gif"
}
```

### Camera orbit

```json
{
  "file_path": "/data/beam.vtu",
  "field_name": "von_mises_stress",
  "mode": "orbit",
  "orbit_duration": 10.0,
  "output_format": "mp4"
}
```

### Speed factor

| Value | Effect |
|-------|--------|
| `1.0` | Real-time (physics 1s = video 1s) |
| `5.0` | 5x fast-forward |
| `0.2` | 5x slow-motion |

### Output formats

| Format | Use case |
|--------|----------|
| `frames` | PNG sequence only |
| `mp4` | H.264 video (requires ffmpeg) |
| `webm` | VP9 video (requires ffmpeg) |
| `gif` | Animated GIF (requires ffmpeg) |

## split_animate

Multi-pane synchronized animation combining 3D renders with time-series graphs.

```json
{
  "file_path": "/data/sloshing.foam",
  "panes": [
    {
      "type": "render", "row": 0, "col": 0,
      "render_pane": {"render": {"field": "alpha.water"}, "title": "Water"}
    },
    {
      "type": "graph", "row": 1, "col": 0,
      "graph_pane": {
        "series": [{"field": "alpha.water", "stat": "mean"}],
        "title": "Water Fraction"
      }
    }
  ],
  "fps": 24,
  "gif": true
}
```
