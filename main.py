from fastapi import FastAPI
import models
from database import engine
from routers import payment, videos

# Create FastAPI app
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(payment.router)
app.include_router(videos.router)
