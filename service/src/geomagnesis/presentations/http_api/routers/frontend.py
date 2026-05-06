from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.geomagnesis.config import settings

router = APIRouter(prefix="", tags=["Frontend"])
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


@router.get("/")
def home_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="index.html")
