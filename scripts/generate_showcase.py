#!/usr/bin/env python3
"""Generate showcase renders for the landing page.

Uses parapilot VTK engine directly — no ParaView needed.
Each render runs in a separate subprocess to ensure clean VTK state.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
OUT_DIR = PROJECT_ROOT / "www" / "public" / "showcase"

# Each render is a standalone Python snippet executed in its own process.
# This ensures clean VTK render window state and consistent dark backgrounds.

RENDERS: dict[str, str] = {
    "wavelet_contour": textwrap.dedent("""\
        import vtk
        from parapilot.engine.filters import apply_filter
        from parapilot.engine.renderer import RenderConfig, render_to_png
        from parapilot.engine.camera import CameraConfig

        src = vtk.vtkRTAnalyticSource()
        src.SetWholeExtent(-50, 50, -50, 50, -50, 50)
        src.Update()
        contoured = apply_filter(src.GetOutput(), "contour", array_name="RTData", values=[100, 150, 200, 250])
        cam = CameraConfig(position=(100.0, 80.0, 80.0), focal_point=(0, 0, 0), view_up=(0, 0, 1))
        cfg = RenderConfig(
            width=1920, height=1080, background=(0.04, 0.04, 0.06),
            colormap="turbo", array_name="RTData",
            show_scalar_bar=True, scalar_bar_title="RTData",
        )
        PNG = render_to_png(contoured, cfg, cam)
    """),

    "wavelet_volume": textwrap.dedent("""\
        import vtk
        from parapilot.engine.renderer import RenderConfig, render_to_png
        from parapilot.engine.camera import CameraConfig

        src = vtk.vtkRTAnalyticSource()
        src.SetWholeExtent(-50, 50, -50, 50, -50, 50)
        src.Update()
        cam = CameraConfig(position=(120.0, 80.0, 120.0), focal_point=(0, 0, 0), view_up=(0, 0, 1))
        cfg = RenderConfig(
            width=1920, height=1080, background=(0.04, 0.04, 0.06),
            colormap="cool to warm", array_name="RTData",
            show_scalar_bar=True, scalar_bar_title="RTData",
        )
        PNG = render_to_png(src.GetOutput(), cfg, cam)
    """),

    "wavelet_slice": textwrap.dedent("""\
        import vtk
        from parapilot.engine.filters import apply_filter
        from parapilot.engine.renderer import RenderConfig, render_to_png
        from parapilot.engine.camera import CameraConfig

        src = vtk.vtkRTAnalyticSource()
        src.SetWholeExtent(-50, 50, -50, 50, -50, 50)
        src.Update()
        sliced = apply_filter(src.GetOutput(), "slice", origin=[0, 0, 0], normal=[1, 0, 0])
        cam = CameraConfig(position=(100.0, 0.0, 0.0), focal_point=(0, 0, 0), view_up=(0, 0, 1))
        cfg = RenderConfig(
            width=1920, height=1080, background=(0.04, 0.04, 0.06),
            colormap="plasma", array_name="RTData",
            show_scalar_bar=True, scalar_bar_title="Pressure",
        )
        PNG = render_to_png(sliced, cfg, cam)
    """),

    "wavelet_clip": textwrap.dedent("""\
        import vtk
        from parapilot.engine.filters import apply_filter
        from parapilot.engine.renderer import RenderConfig, render_to_png
        from parapilot.engine.camera import CameraConfig

        src = vtk.vtkRTAnalyticSource()
        src.SetWholeExtent(-50, 50, -50, 50, -50, 50)
        src.Update()
        clipped = apply_filter(src.GetOutput(), "clip", origin=[0, 0, 0], normal=[1, 0, 0], inside_out=False)
        cam = CameraConfig(position=(100.0, 60.0, 80.0), focal_point=(0, 0, 0), view_up=(0, 0, 1))
        cfg = RenderConfig(
            width=1920, height=1080, background=(0.04, 0.04, 0.06),
            colormap="viridis", array_name="RTData",
            show_scalar_bar=True, scalar_bar_title="RTData",
        )
        PNG = render_to_png(clipped, cfg, cam)
    """),

    "superquadric": textwrap.dedent("""\
        import vtk
        from parapilot.engine.renderer import RenderConfig, render_to_png
        from parapilot.engine.camera import CameraConfig

        sq = vtk.vtkSuperquadricSource()
        sq.SetPhiResolution(128)
        sq.SetThetaResolution(128)
        sq.SetPhiRoundness(0.5)
        sq.SetThetaRoundness(1.7)
        sq.SetSize(1.0)
        sq.ToroidalOn()
        sq.Update()

        norms = vtk.vtkPolyDataNormals()
        norms.SetInputData(sq.GetOutput())
        norms.ComputePointNormalsOn()
        norms.Update()

        elev = vtk.vtkElevationFilter()
        elev.SetInputConnection(norms.GetOutputPort())
        elev.SetLowPoint(0, 0, -1)
        elev.SetHighPoint(0, 0, 1)
        elev.Update()

        cam = CameraConfig(position=(2.5, 1.5, 1.5), focal_point=(0, 0, 0), view_up=(0, 0, 1))
        cfg = RenderConfig(
            width=1920, height=1080, background=(0.04, 0.04, 0.06),
            colormap="magma", array_name="Elevation",
            show_scalar_bar=True, scalar_bar_title="Elevation",
        )
        PNG = render_to_png(elev.GetOutput(), cfg, cam)
    """),

    "streamlines": textwrap.dedent("""\
        import vtk
        from parapilot.engine.filters import apply_filter
        from parapilot.engine.renderer import RenderConfig, render_to_png
        from parapilot.engine.camera import CameraConfig

        src = vtk.vtkRTAnalyticSource()
        src.SetWholeExtent(-50, 50, -50, 50, -50, 50)
        src.Update()

        gradient = apply_filter(src.GetOutput(), "gradient", array_name="RTData")

        # Dense multi-seed grid for impressive coverage
        append = vtk.vtkAppendPolyData()
        for z in range(-40, 41, 10):
            for y in range(-40, 41, 15):
                line = vtk.vtkLineSource()
                line.SetPoint1(-40, y, z)
                line.SetPoint2(40, y, z)
                line.SetResolution(20)
                line.Update()
                append.AddInputData(line.GetOutput())
        append.Update()

        tracer = vtk.vtkStreamTracer()
        tracer.SetInputData(gradient)
        tracer.SetSourceConnection(append.GetOutputPort())
        tracer.SetInputArrayToProcess(0, 0, 0, vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, "Gradient")
        tracer.SetMaximumPropagation(300.0)
        tracer.SetIntegrationDirectionToBoth()
        tracer.SetIntegratorTypeToRungeKutta4()
        tracer.Update()

        tube = vtk.vtkTubeFilter()
        tube.SetInputData(tracer.GetOutput())
        tube.SetRadius(1.2)
        tube.SetNumberOfSides(12)
        tube.SetVaryRadiusToVaryRadiusByVector()
        tube.Update()

        cam = CameraConfig(position=(90.0, 70.0, 80.0), focal_point=(0, 0, 0), view_up=(0, 0, 1))
        cfg = RenderConfig(
            width=1920, height=1080, background=(0.04, 0.04, 0.06),
            colormap="plasma", array_name="Gradient",
            show_scalar_bar=True, scalar_bar_title="Gradient Magnitude",
        )
        PNG = render_to_png(tube.GetOutput(), cfg, cam)
    """),
}


def run_render(name: str, code: str) -> bool:
    """Run a render in an isolated subprocess."""
    preamble = f"import sys, io\nsys.path.insert(0, {str(PROJECT_ROOT / 'src')!r})\n\n"
    postamble = (
        "\n# Save optimized 960x540\n"
        "from PIL import Image\n"
        f"out_path = {str(OUT_DIR)!r} + '/{name}.png'\n"
        "img = Image.open(io.BytesIO(PNG))\n"
        "resized = img.resize((960, 540), Image.LANCZOS)\n"
        "resized.save(out_path, 'PNG', optimize=True)\n"
        "import os\n"
        "print(f'{os.path.getsize(out_path) // 1024}KB')\n"
    )
    wrapper = preamble + code + postamble

    result = subprocess.run(
        [sys.executable, "-c", wrapper],
        capture_output=True, text=True, timeout=60,
    )

    if result.returncode != 0:
        print(f"  FAIL: {result.stderr.strip().splitlines()[-1] if result.stderr else 'unknown'}")
        return False

    size = result.stdout.strip()
    print(f"  {name}.png: {size}")
    return True


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Generating {len(RENDERS)} showcase renders (isolated subprocess per render)...\n")

    success = 0
    for i, (name, code) in enumerate(RENDERS.items(), 1):
        print(f"[{i}/{len(RENDERS)}] {name}")
        if run_render(name, code):
            success += 1

    print(f"\nDone: {success}/{len(RENDERS)} renders saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
