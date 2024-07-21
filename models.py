from database import Base
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
import sqlalchemy
from pydantic import BaseModel
from pydantic import schema
from datetime import datetime

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True)
    youtubeId = Column(String)
    title = Column(String)
    playerName = Column(String)
    thumbnailUrl = Column(String, default='https://www.youtube.com/watch?v=')
    voteCount = Column(Integer, default=0)
    publishedAt = Column(sqlalchemy.DateTime, default=datetime.utcnow)

# Define SQLAlchemy model for storing payment data
class PaymentData(BaseModel):
    mobilenumber: str
    trancurrency: str
    amounttransaction: float