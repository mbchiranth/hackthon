# DisasterBridge

DisasterBridge acts as a universal bridge between chaotic human intent and complex systems during crises. It takes messy, unstructured disaster-related text input (such as panicked eyewitness reports, broken news snippets, or chaotic WhatsApp messages) and instantly converts them into structured, verified, and actionable disaster alerts using Google Gemini 1.5 Flash.

By bringing immediate clarity to chaos, DisasterBridge accelerates emergency response efforts, helping agencies prioritize effectively and quite literally saving lives.

## Features
- Intelligently extracts: disaster type, alert level, action points, and agencies to notify.
- Returns output in a strict structured format.
- Uses **Google Gemini 1.5 Flash** for high speed, low-latency reasoning.
- Dark, functional industrial UI optimized for emergency operation centers.

## Example

**Messy Input:**
> "omg the water is rising so fast here in downtown miami by 5th st. people are trapped on their roofs!!! we need boats now! also power lines are down it looks crazy maybe a fire starting too?"

**Structured Output:**
- **Alert Level:** CRITICAL (Color coded Red)
- **Disaster Type:** Flash Flood & Potential Electrical Fire
- **Location:** Downtown Miami, FL (near 5th St)
- **Actions:** 1. Dispatch water rescue boats. 2. Cut power grid to affected area. 3. Initiate emergency roof evacuations.
- **Agencies:** Coast Guard, Fire Department, Local EMS, Power Grid Operators
- **Confidence Level:** HIGH

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/disaster-bridge.git
cd disaster-bridge
```

### 2. Install dependencies
Ensure you have Python 3.8+ installed.
```bash
pip install -r requirements.txt
```

### 3. Set up your Gemini API Key
1. Get an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Edit the `.env` file and replace `your_api_key_here` with your actual Gemini API key.

### 4. Run the app
```bash
python app.py
```
Then navigate to `http://127.0.0.1:5000` in your web browser.

## Built With
* Python & Flask
* Google Gemini API (`google-generativeai`)
* Vanilla HTML / CSS / JS (No external bloated frontend frameworks)
