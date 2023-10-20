import asyncio

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from settings import database_url


Base = declarative_base()
engine = create_async_engine(database_url, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Koan(Base):
    __tablename__ = 'koans'
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, index=True)
    koan_text = Column(String, index=True)
    image_url = Column(String, index=True)
    image_description = Column(String, index=True)

    async def connect(self):
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(Koan().connect())
