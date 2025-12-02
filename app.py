"""
Drone FAQ Chatbot API
=====================
A RESTful API for answering drone-related FAQ questions.
Uses Object-Oriented Programming principles: classes, inheritance, and polymorphism.

Run from terminal: python app.py
Access via: http://localhost:5000/chat?question=YOUR_QUESTION
Or use curl: curl "http://localhost:5000/chat?question=What is the flight time?"
"""

from flask import Flask, request, jsonify
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional
from abc import ABC, abstractmethod


# ============================================================================
# Base Classes (Abstract Base Classes for Polymorphism)
# ============================================================================

class MatcherStrategy(ABC):
    """
    Abstract base class for different matching strategies.
    Uses Strategy Pattern for polymorphism.
    """
    
    @abstractmethod
    def calculate_score(self, user_input: str, faq_item: Dict) -> float:
        """
        Calculate similarity score between user input and FAQ item.
        
        Args:
            user_input: The user's question
            faq_item: A dictionary containing question, answer, and keywords
            
        Returns:
            A float score between 0.0 and 1.0
        """
        pass


class ResponseHandler(ABC):
    """
    Abstract base class for different response handling strategies.
    Uses Template Method Pattern.
    """
    
    @abstractmethod
    def format_response(self, response_data: Dict) -> Dict:
        """
        Format the response data for output.
        
        Args:
            response_data: Dictionary containing response information
            
        Returns:
            Formatted response dictionary
        """
        pass


# ============================================================================
# Concrete Matcher Classes (Inheritance)
# ============================================================================

class SimilarityMatcher(MatcherStrategy):
    """
    Matches FAQs based on string similarity using SequenceMatcher.
    Inherits from MatcherStrategy base class.
    """
    
    def calculate_score(self, user_input: str, faq_item: Dict) -> float:
        """
        Calculate similarity score based on question text similarity.
        
        Args:
            user_input: The user's question
            faq_item: FAQ dictionary with 'question' key
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        question = faq_item.get("question", "")
        return SequenceMatcher(None, user_input.lower(), question.lower()).ratio()


class KeywordMatcher(MatcherStrategy):
    """
    Matches FAQs based on keyword matching.
    Inherits from MatcherStrategy base class.
    Demonstrates inheritance and polymorphism.
    """
    
    def calculate_score(self, user_input: str, faq_item: Dict) -> float:
        """
        Calculate similarity score based on keyword matches.
        
        Args:
            user_input: The user's question
            faq_item: FAQ dictionary with 'keywords' key
            
        Returns:
            Keyword match score (0.0 to 1.0)
        """
        keywords = faq_item.get("keywords", [])
        if not keywords:
            return 0.0
        
        user_lower = user_input.lower()
        matches = sum(1 for keyword in keywords if keyword in user_lower)
        return matches / len(keywords) if keywords else 0.0


class HybridMatcher(MatcherStrategy):
    """
    Combines multiple matching strategies using weighted scores.
    Demonstrates composition and polymorphism.
    Inherits from MatcherStrategy base class.
    """
    
    def __init__(self, similarity_weight: float = 0.7, keyword_weight: float = 0.3):
        """
        Initialize hybrid matcher with weights.
        
        Args:
            similarity_weight: Weight for similarity matching (default: 0.7)
            keyword_weight: Weight for keyword matching (default: 0.3)
        """
        self.similarity_matcher = SimilarityMatcher()
        self.keyword_matcher = KeywordMatcher()
        self.similarity_weight = similarity_weight
        self.keyword_weight = keyword_weight
    
    def calculate_score(self, user_input: str, faq_item: Dict) -> float:
        """
        Calculate combined score using multiple matchers.
        Demonstrates polymorphism - same interface, different implementation.
        
        Args:
            user_input: The user's question
            faq_item: FAQ dictionary
            
        Returns:
            Combined weighted score (0.0 to 1.0)
        """
        similarity_score = self.similarity_matcher.calculate_score(user_input, faq_item)
        keyword_score = self.keyword_matcher.calculate_score(user_input, faq_item)
        
        combined_score = (similarity_score * self.similarity_weight) + \
                        (keyword_score * self.keyword_weight)
        return combined_score


# ============================================================================
# Response Handler Classes (Inheritance and Polymorphism)
# ============================================================================

class JSONResponseHandler(ResponseHandler):
    """
    Formats responses as JSON.
    Inherits from ResponseHandler base class.
    """
    
    def format_response(self, response_data: Dict) -> Dict:
        """
        Format response as JSON dictionary.
        
        Args:
            response_data: Dictionary with 'answer', 'confidence', 'question' keys
            
        Returns:
            Formatted JSON response
        """
        return {
            "response": response_data.get("answer", ""),
            "confidence": round(response_data.get("confidence", 0.0), 2),
            "matched_question": response_data.get("question", ""),
            "status": "success"
        }


class ErrorResponseHandler(ResponseHandler):
    """
    Formats error responses.
    Inherits from ResponseHandler base class.
    Demonstrates polymorphism - same interface, different behavior.
    """
    
    def format_response(self, response_data: Dict) -> Dict:
        """
        Format error response.
        
        Args:
            response_data: Dictionary with 'error' key
            
        Returns:
            Formatted error response
        """
        return {
            "response": response_data.get("error", "An error occurred"),
            "status": "error"
        }


# ============================================================================
# FAQ Database Class
# ============================================================================

class FAQDatabase:
    """
    Manages the FAQ database and provides search functionality.
    Uses composition to work with MatcherStrategy objects.
    """
    
    # Class-level constant
    HELPLINE_MESSAGE = (
        "I'm not trained to answer this question yet. "
        "Please visit https://www.comsats.edu.pk/ for more details."
    )
    
    # Class-level constant for confidence threshold
    CONFIDENCE_THRESHOLD = 0.4
    
    def __init__(self, faq_data: List[Dict], matcher: MatcherStrategy):
        """
        Initialize FAQ database with data and matcher strategy.
        
        Args:
            faq_data: List of FAQ dictionaries
            matcher: MatcherStrategy object (demonstrates dependency injection)
        """
        self.faq_data = faq_data
        self.matcher = matcher  # Polymorphism: accepts any MatcherStrategy subclass
    
    def find_best_match(self, user_input: str) -> Tuple[Optional[Dict], float]:
        """
        Find the best matching FAQ for user input.
        
        Args:
            user_input: The user's question
            
        Returns:
            Tuple of (best_match_dict, confidence_score)
        """
        best_match = None
        best_score = 0.0
        
        for faq_item in self.faq_data:
            # Polymorphism: matcher.calculate_score() works with any MatcherStrategy subclass
            score = self.matcher.calculate_score(user_input, faq_item)
            
            if score > best_score:
                best_score = score
                best_match = faq_item
        
        return best_match, best_score
    
    def get_response(self, user_input: str) -> Dict:
        """
        Get response for user input.
        
        Args:
            user_input: The user's question
            
        Returns:
            Dictionary with answer and metadata
        """
        match, confidence = self.find_best_match(user_input)
        
        if match and confidence >= self.CONFIDENCE_THRESHOLD:
            return {
                "answer": match["answer"],
                "confidence": confidence,
                "question": match["question"]
            }
        else:
            return {
                "answer": self.HELPLINE_MESSAGE,
                "confidence": confidence,
                "question": None
            }


# ============================================================================
# Chatbot API Class
# ============================================================================

class ChatbotAPI:
    """
    Main API class that coordinates FAQ database and response handlers.
    Demonstrates composition and dependency injection.
    """
    
    def __init__(self, faq_database: FAQDatabase, response_handler: ResponseHandler):
        """
        Initialize API with database and response handler.
        
        Args:
            faq_database: FAQDatabase instance
            response_handler: ResponseHandler instance (polymorphism)
        """
        self.faq_database = faq_database
        self.response_handler = response_handler  # Polymorphism: accepts any ResponseHandler subclass
    
    def process_query(self, user_input: str) -> Dict:
        """
        Process user query and return formatted response.
        
        Args:
            user_input: The user's question
            
        Returns:
            Formatted response dictionary
        """
        if not user_input or not user_input.strip():
            return self.response_handler.format_response({
                "error": "Please provide a question."
            })
        
        # Get response from database
        response_data = self.faq_database.get_response(user_input.strip())
        
        # Format response using handler (polymorphism)
        return self.response_handler.format_response(response_data)


# ============================================================================
# FAQ Data (Class-level constant)
# ============================================================================

FAQ_DATA = [
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


# ============================================================================
# Flask Application Setup
# ============================================================================

# Initialize components using dependency injection
matcher = HybridMatcher(similarity_weight=0.7, keyword_weight=0.3)
faq_db = FAQDatabase(FAQ_DATA, matcher)
response_handler = JSONResponseHandler()
chatbot_api = ChatbotAPI(faq_db, response_handler)

# Create Flask app
app = Flask(__name__)


# ============================================================================
# API Routes
# ============================================================================

@app.route("/", methods=["GET"])
def home():
    """
    Home endpoint with API documentation.
    """
    return jsonify({
        "message": "Drone FAQ Chatbot API",
        "version": "1.0",
        "endpoints": {
            "/chat": "GET or POST - Ask a question",
            "/health": "GET - Health check"
        },
        "usage": {
            "GET": "curl 'http://localhost:5000/chat?question=What is the flight time?'",
            "POST": "curl -X POST http://localhost:5000/chat -H 'Content-Type: application/json' -d '{\"question\":\"What is the flight time?\"}'"
        }
    })


@app.route("/chat", methods=["GET", "POST"])
def chat():
    """
    Main chat endpoint - handles both GET and POST requests.
    Accessible via terminal using curl or wget.
    """
    try:
        # Get question from request (supports both GET and POST)
        if request.method == "POST":
            data = request.get_json() or {}
            question = data.get("question") or data.get("user_input", "")
        else:
            question = request.args.get("question") or request.args.get("user_input", "")
        
        # Process query through API
        response = chatbot_api.process_query(question)
        
        return jsonify(response), 200
        
    except Exception as e:
        error_handler = ErrorResponseHandler()
        return jsonify(error_handler.format_response({
            "error": f"Server error: {str(e)}"
        })), 500


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    """
    return jsonify({
        "status": "healthy",
        "service": "Drone FAQ Chatbot API",
        "faq_count": len(FAQ_DATA)
    }), 200


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Drone FAQ Chatbot API Server")
    print("=" * 60)
    print("\nServer starting on http://localhost:5000")
    print("\nUsage examples:")
    print("  GET:  curl 'http://localhost:5000/chat?question=What is the flight time?'")
    print("  POST: curl -X POST http://localhost:5000/chat \\")
    print("           -H 'Content-Type: application/json' \\")
    print("           -d '{\"question\":\"What is the maximum range?\"}'")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60 + "\n")
    
    # Run Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
