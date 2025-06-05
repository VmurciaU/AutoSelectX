# database/conection.py
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore

# URL de conexión actualizada con tus credenciales y puerto
DATABASE_URL = "postgresql://postgres:root@localhost:5433/autoselectx"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
