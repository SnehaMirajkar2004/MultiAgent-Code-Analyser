import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL

logger = logging.getLogger(__name__)

# Create SQLAlchemy Engine
try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Failed to initialize database engine: {e}")
    engine = None
    SessionLocal = None

Base = declarative_base()


def get_db():
    """
    FastAPI Dependency to provide a database session per request.
    Yields None if database is not reachable.
    """
    if SessionLocal is None:
        yield None
        return

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Creates database tables on application startup.
    Fails gracefully with a warning if PostgreSQL is not yet running.
    """
    if engine is None:
        print("[DATABASE WARNING] Database Engine not initialized. Persistence will be bypassed.")
        return False

    try:
        from app.models.analysis import AnalysisRecord  # noqa: F401
        Base.metadata.create_all(bind=engine)
        print("[DATABASE SUCCESS] PostgreSQL tables initialized successfully.")
        return True
    except Exception as e:
        print(f"[DATABASE WARNING] Could not connect to PostgreSQL ({e}). Persistence will be bypassed until PostgreSQL is running.")
        return False
