"""
POST /api/logo/analyze

Request : the image file itself as the raw request body (e.g. fetch(url, { method: "POST", body: file })).
          Read as a stream and stopped at the size limit; nothing is written to disk.
Response: { is_logo: true, analysis, logo_status }  or  { is_logo: false, message }
"""

from typing import Annotated, Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from app.api.dependencies import AIDep, SettingsDep
from app.api.rate_limit import rate_limited
from app.modules.analysis import LogoAnalysis, NotALogo, analyze_logo
from app.modules.logo_status import LogoStatus, get_logo_status
from app.modules.upload import FileTooLarge, prepare_image

router = APIRouter(prefix="/logo", tags=["analysis"])


class AnalyzeLogoResponse(BaseModel):
    is_logo: Literal[True] = True
    analysis: LogoAnalysis
    logo_status: LogoStatus


AnalyzeResponse = Annotated[AnalyzeLogoResponse | NotALogo, Field(discriminator="is_logo")]

_BINARY_BODY = {
    "requestBody": {
        "required": True,
        "content": {"application/octet-stream": {"schema": {"type": "string", "format": "binary"}}},
    }
}


async def _read_body(request: Request, max_bytes: int) -> bytes:
    too_large = FileTooLarge(f"The file exceeds the {max_bytes / (1024 * 1024):g} MB limit.")
    declared = request.headers.get("content-length", "")
    if declared.isdigit() and int(declared) > max_bytes:
        raise too_large
    data = bytearray()
    async for chunk in request.stream():
        data += chunk
        if len(data) > max_bytes:
            raise too_large
    return bytes(data)


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    dependencies=[rate_limited("analyze")],
    openapi_extra=_BINARY_BODY,
)
async def analyze(request: Request, settings: SettingsDep, ai: AIDep) -> AnalyzeLogoResponse | NotALogo:
    data = await _read_body(request, settings.max_upload_bytes)
    # Image decoding/rendering is CPU work: run it in a thread so other requests are not blocked.
    image = await run_in_threadpool(
        prepare_image,
        data,
        max_bytes=settings.max_upload_bytes,
        max_dimension=settings.max_image_dimension,
    )
    result = await analyze_logo(image, ai)
    if isinstance(result, NotALogo):
        return result
    return AnalyzeLogoResponse(analysis=result, logo_status=get_logo_status(result))