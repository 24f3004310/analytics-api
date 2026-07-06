from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# --- Requirement: CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows the grader's domain to access it
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your specific credentials
ASSIGNED_API_KEY = "ak_x4kbk6j0x7kufrpyp358eky9"
YOUR_EMAIL = "24f3004310@ds.study.iitm.ac.in"  # Change this to your actual logged-in email!

# Define what an incoming event looks like
class Event(BaseModel):
    user: str
    amount: float
    ts: int

# Define the full request body structure
class AnalyticsRequest(BaseModel):
    events: List[Event]

@app.post("/analytics")
async def post_analytics(
    data: AnalyticsRequest, 
    x_api_key: Optional[str] = Header(None)  # Automatically looks for X-API-Key header
):
    # --- Requirement: Auth Check ---
    if x_api_key != ASSIGNED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or missing API key"
        )
    
    # --- Requirement: Aggregation Rules ---
    events = data.events
    total_events = len(events)
    
    unique_users_set = set()
    user_revenue_tracker = {}
    total_revenue = 0.0
    
    for event in events:
        unique_users_set.add(event.user)
        
        # Only process positive amounts
        if event.amount > 0:
            total_revenue += event.amount
            # Track revenue per user to find the top user
            user_revenue_tracker[event.user] = user_revenue_tracker.get(event.user, 0.0) + event.amount
            
    # Find the user with the maximum revenue (handling case where no one spent money safely)
    if user_revenue_tracker:
        top_user = max(user_revenue_tracker, key=user_revenue_tracker.get)
    else:
        top_user = "" 

    # --- Requirement: Expected JSON Response ---
    return {
        "email": YOUR_EMAIL,
        "total_events": total_events,
        "unique_users": len(unique_users_set),
        "revenue": total_revenue,
        "top_user": top_user
    }