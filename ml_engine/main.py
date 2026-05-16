from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn
import pandas as pd

app = FastAPI(title="TransitCore Carbon API")
print("🧠 Loading Random Forest Model...")
model = joblib.load('traffic_model.joblib')


class RideRequest(BaseModel):
    hour: int
    is_weekend: int
    is_raining: int
    distance_km: float
    vehicle_type: str  


EMISSION_FACTORS = {
    "Petrol": 0.165,
    "Diesel": 0.167,
    "EV": 0.050
}


@app.post("/calculate_savings")
def calculate_savings(ride: RideRequest):
    
    input_features = pd.DataFrame([{
        'hour': ride.hour,
        'is_weekend': ride.is_weekend,
        'is_raining': ride.is_raining
    }])
    
   
    predicted_multiplier = model.predict(input_features)[0]
    
   
    base_factor = EMISSION_FACTORS.get(ride.vehicle_type, 0.165)
    
 
    base_co2 = ride.distance_km * base_factor
    
    
    actual_co2_per_car = base_co2 * predicted_multiplier
    
   
    two_solo_cabs = actual_co2_per_car * 2
    detour_penalty=1.15
    one_shared_cab = actual_co2_per_car * detour_penalty
    total_saved = two_solo_cabs - one_shared_cab
    
    return {
        "status": "success",
        "predicted_traffic_multiplier": round(predicted_multiplier, 2),
        "actual_co2_emitted_kg": round(one_shared_cab, 2),
        "total_co2_saved_kg": round(total_saved, 2)
    }

# Run the server
if __name__ == "__main__":
    print(" Starting TransitCore API on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)