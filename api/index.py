from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ❌ Maine wo HTML wala 'read_root' function HATA DIYA hai.
# Kyunki HTML ab 'public' folder se Vercel khud dikhayega.

@app.get("/api/lookup")
def lookup_number(number: str = Query(..., description="Phone number")):
    try:
        parsed_number = phonenumbers.parse(number, None)
        is_valid = phonenumbers.is_valid_number(parsed_number)
        
        if not is_valid:
            return {"status": "error", "message": "Invalid Number Format ❌"}

        country = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)
        formatted = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        
        # Link banane ke liye clean number
        clean_num = formatted.replace(" ", "").replace("+", "")

        return {
            "status": "success",
            "data": {
                "Number": formatted,
                "Status": "Active ✅",
                "Region": country,
                "Carrier": service_provider,
                "Timezone": ", ".join(time_zones),
                "clean_num": clean_num
            }
        }

    except Exception as e:
        return {"status": "error", "message": "Server Error"}
        
