from difflib import SequenceMatcher
import json

# FAQ Database
faq_database = [
    {
        "question": "What is the flight time of this drone?",
        "answer": "The drone offers up to 28–32 minutes of continuous flight time per battery, depending on wind and payload.",
        "keywords": ["flight", "time", "battery", "minutes", "duration"]
    },
    {
        "question": "What is the maximum range?",
        "answer": "You can fly the drone up to 6–8 kilometers with a clear line of sight and minimal interference.",
        "keywords": ["maximum", "range", "distance", "kilometers", "km"]
    },
    {
        "question": "Does this drone have GPS?",
        "answer": "Yes, it features built-in GPS + GLONASS for stable hovering, accurate positioning, and automated flight modes.",
        "keywords": ["gps", "glonass", "positioning", "navigation"]
    },
    {
        "question": "What camera resolution does it support?",
        "answer": "The drone comes with a 4K Ultra HD camera (30 fps) with a 3-axis gimbal for smooth and stable footage.",
        "keywords": ["camera", "resolution", "4k", "ultra", "hd", "gimbal", "fps"]
    },
    {
        "question": "Is the camera removable or upgradeable?",
        "answer": "Yes, the camera is removable, and there are upgrade options that are fully compatible with the drone's gimbal system.",
        "keywords": ["camera", "removable", "upgradeable", "upgrade", "compatible"]
    },
    {
        "question": "What is the payload capacity?",
        "answer": "The drone can safely carry up to 500–700 grams without affecting stability.",
        "keywords": ["payload", "capacity", "weight", "carry", "grams"]
    },
    {
        "question": "What is the maximum speed?",
        "answer": "The drone reaches speeds of up to 60 km/h (in Sport Mode).",
        "keywords": ["maximum", "speed", "km/h", "sport", "mode"]
    },
    {
        "question": "Is it waterproof or weather-resistant?",
        "answer": "The drone is weather-resistant (IP43), meaning it can handle light rain and dust—but it is not fully waterproof.",
        "keywords": ["waterproof", "weather", "resistant", "rain", "dust", "ip43"]
    },
]

HELPLINE_MESSAGE = (
    "I'm not trained to answer this question yet. "
    "Please visit https://www.comsats.edu.pk/ for more details."
)

def similarity(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_best_match(user_input):
    """Find the best matching FAQ based on question similarity and keywords."""
    user_lower = user_input.lower()
    best_match = None
    best_score = 0.0
    
    for faq in faq_database:
        # Check question similarity
        question_score = similarity(user_input, faq["question"])
        
        # Check keyword matches
        keyword_score = sum(1 for keyword in faq["keywords"] if keyword in user_lower)
        keyword_score = keyword_score / len(faq["keywords"]) if faq["keywords"] else 0
        
        # Combined score (weighted)
        combined_score = (question_score * 0.7) + (keyword_score * 0.3)
        
        if combined_score > best_score:
            best_score = combined_score
            best_match = faq
    
    return best_match, best_score

def handler(event, context):
    """Netlify serverless function handler."""
    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    }

    # Handle preflight OPTIONS request
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    try:
        # Parse request body
        if event.get('body'):
            body = json.loads(event['body'])
            user_input = body.get('user_input', '').strip()
        else:
            user_input = event.get('queryStringParameters', {}).get('user_input', '').strip()

        if not user_input:
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({"response": "Please ask a question."})
            }

        # Find best match
        match, confidence = find_best_match(user_input)

        # Use confidence threshold
        if match and confidence >= 0.4:
            response_text = match["answer"]
        else:
            response_text = HELPLINE_MESSAGE

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({"response": response_text})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"response": f"Error: {str(e)}"})
        }


