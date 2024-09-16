from sqlalchemy.orm import sessionmaker
from api.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


DB_POOL_SIZE = 83
WEB_CONCURRENCY = 9
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

connect_args = {"check_same_thread": False}


engine = create_async_engine(
    settings.ASYNC_DATABASE_URI,
    echo=False,
    future=True,
    pool_size=POOL_SIZE,
    max_overflow=64,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
