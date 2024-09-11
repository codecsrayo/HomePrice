import os
from pydantic import PostgresDsn, field_validator,  AnyUrl
from typing import Optional, Any, Union, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    ASYNC_DATABASE_URI: Optional[str] = None

    TITLE: str
    DESCRIPTION: str
    BACKEND_CORS_ORIGINS: Union[List[str], List[AnyUrl]]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    def model_post_init(self, __context: Any) -> None:
        if self.ASYNC_DATABASE_URI is None:
            self.ASYNC_DATABASE_URI = str(
                PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    username=self.DATABASE_USER,
                    password=self.DATABASE_PASSWORD,
                    host=self.DATABASE_HOST,
                    port=self.DATABASE_PORT,
                    path=self.DATABASE_NAME,
                )
            )

    class Config:
        case_sensitive = True
        env_file = os.path.expanduser("/workspaces/HomePriceBackend/.env")


settings = Settings()
print(settings.ASYNC_DATABASE_URI)
