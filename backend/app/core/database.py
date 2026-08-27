from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker

# from app.core.config import settings


# class Base(DeclarativeBase):
#     pass


<<<<<<< HEAD
# engine = create_engine(
#     settings.DATABASE_URL
# )


# SessionLocal = sessionmaker(
#     bind=engine,
#     autoflush=False,
#     autocommit=False
# )
=======
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
>>>>>>> 9f132266c64013c2075e8e445d55a2a65744e3e4
