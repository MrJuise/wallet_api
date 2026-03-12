import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

_engine = None
_sessionmaker = None


def get_engine():
    url = os.environ.get('DATABASE_URL')
    if url is None:
        raise RuntimeError('DATABASE_URL is not set')
    global _engine
    if _engine is None:
        _engine = create_async_engine(url, pool_pre_ping=True, echo=False, poolclass=NullPool)
    return _engine


def get_sessionmaker():
    global _sessionmaker
    if _sessionmaker is None:
        _sessionmaker = async_sessionmaker(bind=get_engine(), autoflush=False)
    return _sessionmaker


async def get_db():
    session_factory = get_sessionmaker()
    db = session_factory()
    try:
        yield db
    finally:
        await db.close()
