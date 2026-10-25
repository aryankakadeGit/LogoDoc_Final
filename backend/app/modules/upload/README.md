MODULE: upload                STATUS: FINALIZED (pending local test)
Purpose : Turn raw upload bytes into a safe, normalized PNG for the AI.
Input   : prepare_image(data: bytes, *, max_bytes: int, max_dimension: int)
Output  : PreparedImage(png_bytes, width, height, source_format: png|jpeg|webp|svg)
Errors  : EmptyFile 400, FileTooLarge 413, UnsupportedFormat 415,
          InvalidImage 422, ImageTooLarge 413, UnsafeSvg 422   (all extend core AppError)
Depends : core.exceptions; pillow, defusedxml, resvg-py
Used by : api (analyze route) -> analysis
Test    : pytest tests/upload   |   python -m scripts.try_upload path/to/logo.svg

Rules
- Type comes from file content (magic bytes), never filename / Content-Type.
- In-memory only; nothing written to disk.
- Output is always PNG, metadata stripped, longest side <= max_dimension
  (raster: shrink only; SVG: rendered to fit max_dimension).
- The API layer must also stop reading the request at max_bytes (streaming guard).