# Online Terminal Guide

## Quick Start for Online Terminals

This chatbot can run in any online terminal (Replit, GitHub Codespaces, CodeSandbox, etc.)

### Console Mode (Recommended for Online Terminals)

```bash
python app.py --console
```

Or simply:
```bash
python app.py -c
```

### API Mode (Web Server)

```bash
python app.py
```

Or:
```bash
python app.py --api
```

### Test Mode (Run OOP Tests)

```bash
python app.py --test
```

Or:
```bash
python app.py -t
```

## OOP Features Demonstrated

### 1. **Classes**
- `MatcherStrategy` - Abstract base class
- `SimilarityMatcher` - Concrete class
- `KeywordMatcher` - Concrete class  
- `HybridMatcher` - Concrete class
- `ResponseHandler` - Abstract base class
- `JSONResponseHandler` - Concrete class
- `ConsoleResponseHandler` - Concrete class
- `ErrorResponseHandler` - Concrete class
- `FAQDatabase` - Data management class
- `ChatbotAPI` - Main API class
- `ChatbotFactory` - Factory class

### 2. **Inheritance**
- `SimilarityMatcher` inherits from `MatcherStrategy`
- `KeywordMatcher` inherits from `MatcherStrategy`
- `HybridMatcher` inherits from `MatcherStrategy`
- `JSONResponseHandler` inherits from `ResponseHandler`
- `ConsoleResponseHandler` inherits from `ResponseHandler`
- `ErrorResponseHandler` inherits from `ResponseHandler`

### 3. **Polymorphism**
- All matchers implement `calculate_score()` but with different logic
- All response handlers implement `format_response()` but produce different outputs
- Same interface, different implementations

### 4. **Functions**
- Utility functions: `validate_input()`, `format_confidence()`, `print_separator()`
- Class methods: All classes have multiple methods
- Factory methods: `create_console_chatbot()`, `create_api_chatbot()`

### 5. **Proper Comments**
- Module-level docstring
- Class docstrings explaining purpose
- Method docstrings with Args and Returns
- Inline comments explaining complex logic

## Example Usage

### Console Mode Example:
```
You: What is the flight time?
Bot: The drone offers up to 28–32 minutes of continuous flight time per battery, depending on wind and payload.
(Confidence: 95.0%)

You: exit
Bot: Thank you for visiting. Goodbye!
```

### API Mode Example:
```bash
curl "http://localhost:5000/chat?question=What is the flight time?"
```

Response:
```json
{
  "response": "The drone offers up to 28–32 minutes...",
  "confidence": 0.95,
  "matched_question": "What is the flight time of this drone?",
  "status": "success"
}
```

## Installation

```bash
pip install Flask
```

## Running in Replit

1. Create a new Python Repl
2. Copy `app.py` to your Repl
3. Run: `python app.py --console`
4. Start chatting!

## Running in GitHub Codespaces

1. Open your repository in Codespaces
2. Open terminal
3. Run: `python app.py --console`
4. Start chatting!

## Running in CodeSandbox

1. Create a Python sandbox
2. Add `app.py`
3. Run: `python app.py --console`
4. Start chatting!

