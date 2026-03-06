# Analysis Tools

## inspect_data

Returns comprehensive metadata about a simulation file:

- Bounds (spatial extents)
- Point arrays with data ranges
- Cell arrays with data ranges
- Timestep information
- Multiblock structure

```json
{
  "file_path": "/data/cavity.foam"
}
```

## extract_stats

Statistical summary (min, max, mean, std) for one or more fields.

```json
{
  "file_path": "/data/cavity.foam",
  "fields": ["p", "U"],
  "timestep": "latest"
}
```

## plot_over_line

Sample field values along a line between two points. Useful for validation against analytical solutions.

```json
{
  "file_path": "/data/cavity.foam",
  "field_name": "p",
  "point1": [0.0, 0.0, 0.0],
  "point2": [1.0, 0.0, 0.0],
  "resolution": 200
}
```

## integrate_surface

Integrate a field over a surface for force/flux calculations.

```json
{
  "file_path": "/data/cavity.foam",
  "field_name": "p",
  "boundary": "wall"
}
```

## probe_timeseries

Monitor a field at a fixed point across all timesteps.

```json
{
  "file_path": "/data/cavity.foam",
  "field_name": "p",
  "point": [0.5, 0.5, 0.05]
}
```
