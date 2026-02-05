from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

app = FastAPI()

# 🔥 JUGGAD: HTML CODE PYTHON KE ANDAR HI HAI (Ab koi file error nahi aayega)
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSINT Scanner</title>
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <style>
        body { background: #0f172a; color: white; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 30px; border-radius: 20px; width: 350px; border: 1px solid #334155; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        h2 { margin-bottom: 5px; color: #38bdf8; }
        p { color: #94a3b8; font-size: 14px; margin-bottom: 20px; }
        
        .input-box { display: flex; gap: 10px; background: #0f172a; padding: 5px; border-radius: 10px; border: 1px solid #334155; }
        input { background: transparent; border: none; color: white; width: 100%; padding: 10px; outline: none; font-size: 16px; }
        button { background: #38bdf8; border: none; padding: 10px 15px; border-radius: 8px; cursor: pointer; color: #0f172a; font-weight: bold; transition: 0.2s; }
        button:hover { background: #0ea5e9; }

        .hidden { display: none; }
        #loader { margin-top: 15px; color: #38bdf8; font-size: 14px; }
        
        #result { margin-top: 20px; background: #0f172a; padding: 15px; border-radius: 10px; text-align: left; }
        .row { display: flex; justify-content: space-between; margin-bottom: 8px; border-bottom: 1px solid #334155; padding-bottom: 5px; font-size: 14px; }
        .row:last-child { border: none; }
        .row span { color: #94a3b8; }
        .row b { color: #e2e8f0; }

        .btn-tc { background: #2563eb; color: white; width: 100%; margin-top: 15px; padding: 10px; border-radius: 8px; font-size: 14px; }
        .error { color: #ef4444; margin-top: 10px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="card">
        <i class="ph ph-scan" style="font-size: 40px; color: #38bdf8;"></i>
        <h2>Number Scanner</h2>
        <p>Enter number with country code</p>

        <div class="input-box">
            <input type="text" id="phoneInput" placeholder="+91 9999999999">
            <button onclick="checkNumber()"><i class="ph ph-magnifying-glass"></i></button>
        </div>

        <p id="loader" class="hidden">Scanning Network...</p>

        <div id="result" class="hidden">
            <div id="grid"></div>
            <button onclick="openTruecaller()" class="btn-tc">Search Name on Truecaller 🆔</button>
        </div>
        
        <p id="error" class="error hidden"></p>
    </div>

    <script>
        let cleanNum = "";
        
        async function checkNumber() {
            const num = document.getElementById("phoneInput").value.trim();
            if(!num) return alert("Number daal bhai!");
            
            document.getElementById("loader").classList.remove("hidden");
            document.getElementById("result").classList.add("hidden");
            document.getElementById("error").classList.add("hidden");
            
            try {
                // API Call
                const res = await fetch(`/api/lookup?number=${encodeURIComponent(num)}`);
                const data = await res.json();
                
                if(data.status === "success") {
                    cleanNum = data.data.clean_num;
                    document.getElementById("grid").innerHTML = `
                        <div class="row"><span>Format:</span> <b>${data.data.Number}</b></div>
                        <div class="row"><span>Region:</span> <b>${data.data.Region}</b></div>
                        <div class="row"><span>Carrier:</span> <b>${data.data.Carrier}</b></div>
                        <div class="row"><span>Time:</span> <b>${data.data.Timezone}</b></div>
                    `;
                    document.getElementById("result").classList.remove("hidden");
                } else {
                    showError(data.message);
                }
            } catch(e) { 
                showError("Server Error! Check connection."); 
            } finally { 
                document.getElementById("loader").classList.add("hidden"); 
            }
        }

        function showError(msg) {
            document.getElementById("error").innerText = msg;
            document.getElementById("error").classList.remove("hidden");
        }

        function openTruecaller() { 
            if(cleanNum) window.open(`https://www.truecaller.com/search/in/${cleanNum}`, '_blank'); 
        }
    </script>
</body>
</html>
"""

# 🔥 Fix 1: Root URL (Homepage) par HTML dikhayega
@app.get("/", response_class=HTMLResponse)
async def home():
    return html_code

# 🔥 Fix 2: API Request Logic
@app.get("/api/lookup")
def lookup_number(number: str = Query(...)):
    try:
        parsed_number = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            return {"status": "error", "message": "Invalid Number ❌"}
        
        country = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")
        time_zones = timezone.time_zones_for_number(parsed_number)
        formatted = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        
        # Link ke liye clean number
        clean_num = formatted.replace(" ", "").replace("+", "")

        return {
            "status": "success",
            "data": {
                "Number": formatted,
                "Region": country,
                "Carrier": service_provider,
                "Timezone": ", ".join(time_zones),
                "clean_num": clean_num
            }
        }
    except: 
        return {"status": "error", "message": "Parsing Error"}
        
