from fastapi import FastAPI
from api.core.config import settings
from starlette.responses import RedirectResponse
from api.routers import registed_routers


app = FastAPI(
    title=settings.TITLE, version="0.1.0"
)


@app.get("/", include_in_schema=False)
async def main():
    """Redireccionar desde / a /docs"""
    return RedirectResponse(url="/docs")


app.include_router(registed_routers, prefix=f"{settings.API_V1_STR}/v1")
