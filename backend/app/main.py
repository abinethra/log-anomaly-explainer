import os
import json
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from google import genai
from app.models.database import get_db, Incident, LogEvent

app = FastAPI(title="Log Anomaly Explainer")

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else genai.Client()

class LogAnalysisRequest(BaseModel):
    logs: str

@app.get("/")
def root():
    return {"status": "Backend active and ready"}

@app.get("/incidents")
def get_incidents(db: Session = Depends(get_db)):
    return db.query(Incident).all()

@app.post("/analyze")
def analyze_logs(req: LogAnalysisRequest):
    prompt = f"""
You are a SOC Cybersecurity Analyst. Analyze the following system log entries:

{req.logs}

Return a valid JSON object with EXACTLY these keys:
- "severity": "LOW", "MEDIUM", or "HIGH"
- "summary": A 1-2 sentence executive summary of what happened.
- "likely_cause": Detailed technical root cause explanation.
- "suggested_actions": Bulleted mitigation steps for the admin.
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
