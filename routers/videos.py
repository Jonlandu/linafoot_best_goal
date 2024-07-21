from fastapi import APIRouter, HTTPException, Depends, Path
from pydantic import BaseModel, Field, schema
from starlette import status
from models import Video
from typing import Annotated, List
from database import SessionLocal, Base
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, JSON

router = APIRouter(
    tags=['video']
)

# Define a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class VideoRequest(BaseModel):
    youtubeId: str = Field(min_length=1)
    title: str = Field(min_length=3)
    playerName: str = Field(min_length=3)

    thumbnailUrl: str = Field(default='https://www.youtube.com/watch?v=')
    #publishedAt: datetime

# Define the endpoint for getting all videos
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_videos(db: db_dependency):
    try:
        # Get all videos from the database
        videos = db.query(Video).all()
        return videos

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("video/{video_id}", status_code=status.HTTP_200_OK)
async def fetch_video(db: db_dependency, video_id: int = Path(gt=0)):
   video_model = db.query(Video).filter(Video.id == video_id).first()
   if video_model is not None:
       return video_model
   raise HTTPException(status_code=404, detail='Video not found.')

@router.post("/video", status_code=status.HTTP_201_CREATED)
async def create_videos(db: db_dependency, video_request: VideoRequest):
    video_model = Video(**video_request.model_dump())

    db.add(video_model)
    db.commit()

@router.put("/video/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_video(db: db_dependency, video_request: VideoRequest, video_id: int = Path(gt=0)):
    video_model = db.query(Video).filter(Video.id == video_id).first()
    if video_model is None:
        raise HTTPException(status_code=404, detail='Video not found.')
    video_model.youtubeId = video_request.youtubeId
    video_model.title = video_request.title
    video_model.playerName = video_request.playerName
    video_model.thumbnailUrl = video_request.thumbnailUrl

    db.add(video_model)
    db.commit()

@router.delete("/video/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_video(db: db_dependency, video_id: int = Path(gt=0)):
    video_model = db.query(Video).filter(Video.id == video_id).first()
    if video_model is None:
        raise HTTPException(status_code=404, detail='Video not found.')

    db.query(Video).filter(Video.id == video_id).delete()
    db.commit()