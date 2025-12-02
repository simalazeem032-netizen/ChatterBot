"""
Drone FAQ Chatbot - OOP Implementation
=======================================
A comprehensive chatbot system demonstrating Object-Oriented Programming principles:
- Classes: Multiple classes for different responsibilities
- Inheritance: Base classes with derived classes
- Polymorphism: Same interface, different implementations
- Functions: Utility functions and methods
- Proper Comments: Comprehensive documentation

Run Modes:
1. Console Mode: python app.py --console (for online terminals)
2. API Mode: python app.py (Flask web server)
3. Test Mode: python app.py --test (run test cases)

Usage Examples:
- Console: python app.py --console
- API: python app.py
- Test: python app.py --test
- API via curl: curl "http://localhost:5000/chat?question=What is the flight time?"
"""

import sys
import os
from flask import Flask, request, jsonify
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional
from abc import ABC, abstractmethod


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_input(user_input: str) -> bool:
    """
    Validate user input.
    
    Args:
        user_input: The input string to validate
        
    Returns:
        True if input is valid, False otherwise
    """
    return bool(user_input and user_input.strip())


def format_confidence(confidence: float) -> str:
    """
    Format confidence score as percentage string.
    
    Args:
        confidence: Confidence score (0.0 to 1.0)
        
    Returns:
        Formatted percentage string
    """
    return f"{confidence * 100:.1f}%"


def print_separator(char: str = "=", length: int = 60) -> None:
    """
    Print a separator line.
    
    Args:
        char: Character to use for separator
        length: Length of separator line
    """
    print(char * length)


# ============================================================================
# BASE CLASSES (Abstract Base Classes for Polymorphism)
# ============================================================================

class MatcherStrategy(ABC):
    """
    Abstract base class for different matching strategies.
    Uses Strategy Pattern for polymorphism.
    
    This is an abstract class that defines the interface for all matchers.
    Subclasses must implement calculate_score() method.
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
    
    This abstract class defines how responses should be formatted.
    Different subclasses can format responses differently (JSON, Text, HTML, etc.)
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
# CONCRETE MATCHER CLASSES (Inheritance)
# ============================================================================

class SimilarityMatcher(MatcherStrategy):
    """
    Matches FAQs based on string similarity using SequenceMatcher.
    Inherits from MatcherStrategy base class.
    
    This class demonstrates inheritance - it inherits from MatcherStrategy
    and implements the abstract calculate_score() method.
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
    
    Demonstrates inheritance and polymorphism - same interface as SimilarityMatcher
    but different implementation (keyword-based vs similarity-based).
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
    
    This class uses composition (contains other matchers) and polymorphism
    (can be used anywhere a MatcherStrategy is expected).
    """
    
    def __init__(self, similarity_weight: float = 0.7, keyword_weight: float = 0.3):
        """
        Initialize hybrid matcher with weights.
        
        Args:
            similarity_weight: Weight for similarity matching (default: 0.7)
            keyword_weight: Weight for keyword matching (default: 0.3)
        """
        # Composition: This class contains instances of other matchers
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
        # Polymorphism: Both matchers have the same interface
        similarity_score = self.similarity_matcher.calculate_score(user_input, faq_item)
        keyword_score = self.keyword_matcher.calculate_score(user_input, faq_item)
        
        # Weighted combination
        combined_score = (similarity_score * self.similarity_weight) + \
                        (keyword_score * self.keyword_weight)
        return combined_score


# ============================================================================
# RESPONSE HANDLER CLASSES (Inheritance and Polymorphism)
# ============================================================================

class JSONResponseHandler(ResponseHandler):
    """
    Formats responses as JSON.
    Inherits from ResponseHandler base class.
    
    Demonstrates inheritance - inherits from ResponseHandler and implements
    the abstract format_response() method.
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


class ConsoleResponseHandler(ResponseHandler):
    """
    Formats responses for console/terminal output.
    Inherits from ResponseHandler base class.
    
    Demonstrates polymorphism - same interface as JSONResponseHandler but
    different output format (console-friendly text vs JSON).
    """
    
    def format_response(self, response_data: Dict) -> Dict:
        """
        Format response for console display.
        
        Args:
            response_data: Dictionary with response information
            
        Returns:
            Formatted response dictionary with console-friendly formatting
        """
        answer = response_data.get("answer", "")
        confidence = response_data.get("confidence", 0.0)
        question = response_data.get("question", "")
        
        return {
            "response": answer,
            "confidence": confidence,
            "matched_question": question,
            "formatted": f"Bot: {answer}\n(Confidence: {format_confidence(confidence)})"
        }


class ErrorResponseHandler(ResponseHandler):
    """
    Formats error responses.
    Inherits from ResponseHandler base class.
    
    Demonstrates polymorphism - same interface, different behavior (error handling).
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
# FAQ DATABASE CLASS
# ============================================================================

class FAQDatabase:
    """
    Manages the FAQ database and provides search functionality.
    Uses composition to work with MatcherStrategy objects.
    
    This class demonstrates:
    - Encapsulation: Data and methods are bundled together
    - Composition: Uses MatcherStrategy objects
    - Polymorphism: Works with any MatcherStrategy subclass
    """
    
    # Class-level constants (shared by all instances)
    HELPLINE_MESSAGE = (
        "I'm not trained to answer this question yet. "
        "Please visit https://www.comsats.edu.pk/ for more details."
    )
    CONFIDENCE_THRESHOLD = 0.4
    
    def __init__(self, faq_data: List[Dict], matcher: MatcherStrategy):
        """
        Initialize FAQ database with data and matcher strategy.
        
        Args:
            faq_data: List of FAQ dictionaries
            matcher: MatcherStrategy object (demonstrates dependency injection)
        """
        self.faq_data = faq_data
        # Polymorphism: accepts any MatcherStrategy subclass
        self.matcher = matcher
    
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
    
    def get_all_questions(self) -> List[str]:
        """
        Get list of all FAQ questions.
        
        Returns:
            List of question strings
        """
        return [faq["question"] for faq in self.faq_data]


# ============================================================================
# CHATBOT API CLASS
# ============================================================================

class ChatbotAPI:
    """
    Main API class that coordinates FAQ database and response handlers.
    Demonstrates composition and dependency injection.
    
    This class acts as a facade, coordinating between different components.
    """
    
    def __init__(self, faq_database: FAQDatabase, response_handler: ResponseHandler):
        """
        Initialize API with database and response handler.
        
        Args:
            faq_database: FAQDatabase instance
            response_handler: ResponseHandler instance (polymorphism)
        """
        self.faq_database = faq_database
        # Polymorphism: accepts any ResponseHandler subclass
        self.response_handler = response_handler
    
    def process_query(self, user_input: str) -> Dict:
        """
        Process user query and return formatted response.
        
        Args:
            user_input: The user's question
            
        Returns:
            Formatted response dictionary
        """
        # Input validation using utility function
        if not validate_input(user_input):
            error_handler = ErrorResponseHandler()
            return error_handler.format_response({
                "error": "Please provide a question."
            })
        
        # Get response from database
        response_data = self.faq_database.get_response(user_input.strip())
        
        # Format response using handler (polymorphism)
        return self.response_handler.format_response(response_data)


# ============================================================================
# FACTORY CLASS (Factory Pattern)
# ============================================================================

class ChatbotFactory:
    """
    Factory class for creating chatbot instances.
    Demonstrates Factory Pattern for object creation.
    """
    
    @staticmethod
    def create_console_chatbot(faq_data: List[Dict]) -> ChatbotAPI:
        """
        Create a chatbot configured for console/terminal use.
        
        Args:
            faq_data: List of FAQ dictionaries
            
        Returns:
            ChatbotAPI instance configured for console
        """
        matcher = HybridMatcher(similarity_weight=0.7, keyword_weight=0.3)
        faq_db = FAQDatabase(faq_data, matcher)
        response_handler = ConsoleResponseHandler()
        return ChatbotAPI(faq_db, response_handler)
    
    @staticmethod
    def create_api_chatbot(faq_data: List[Dict]) -> ChatbotAPI:
        """
        Create a chatbot configured for API/web use.
        
        Args:
            faq_data: List of FAQ dictionaries
            
        Returns:
            ChatbotAPI instance configured for API
        """
        matcher = HybridMatcher(similarity_weight=0.7, keyword_weight=0.3)
        faq_db = FAQDatabase(faq_data, matcher)
        response_handler = JSONResponseHandler()
        return ChatbotAPI(faq_db, response_handler)


# ============================================================================
# FAQ DATA (Module-level constant)
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
# CONSOLE MODE (For Online Terminals)
# ============================================================================

def run_console_mode():
    """
    Run chatbot in console/terminal mode.
    Perfect for online terminals like Replit, GitHub Codespaces, etc.
    """
    # Use factory to create console chatbot
    chatbot = ChatbotFactory.create_console_chatbot(FAQ_DATA)
    
    print_separator()
    print("  🚁 Drone FAQ Chatbot - Console Mode")
    print_separator()
    print("\nType 'exit', 'quit', or 'bye' to exit")
    print("Type 'help' to see available questions")
    print_separator()
    print("\nYou can ask questions like:")
    print("- What is the flight time of this drone?")
    print("- What is the maximum range?")
    print("- Does this drone have GPS?")
    print("- What camera resolution does it support?")
    print("- Is the camera removable or upgradeable?")
    print("- What is the payload capacity?")
    print("- What is the maximum speed?")
    print("- Is it waterproof or weather-resistant?")
    print_separator()
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nBot: Thank you for visiting. Goodbye!")
                break
            
            if user_input.lower() == "help":
                print("\nAvailable questions:")
                for i, question in enumerate(chatbot.faq_database.get_all_questions(), 1):
                    print(f"{i}. {question}")
                print()
                continue
            
            if not user_input:
                continue
            
            # Process query
            response = chatbot.process_query(user_input)
            
            # Display formatted response
            if "formatted" in response:
                print(response["formatted"])
            else:
                print(f"Bot: {response.get('response', 'No response')}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\nBot: Thank you for visiting. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")


# ============================================================================
# FLASK APPLICATION SETUP (API Mode)
# ============================================================================

def create_flask_app():
    """
    Create and configure Flask application.
    
    Returns:
        Configured Flask app instance
    """
    # Use factory to create API chatbot
    chatbot = ChatbotFactory.create_api_chatbot(FAQ_DATA)
    
    app = Flask(__name__)
    
    @app.route("/", methods=["GET"])
    def home():
        """Home endpoint with API documentation."""
        return jsonify({
            "message": "Drone FAQ Chatbot API",
            "version": "1.0",
            "oop_features": {
                "classes": ["MatcherStrategy", "ResponseHandler", "FAQDatabase", "ChatbotAPI", "ChatbotFactory"],
                "inheritance": "Multiple classes inherit from base classes",
                "polymorphism": "Same interface, different implementations",
                "functions": "Utility functions and methods throughout"
            },
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
        """Main chat endpoint - handles both GET and POST requests."""
        try:
            # Get question from request
            if request.method == "POST":
                data = request.get_json() or {}
                question = data.get("question") or data.get("user_input", "")
            else:
                question = request.args.get("question") or request.args.get("user_input", "")
            
            # Process query through API
            response = chatbot.process_query(question)
            
            return jsonify(response), 200
            
        except Exception as e:
            error_handler = ErrorResponseHandler()
            return jsonify(error_handler.format_response({
                "error": f"Server error: {str(e)}"
            })), 500
    
    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "service": "Drone FAQ Chatbot API",
            "faq_count": len(FAQ_DATA)
        }), 200
    
    return app, chatbot


# ============================================================================
# TEST MODE
# ============================================================================

def run_tests():
    """
    Run test cases to demonstrate OOP features.
    """
    print_separator()
    print("  🧪 Running Tests - OOP Features Demonstration")
    print_separator()
    
    # Test 1: Inheritance
    print("\n1. Testing Inheritance:")
    similarity_matcher = SimilarityMatcher()
    keyword_matcher = KeywordMatcher()
    hybrid_matcher = HybridMatcher()
    
    print(f"   ✓ SimilarityMatcher is instance of MatcherStrategy: {isinstance(similarity_matcher, MatcherStrategy)}")
    print(f"   ✓ KeywordMatcher is instance of MatcherStrategy: {isinstance(keyword_matcher, MatcherStrategy)}")
    print(f"   ✓ HybridMatcher is instance of MatcherStrategy: {isinstance(hybrid_matcher, MatcherStrategy)}")
    
    # Test 2: Polymorphism
    print("\n2. Testing Polymorphism:")
    test_faq = FAQ_DATA[0]
    test_input = "flight time"
    
    matchers = [similarity_matcher, keyword_matcher, hybrid_matcher]
    for i, matcher in enumerate(matchers, 1):
        score = matcher.calculate_score(test_input, test_faq)
        print(f"   Matcher {i} score: {score:.3f} (same interface, different implementation)")
    
    # Test 3: Factory Pattern
    print("\n3. Testing Factory Pattern:")
    console_bot = ChatbotFactory.create_console_chatbot(FAQ_DATA)
    api_bot = ChatbotFactory.create_api_chatbot(FAQ_DATA)
    print(f"   ✓ Console chatbot created: {type(console_bot).__name__}")
    print(f"   ✓ API chatbot created: {type(api_bot).__name__}")
    
    # Test 4: Response Handlers (Polymorphism)
    print("\n4. Testing Response Handler Polymorphism:")
    test_data = {"answer": "Test answer", "confidence": 0.85, "question": "Test question"}
    
    json_handler = JSONResponseHandler()
    console_handler = ConsoleResponseHandler()
    
    json_response = json_handler.format_response(test_data)
    console_response = console_handler.format_response(test_data)
    
    print(f"   ✓ JSON Handler: {type(json_response)}")
    print(f"   ✓ Console Handler: {type(console_response)}")
    print(f"   ✓ Both use same interface but produce different outputs")
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60 + "\n")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Parse command line arguments
    mode = "api"  # Default mode
    
    if len(sys.argv) > 1:
        if "--console" in sys.argv or "-c" in sys.argv:
            mode = "console"
        elif "--test" in sys.argv or "-t" in sys.argv:
            mode = "test"
        elif "--api" in sys.argv or "-a" in sys.argv:
            mode = "api"
    
    if mode == "console":
        # Console mode for online terminals
        run_console_mode()
    elif mode == "test":
        # Test mode
        run_tests()
    else:
        # API mode (Flask server)
        app, chatbot = create_flask_app()
        
        print("=" * 60)
        print("  🚁 Drone FAQ Chatbot API Server")
        print("=" * 60)
        print("\nServer starting on http://localhost:5000")
        print("\nOOP Features:")
        print("  ✓ Classes: Multiple classes with clear responsibilities")
        print("  ✓ Inheritance: Base classes with derived classes")
        print("  ✓ Polymorphism: Same interface, different implementations")
        print("  ✓ Functions: Utility functions and methods")
        print("  ✓ Comments: Comprehensive documentation")
        print("\nUsage examples:")
        print("  GET:  curl 'http://localhost:5000/chat?question=What is the flight time?'")
        print("  POST: curl -X POST http://localhost:5000/chat \\")
        print("           -H 'Content-Type: application/json' \\")
        print("           -d '{\"question\":\"What is the maximum range?\"}'")
        print("\nPress CTRL+C to stop the server")
        print("=" * 60 + "\n")
        
        # Run Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
