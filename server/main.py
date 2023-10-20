import os
import logging
from binascii import a2b_base64

from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import Body, Depends, FastAPI, HTTPException, Depends, status

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

import openai

import settings
import gpt4_service
import dalle_service
from database import SessionLocal, Koan

openai.api_key = settings.openai_api_key

app = FastAPI()

app.mount("/static", StaticFiles(directory=settings.static_folder), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Request(BaseModel):
    prompt : str | None = None
    koan_id : int | None = None


@app.on_event("startup")
async def init_tables():
    await Koan().connect()


@app.post('/api/generate-koan')
async def generate_koan(body: Request, db: AsyncSession = Depends(get_db)):
    if body.prompt == None:
        raise HTTPException(status=422, detail="A prompt is required")
    try:
        koan_text = gpt4_service.generate_koan(body.prompt)
        koan = Koan(koan_text=koan_text, prompt=body.prompt)
        db.add(koan)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'koan_id': koan.id, 'koan': koan_text}


@app.get('/api/koan/{id}')
async def get_koan(id: int, db: AsyncSession = Depends(get_db)):
    try:
        koan = await db.execute(select(Koan).where(Koan.id == id))
        koan = koan.scalar_one_or_none()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if koan is None:
        raise HTTPException(status_code=404, detail="Koan not found")
    return {
        'koan': koan.koan_text,
        'image_url': koan.image_url,
        'image_alt_text': koan.image_description,
    }


# TODO make this like a paginated thing with random option
@app.get('/api/koans')
async def get_koans(db: AsyncSession = Depends(get_db)):
    try:
        random_koans = await db.execute(
            select(Koan).order_by(func.random()).limit(10)
        )
        random_koans = random_koans.scalars().all()
        koan_list = [{
            'koan_id': koan.id,
            'koan_text': koan.koan_text,
            'image_url': koan.image_url,
            'image_alt_text': koan.image_description,
        } for koan in random_koans]
        return {'koans': koan_list}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/api/generate-image')
async def generate_image(body: Request, db: AsyncSession = Depends(get_db)):
    if body.koan_id == None:
        raise HTTPException(status=422, detail="koan_id is required")
    try:
        koan = await db.execute(select(Koan).where(Koan.id == body.koan_id))
        koan = koan.scalar_one_or_none()
        if koan is None:
            raise HTTPException(status_code=404, detail="Koan not found")

        description, image_data = dalle_service.generate_image(koan.koan_text)
        binary_data = a2b_base64(image_data)
        with open(os.path.join(settings.static_folder, "koans", f'{body.koan_id}.png'), 'wb') as fd:
            fd.write(binary_data)
            fd.close()

        koan.image_url = f"/static/koans/{body.koan_id}.png"
        koan.image_description = description
        await db.commit()
        return {'image_url': koan.image_url, "image_alt_text": koan.image_description}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.api_route("/{path_name:path}", methods=["GET"])
async def serve(path_name : str=None):
    return FileResponse(path=os.path.join(settings.static_folder, 'index.html'))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
