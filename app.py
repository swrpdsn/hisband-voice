# app.py - FastAPI AI Call Engine
from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv
from supabase import create_client, Client
import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import json

# Load secrets from .env file
load_dotenv()

# --- Supabase Setup ---
SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY: str = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# --- Exotel Setup ---
EXOTEL_SID = os.environ.get("EXOTEL_SID")
EXOTEL_TOKEN = os.environ.get("EXOTEL_TOKEN")
EXOTEL_CALLER_ID = os.environ.get("EXOTEL_CALLER_ID")

# --- Nari Labs Setup ---
NARI_LABS_API_KEY = os.environ.get("NARI_LABS_API_KEY")
NARI_LABS_BASE_URL = os.environ.get("NARI_LABS_BASE_URL")

# --- FastAPI App ---
app = FastAPI()
# This will be replaced by your actual deployed URL (e.g., from Render/Fly.io)
LIVE_API_URL = os.environ.get("LIVE_API_URL", "http://127.0.0.1:8000") 

# =======================================================
# 0. NARI LABS TTS Function (Simplified for MVP)
# =======================================================
def get_nari_audio_url(text_to_speak: str) -> str | None:
    """Gets an MP3 URL from Nari Labs for the given text."""
    try:
        # NOTE: Using a simplified request assuming Nari returns a direct URL
        headers = {
            'Authorization': f'Bearer {NARI_LABS_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            "text": text_to_speak,
            "voice": "hindi_female_v1" # Or a preferred Indian voice
        }
        
        # NOTE: You need to replace the URL below with the exact Nari API endpoint
        response = requests.post(NARI_LABS_BASE_URL, headers=headers, json=payload)
        response.raise_for_status() 
        
        # Assuming Nari returns a JSON with a direct 'url' to the audio file
        audio_url = response.json().get('url') 
        return audio_url

    except requests.exceptions.RequestException as e:
        print(f"Nari Labs API Error: {e}")
        # Fallback: Return None to use basic TTS later
        return None

# =======================================================
# 1. CALL TRIGGER (Called by Dashboard)
# =======================================================
@app.post("/api/call/{lead_id}")
async def trigger_call(lead_id: str):
    """Endpoint called by the dashboard's 'Call' button."""
    try:
        # 1. Fetch Lead Data
        lead_data = supabase.table('leads').select('phone, name, project').eq('id', lead_id).execute()
        
        if not lead_data.data:
            return {"status": "error", "message": "Lead not found"}, 404

        lead = lead_data.data[0]
        customer_phone = lead['phone']
        
        # 2. Exotel Outbound Call API Logic
        url = f"https://{EXOTEL_SID}:{EXOTEL_TOKEN}@api.exotel.com/v1/Accounts/{EXOTEL_SID}/Calls/connect"
        
        payload = {
            "From": EXOTEL_CALLER_ID,  
            "To": customer_phone,
            "CallerId": EXOTEL_CALLER_ID,
            # IMPORTANT: Exotel ko batao ki IVR script kahan se leni hai
            "Url": f"{LIVE_API_URL}/webhook/ivr/{lead_id}", 
            "CallType": "transfers"
        }
        
        # response = requests.post(url, data=payload) # NOTE: Un-comment this on deployment
        
        # 3. Log Call Trigger (Assuming call was triggered successfully)
        # NOTE: You need a 'calls' table for this, but for MVP, we just return success
        
        return {"status": "success", "message": f"Call triggered for {customer_phone}. Status updates coming soon."}

    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

# =======================================================
# 2. IVR FLOW (Called by Exotel to get the audio script)
# =======================================================
@app.post("/webhook/ivr/{lead_id}")
async def provide_ivr_script(lead_id: str, request: Request):
    """Exotel calls this immediately after connecting the call."""
    
    # 1. Fetch Lead Data for personalized script
    lead_data = supabase.table('leads').select('name, project').eq('id', lead_id).execute()
    lead = lead_data.data[0] if lead_data.data else {"name": "sir/madam", "project": "new"}

    # 2. The Hinglish Script
    tts_text = (
        f"Namaskar {lead['name']}! Hum aapke {lead['project']} project ke baare mein call kar rahe hain. "
        "Kya aap site visit ke liye agle 2 din mein available hain? "
        "Confirm booking ke liye 1 dabayein, ya callback ke liye 2 dabayein."
    )
    
    # 3. GET AUDIO URL (Nari Labs or Fallback)
    audio_url = get_nari_audio_url(tts_text)
    
    # 4. Create ExoML (Exotel's XML instruction)
    root = ET.Element("Response")
    
    if audio_url:
        # Play the high-quality Nari Labs audio
        ET.SubElement(root, "Play").text = audio_url 
    else:
        # Fallback to Exotel's basic TTS (needs language tag for Indian voice)
        ET.SubElement(root, "Say", language="en-IN").text = tts_text
    
    # Gather: Collect 1 digit input and send the result to the /webhook/status endpoint
    ET.SubElement(root, "Gather", 
                  numDigits="1", 
                  action=f"{LIVE_API_URL}/webhook/status/{lead_id}",
                  timeout="10").text = ""

    xml_response = ET.tostring(root, encoding='unicode')
    
    # Exotel expects XML response
    return PlainTextResponse(content=xml_response, media_type="application/xml")


# =======================================================
# 3. STATUS WEBHOOK (Called by Exotel when customer presses a key or call ends)
# =======================================================
@app.post("/webhook/status/{lead_id}")
async def handle_status_webhook(lead_id: str, Digits: str = Form(None), CallStatus: str = Form(None)):
    """Exotel calls this when a key is pressed (Digits) or when the call ends (CallStatus)."""
    
    new_status = 'contacted'
    
    if Digits == '1':
        new_status = 'booked'
    elif Digits == '2':
        new_status = 'callback'
    elif CallStatus == 'no-answer' or CallStatus == 'busy' or CallStatus == 'failed':
        new_status = 'pending' 

    # 1. Update Lead in Supabase
    supabase.table('leads').update({
        'status': new_status,
        'last_call_status': CallStatus,
        'dtmf_input': Digits,
        'last_called_at': datetime.now().isoformat()
    }).eq('id', lead_id).execute()

    # 2. Respond to Exotel to end the flow
    return PlainTextResponse(content="<Response><Hangup/></Response>", media_type="application/xml")