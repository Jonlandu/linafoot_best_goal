from fastapi import APIRouter, HTTPException, Request, Depends, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, validator, Field
from typing import Optional, Dict
from models import PaymentData, Video
from typing import Annotated
from database import SessionLocal
from sqlalchemy.orm import Session
import httpx

router = APIRouter()

# Define a function to get a database session
# Definir une fonction qui reccupere la session de la Base des Données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Define Pydantic models for request and response data
"""class PaymentData(BaseModel):
    mobilenumber: str = "00243907763838"
    trancurrency: str = "USD"
    amounttransaction: float =  5.00
    merchantid: str = "merch0000000000001042"
    invoiceid: str = "123456715"
    terminalid: str = "123456789012"
    encryptkey: str = "NozZSGL660ZZM8u4kUTV4CfgSy3G7wpFDQ0vCOhLWLpmnkNLkGia6mn7J2j2f4CJ/RDKF0ICxN7mBD9ciURYWj97KT2LYBoaPJVJs3hv5s5SGYoOw4fcAigt7+0nQiza"
    securityparams: Dict[str, str] = {
        "gpslatitude": "24.864190",
        "gpslongitude": "67.090420"
    }

    @validator('mobilenumber')
    def validate_mobilenumber(cls, value):
        if not isinstance(value, str):
            raise ValueError("Mobile number must be an string.")
        return value

    @validator('trancurrency')
    def validate_trancurrency(cls, value):
        if not isinstance(value, str):
            raise ValueError("Transaction currency must be a string.")
        return value

    @validator('amounttransaction')
    def validate_amounttransaction(cls, value):
        if not isinstance(value, float):
            raise ValueError("Amount transaction must be a float.")
        return value"""

class PaymentResponse(BaseModel):
    status: str
    message: str
    data: Optional[Dict] = None

class VoteRequest(BaseModel):
    videoId: int

class VoteResponse(BaseModel):
    status: str
    message: str
    voteCount: Optional[int] = None

# Define the endpoint for processing payments
@router.post("/payments", response_model=PaymentResponse)
async def process_payment(data: PaymentData = Body(...)):
    try:
        # Create a new Payment object
        payment = {
            "mobilenumber": data.mobilenumber,
            "trancurrency": data.trancurrency,
            "amounttransaction": data.amounttransaction,
            "merchantid": "merch0000000000001042",
            "invoiceid": "123456715",
            "terminalid": "123456789012",
            "encryptkey": "NozZSGL660ZZM8u4kUTV4CfgSy3G7wpFDQ0vCOhLWLpmnkNLkGia6mn7J2j2f4CJ/RDKF0ICxN7mBD9ciURYWj97KT2LYBoaPJVJs3hv5s5SGYoOw4fcAigt7+0nQiza",
            "securityparams": {
                "gpslatitude": "24.864190",
                "gpslongitude": "67.090420"
            }
        }

        # Add the payment to the database
        """db.add(payment)
        db.commit()
        db.refresh(payment)"""

        # Send payment request to RAWAPIGateway
        headers = {
            'LogInName': 'a5169891f7424defec80033e2c4264004716e4846b6929caea8f431c7568d604',
            'Content-Type': 'application/json',
            'LoginPass': '22cf830393691407806b22424dd66354e543c0e34f8161f00df1e74fa0a61e2b'
        }
        url = 'https://test.new.rawbankillico.com:4003/RAWAPIGateway/ecommerce/payment'
        auth = ('delta', '123456')
        """
        session = requests.Session()
        context = ssl.create_default_context()
        session.verify = context  # Set the SSL context on the session"""

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(url, json=payment, headers=headers, auth=auth)

            if response.status_code == 200:
                return JSONResponse(content=jsonable_encoder(
                    PaymentResponse(status="success", message="Payment processed successfully", data=response.json())),
                                    status_code=200)
            else:
                return JSONResponse(content=jsonable_encoder(
                    PaymentResponse(status="error", message="Payment processing failed", data=response.json())),
                                    status_code=response.status_code)
    except Exception as e:
        """db.rollback()"""
        raise HTTPException(status_code=500, detail = str(e))

# Define the endpoint for voting on videos
@router.post("/videos/{video_id}/vote", response_model=VoteResponse)
async def vote_on_video(video_id: int, data: VoteRequest, db: db_dependency):
    try:
        # Get the video from the database
        video = db.query(Video).filter(Video.id == video_id).first()

        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        """
        # Check if the payment was successful (you'll need to define your logic here)
        # Example: Check if the latest payment for the user is successful
        # You might need to add a user ID to the Payment model
        latest_payment = db.query(Payment).filter(Payment.userId == user_id).order_by(Payment.timestamp.desc()).first()

        if latest_payment and latest_payment.status == "success":
            # Increment the vote count
            video.voteCount += 1
            db.commit()
            db.refresh(video)
            return JSONResponse(content=jsonable_encoder(VoteResponse(status="success", message="Vote recorded successfully", voteCount=video.voteCount)), status_code=200)
        else:
            return JSONResponse(content=jsonable_encoder(VoteResponse(status="error", message="Payment not successful, vote not recorded")), status_code=400)

        # Replace the above example with your actual payment success check logic
        """
        # Increment the vote count if payment is successful
        video.voteCount += 1
        db.commit()
        db.refresh(video)

        return JSONResponse(content=jsonable_encoder(VoteResponse(status="success", message="Vote recorded successfully", voteCount=video.voteCount)), status_code=200)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
