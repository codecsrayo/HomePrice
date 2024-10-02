from fastapi import FastAPI
from api.core.config import settings
from starlette.responses import RedirectResponse
from api.routers import registed_routers
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.TITLE, version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# @app.get("/api", include_in_schema=False)
# async def main():
#     """Redireccionar desde / a /docs"""
#     return RedirectResponse(url=f"{settings.API_V1_STR}/docs")


app.include_router(registed_routers, prefix=f"{settings.API_V1_STR}/v1")
