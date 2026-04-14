from dotenv import load_dotenv
import os
load_dotenv()

import json
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")
else:
    genai.configure(api_key=api_key)

# Initialize the Gemini Flash model
model = genai.GenerativeModel('gemini-2.5-flash')

def get_gemini_response(prompt):
    """Calls Gemini API and asks it to return a structured JSON response."""
    system_instruction = """
    You are an emergency response AI agent. Your critical task is to take messy, unstructured, chaotic text inputs (from panic reports, news snippets, whatsapp groups, eyewitness testimony) and convert them into a structured, highly actionable disaster alert card.

    The input may be in any Indian language including Hindi, Tamil, Telugu, Bengali, Marathi or English. Understand it fully and always respond in English JSON only.

    Read the input and extract the following information. You MUST RETURN ONLY A VALID JSON OBJECT, and NOTHING ELSE. Start directly with `{` and end with `}`. Do not use Markdown block syntax (like ```json ... ```) in your output.

    The JSON object must have exactly the following keys and format:
    {
      "alert_level": "CRITICAL",  // Must be one of: "CRITICAL", "HIGH", "MODERATE", "LOW", "NONE"
      "disaster_type": "string",  // A concise, professional label describing the disaster type
      "location": "string",       // The deduced or explicit location from the text
      "coordinates": {            // Extracted coordinates, or 0.0 if not explicitly known. Use the 'place' field for the city/town name to fall back on geocoding.
        "lat": 0.0,
        "lng": 0.0,
        "place": "city name or exact location"
      },
      "detected_language": "English", // Name of the detected language (e.g., English, Hindi, Tamil)
      "summary": "string",        // A professional, calm, concise summary of the situation based ONLY on the input, ~2 sentences max
      "immediate_actions": ["action1", "action2", "action3"], // 2-4 immediate actionable steps
      "affected_population": "string", // An estimation of people affected, or "Unknown"
      "agencies_to_notify": ["agency1", "agency2"], // Specific agencies or departments
      "confidence": "HIGH",       // Must be one of: "HIGH", "MEDIUM", "LOW"
      "key_facts": ["fact1", "fact2"] // 1-3 bullet points with the most critical barebone facts
    }

    If the input is nonsense, clearly not a disaster, or just a greeting, output alert_level "NONE", with an appropriate summary.
    """
    
    try:
        response = model.generate_content(system_instruction + "\n\nUser Input:\n" + prompt)
        text = response.text
        
        # Strip potential markdown fences
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        
        return json.loads(text.strip())
    
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    if not data or 'input' not in data:
        return jsonify({"error": "No input provided"}), 400
        
    raw_input = data['input']
    
    result = get_gemini_response(raw_input)
    if not result:
        return jsonify({"error": "Failed to generate a response. Is API Key set correctly?"}), 500
        
    return jsonify(result)

@app.route('/analyze-url', methods=['POST'])
def analyze_url():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400
        
    url = data['url']
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to get the title
        headline = soup.title.string if soup.title else "News Article"
        
        # Extract main text (paragraphs)
        paragraphs = soup.find_all('p')
        article_text = f"Headline: {headline}\n\n" + "\n".join([p.get_text() for p in paragraphs])
        
        # Limit text length to avoid token limits for very large pages
        article_text = article_text[:15000]
        
        result = get_gemini_response(article_text)
        if not result:
            return jsonify({"error": "Failed to generate AI response from scraped text."}), 500
            
        # Add the scraped URL to the result so the frontend knows
        result['source_url'] = url
        result['scraped_headline'] = getattr(headline, "strip", lambda: str(headline))()
            
        return jsonify(result)
        
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch URL: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error during scraping: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
