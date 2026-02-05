from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 YEH HAI FIX: Root URL par HTML dikhana
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Saath wali index.html file ko padh kar return karega
    with open(os.path.join(os.path.dirname(__file__), "index.html"), "r") as f:
        return f.read()

@app.get("/api/lookup")
def lookup_number(number: str = Query(..., description="Phone number")):
    try:
        parsed_number = phonenumbers.parse(number, None)
        is_valid = phonenumbers.is_valid_number(parsed_number)
        
        if not is_valid:
            return {"status": "error", "message": "Invalid Number Format"}

        country = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)
        formatted = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        return {
            "status": "success",
            "data": {
                "Number": formatted,
                "Status": "Active / Valid",
                "Region": country,
                "Carrier": service_provider,
                "Timezone": ", ".join(time_zones)
            }
        }

    except Exception as e:
        return {"status": "error", "message": "Could not parse number"}
        
