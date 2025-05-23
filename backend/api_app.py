from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel

from api.garmin import get_garmin
from api.geolocation import get_geolocation
from api.weather import get_weather
from api.withings import get_withings
from core.clock import get_clock
from core.event_calendar import get_calendar, display_upcoming_events
from core.notes import get_notes
from core.tasks import get_tasks
from core.workouts import get_workout
from common.data_operations import check_and_create_user_data
from common.data_operations import load_json_data, save_json_data

app = FastAPI(title="DayLog API", description="API for DayLog application")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class GeolocationInput(BaseModel):
    city_name: str

@app.get("/api/execute-all", response_model=Dict[str, Any])
async def execute_all_apis():
    """Execute all data collection APIs and return their combined results"""
    try:
        results = {}
        
        # Execute all data collection APIs
        try:
            garmin_data = get_garmin()
            results["garmin"] = garmin_data if garmin_data else {"message": "No Garmin data available"}
        except Exception as e:
            results["garmin"] = {"error": str(e), "status": "failed"}
            
        try:
            weather_data = get_weather()
            results["weather"] = weather_data if weather_data else {"message": "No weather data available"}
        except Exception as e:
            results["weather"] = {"error": str(e), "status": "failed"}
            
        try:
            geo_data = get_geolocation()
            results["geolocation"] = geo_data if geo_data else {"message": "No geolocation data available"}
        except Exception as e:
            results["geolocation"] = {"error": str(e), "status": "failed"}
            
        try:
            clock_data = get_clock()
            results["clock"] = clock_data if clock_data else {"message": "No clock data available"}
        except Exception as e:
            results["clock"] = {"error": str(e), "status": "failed"}
            
        try:
            withings_data = get_withings()
            results["withings"] = withings_data if withings_data else {"message": "No Withings data available"}
        except Exception as e:
            results["withings"] = {"error": str(e), "status": "failed"}
            
        try:
            notes_data = load_json_data("user_notes.json")
            results["notes"] = notes_data if notes_data else []
        except Exception as e:
            results["notes"] = {"error": str(e), "status": "failed"}
            
        try:
            tasks_data = load_json_data("user_tasks.json")
            results["tasks"] = tasks_data if tasks_data else []
        except Exception as e:
            results["tasks"] = {"error": str(e), "status": "failed"}
            
        try:
            workouts_data = load_json_data("user_workouts.json")
            results["workouts"] = workouts_data if workouts_data else []
        except Exception as e:
            results["workouts"] = {"error": str(e), "status": "failed"}
            
        try:
            calendar_data = load_json_data("user_calendar.json")
            results["calendar"] = calendar_data if calendar_data else []
        except Exception as e:
            results["calendar"] = {"error": str(e), "status": "failed"}
            
        # Add execution timestamp and status
        results["execution_time"] = datetime.now().isoformat()
        results["status"] = "completed"
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Direct data reading endpoints (no menus)
@app.get("/api/notes", response_model=List[Dict[str, Any]])
async def api_read_notes():
    """Get all notes directly from the JSON file"""
    try:
        data = load_json_data("user_notes.json")
        return data if data else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks", response_model=List[Dict[str, Any]])
async def api_read_tasks():
    """Get all tasks directly from the JSON file"""
    try:
        data = load_json_data("user_tasks.json")
        return data if data else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/workouts", response_model=List[Dict[str, Any]])
async def api_read_workouts():
    """Get all workouts directly from the JSON file"""
    try:
        data = load_json_data("user_workouts.json")
        if not data:
            return []
        
        # Format the workouts data for better readability
        formatted_workouts = []
        for workout in data:
            formatted_workout = {
                "workout_name": workout.get("workout_name", ""),
                "exercises": []
            }
            
            for exercise in workout.get("exercises", []):
                formatted_exercise = {
                    "name": exercise.get("exercise", ""),
                    "sets": []
                }
                
                for set_data in exercise.get("sets", []):
                    formatted_exercise["sets"].append({
                        "set_number": set_data.get("set", 0),
                        "reps": set_data.get("reps", 0)
                    })
                
                formatted_workout["exercises"].append(formatted_exercise)
            
            formatted_workouts.append(formatted_workout)
        
        return formatted_workouts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/calendar", response_model=List[Dict[str, Any]])
async def api_read_calendar():
    """Get all calendar events directly from the JSON file"""
    try:
        data = load_json_data("user_calendar.json")
        return data if data else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/withings", response_model=Dict[str, Any])
async def api_read_withings():
    """Get Withings data directly from user_data.json"""
    try:
        data = load_json_data("user_data.json")
        return data.get("Withings", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/garmin", response_model=Dict[str, Any])
async def api_read_garmin():
    """Get Garmin data directly from user_data.json"""
    try:
        data = load_json_data("user_data.json")
        return data.get("Garmin", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather", response_model=Dict[str, Any])
async def api_read_weather():
    """Get weather data directly from user_data.json"""
    try:
        data = load_json_data("user_data.json")
        return data.get("Weather", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clock", response_model=Dict[str, Any])
async def api_read_clock():
    """Get clock data directly from user_data.json"""
    try:
        return get_clock()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/geolocation", response_model=Dict[str, Any])
async def api_read_geolocation():
    """Get geolocation data directly from user_data.json"""
    try:
        data = load_json_data("user_data.json")
        return data.get("Geolocation", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/all", response_model=Dict[str, Any])
async def api_read_all():
    """Get all data directly from user_data.json"""
    try:
        data = load_json_data("user_data.json")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Original endpoints (keeping the menu functionality)
@app.get("/")
async def root():
    """Get information about all available APIs"""
    return {
        "message": "Welcome to DayLog API",
        "available_endpoints": {
            "direct_data_endpoints": {
                "/api/notes": "Get all notes directly from JSON file",
                "/api/tasks": "Get all tasks directly from JSON file",
                "/api/workouts": "Get all workouts directly from JSON file",
                "/api/calendar": "Get all calendar events directly from JSON file",
                "/api/withings": "Get Withings data directly from user_data.json",
                "/api/garmin": "Get Garmin data directly from user_data.json",
                "/api/weather": "Get weather data directly from user_data.json",
                "/api/clock": "Get clock data directly from user_data.json",
                "/api/geolocation": "Get geolocation data directly from user_data.json",
                "/api/all": "Get all data directly from user_data.json"
            },
            "interactive_endpoints": {
                "/garmin": "Get Garmin data with menu interaction",
                "/weather": "Get weather data with menu interaction",
                "/geolocation": "Get geolocation data with menu interaction",
                "/geolocation/set": "Set geolocation by city name (POST)",
                "/clock": "Get clock data with menu interaction",
                "/withings": "Get Withings data with menu interaction",
                "/notes": "Get notes with menu interaction",
                "/tasks": "Get tasks with menu interaction",
                "/calendar": "Get calendar data with menu interaction",
                "/calendar/upcoming": "Get upcoming calendar events",
                "/workouts": "Get workout data with menu interaction"
            },
            "documentation": {
                "/docs": "Interactive API documentation (Swagger UI)",
                "/redoc": "Alternative API documentation (ReDoc)"
            }
        }
    }

@app.get("/garmin")
async def garmin_endpoint():
    try:
        data = get_garmin()
        if data is None:
            raise HTTPException(status_code=404, detail="No Garmin data available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather")
async def weather_endpoint():
    try:
        data = get_weather()
        if data is None:
            raise HTTPException(status_code=404, detail="No weather data available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/geolocation")
async def geolocation_endpoint():
    try:
        data = get_geolocation()
        if data is None:
            raise HTTPException(status_code=404, detail="No geolocation data available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/geolocation/set")
async def set_geolocation(geolocation: GeolocationInput):
    try:
        data = get_geolocation(geolocation.city_name)
        if data is None:
            raise HTTPException(status_code=404, detail=f"Could not find coordinates for {geolocation.city_name}")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/clock")
async def clock_endpoint():
    try:
        data = get_clock()
        if data is None:
            raise HTTPException(status_code=404, detail="No clock data available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/withings")
async def withings_endpoint():
    try:
        data = get_withings()
        if data is None:
            raise HTTPException(status_code=404, detail="No Withings data available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes")
async def notes_endpoint():
    try:
        data = get_notes()
        if data is None:
            raise HTTPException(status_code=404, detail="No notes available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks")
async def tasks_endpoint():
    try:
        data = get_tasks()
        if data is None:
            raise HTTPException(status_code=404, detail="No tasks available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/calendar")
async def calendar_endpoint():
    try:
        data = get_calendar()
        if data is None:
            raise HTTPException(status_code=404, detail="No calendar data available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/calendar/upcoming")
async def upcoming_events_endpoint(days: int = 7):
    try:
        data = display_upcoming_events(days)
        if not data:
            raise HTTPException(status_code=404, detail="No upcoming events available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workouts")
async def workouts_endpoint():
    try:
        data = get_workout()
        if data is None:
            raise HTTPException(status_code=404, detail="No workout data available")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
