# API Usage Guide

## Running the Server

From terminal:
```bash
cd ProjectChaterBot
python app.py
```

The server will start on `http://localhost:5000`

## Accessing via Terminal

### Using curl (GET request):
```bash
curl "http://localhost:5000/chat?question=What is the flight time?"
```

### Using curl (POST request):
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What is the maximum range?"}'
```

### Using wget (GET request):
```bash
wget -qO- "http://localhost:5000/chat?question=Does this drone have GPS?"
```

### Using PowerShell (Windows):
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/chat?question=What is the payload capacity?"
```

## API Endpoints

### 1. Home/Info
```bash
curl http://localhost:5000/
```

### 2. Chat Endpoint
```bash
curl "http://localhost:5000/chat?question=YOUR_QUESTION"
```

### 3. Health Check
```bash
curl http://localhost:5000/health
```

## Example Responses

**Success Response:**
```json
{
  "response": "The drone offers up to 28–32 minutes of continuous flight time per battery...",
  "confidence": 0.95,
  "matched_question": "What is the flight time of this drone?",
  "status": "success"
}
```

**Unknown Question Response:**
```json
{
  "response": "I'm not trained to answer this question yet. Please visit https://www.comsats.edu.pk/ for more details.",
  "confidence": 0.25,
  "matched_question": null,
  "status": "success"
}
```

## OOP Features Used

1. **Classes**: `MatcherStrategy`, `ResponseHandler`, `FAQDatabase`, `ChatbotAPI`
2. **Inheritance**: `SimilarityMatcher`, `KeywordMatcher`, `HybridMatcher` inherit from `MatcherStrategy`
3. **Polymorphism**: Different matchers and handlers can be swapped without changing code
4. **Abstract Base Classes**: `ABC` used for defining interfaces
5. **Composition**: Classes work together through dependency injection

