from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

Base = declarative_base()

class Koan(Base):
    __tablename__ = 'koans'
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, index=True)
    koan_text = Column(String, index=True)
    image_url = Column(String, index=True)
    image_description = Column(String, index=True)

DATABASE_URL = "sqlite+aiosqlite:///koans.db"
__CREATE_TABLE_URL = "sqlite:///koans.db"

engine = create_engine(__CREATE_TABLE_URL, echo=True)

try:
    with engine.connect() as connection:
        connection.execute(text('ALTER TABLE koans ADD COLUMN prompt STRING'))
except Exception:
    pass

Base.metadata.create_all(bind=engine)
engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
