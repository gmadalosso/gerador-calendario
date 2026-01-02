from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def calendario (
    request: Request,
    year: int | None = None
):
    year = year or datetime.now().year

    return templates.TemplateResponse(
        "calendario.html",
        {
            "request": request,
            "year": year
        }
    )
