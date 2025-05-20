from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import sys
from api.geolocation import get_geolocation
from api.weather import get_weather
from api.garmin import get_garmin
from api.withings import get_withings
from utils.notes import get_notes
from utils.tasks import get_tasks
from utils.event_calendar import get_calendar
from utils.data_operations import load_json_data, save_json_data

# Configure logging to show more details
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="DayLog API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GeolocationRequest(BaseModel):
    city_name: Optional[str] = None
    use_ip: Optional[bool] = False

class WeatherResponse(BaseModel):
    temperature: float
    weathercode: int
    time: str
    units: str

@app.get("/test")
def test():
    logger.debug("Test endpoint called")
    return {"test": "ok"}

@app.get("/")
def root():
    logger.debug("Root endpoint called")
    try:
        response = {"status": "ok", "message": "Welcome to DayLog API"}
        logger.debug(f"Returning response: {response}")
        return response
    except Exception as e:
        logger.error(f"Error in root endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather")
async def weather():
    try:
        get_weather()
        return {"message": "Weather data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/geolocation")
async def geolocation():
    try:
        result = get_geolocation()
        if result is None:
            raise HTTPException(status_code=404, detail="Location not found")
        return {"message": "Location updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/garmin")
async def garmin():
    try:
        return get_garmin()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/withings")
async def withings():
    try:
        return get_withings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notes")
async def notes():
    try:
        return get_notes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks")
async def tasks():
    try:
        return get_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/calendar")
async def calendar():
    try:
        return get_calendar()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))