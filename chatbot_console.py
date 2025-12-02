"""
Standalone Console Chatbot - No Flask Required!
================================================
Perfect for running in online terminals.

Usage:
    py chatbot_console.py
    
Or in PowerShell:
    .\chatbot_console.py

Features:
- Classes: Multiple OOP classes
- Inheritance: Base classes with derived classes  
- Polymorphism: Same interface, different implementations
- Functions: Utility functions and methods
- Proper Comments: Comprehensive documentation
"""

from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional
from abc import ABC, abstractmethod


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_input(user_input: str) -> bool:
    """Validate user input."""
    return bool(user_input and user_input.strip())


def format_confidence(confidence: float) -> str:
    """Format confidence score as percentage."""
    return f"{confidence * 100:.1f}%"


def print_separator(char: str = "=", length: int = 60) -> None:
    """Print a separator line."""
    print(char * length)


# ============================================================================
# BASE CLASSES (Abstract Base Classes for Polymorphism)
# ============================================================================

class MatcherStrategy(ABC):
    """
    Abstract base class for different matching strategies.
    Uses Strategy Pattern for polymorphism.
    """
    
    @abstractmethod
    def calculate_score(self, user_input: str, faq_item: Dict) -> float:
        """Calculate similarity score between user input and FAQ item."""
        pass


class ResponseHandler(ABC):
    """
    Abstract base class for different response handling strategies.
    Uses Template Method Pattern.
    """
    
    @abstractmethod
    def format_response(self, response_data: Dict) -> Dict:
        """Format the response data for output."""
        pass


# ============================================================================
# CONCRETE MATCHER CLASSES (Inheritance)
# ============================================================================

class SimilarityMatcher(MatcherStrategy):
    """
    Matches FAQs based on string similarity.
    Inherits from MatcherStrategy base class.
    """
    
    def calculate_score(self, user_input: str, faq_item: Dict) -> float:
        """Calculate similarity score based on question text similarity."""
        question = faq_item.get("question", "")
        return SequenceMatcher(None, user_input.lower(), question.lower()).ratio()


class KeywordMatcher(MatcherStrategy):
    """
    Matches FAQs based on keyword matching.
    Inherits from MatcherStrategy base class.
    Demonstrates inheritance and polymorphism.
    """
    
    def calculate_score(self, user_input: str, faq_item: Dict) -> float:
        """Calculate similarity score based on keyword matches."""
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
        """Initialize hybrid matcher with weights."""
        # Composition: Contains instances of other matchers
        self.similarity_matcher = SimilarityMatcher()
        self.keyword_matcher = KeywordMatcher()
        self.similarity_weight = similarity_weight
        self.keyword_weight = keyword_weight
    
    def calculate_score(self, user_input: str, faq_item: Dict) -> float:
        """
        Calculate combined score using multiple matchers.
        Demonstrates polymorphism - same interface, different implementation.
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

class ConsoleResponseHandler(ResponseHandler):
    """
    Formats responses for console/terminal output.
    Inherits from ResponseHandler base class.
    """
    
    def format_response(self, response_data: Dict) -> Dict:
        """Format response for console display."""
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
    """
    
    def format_response(self, response_data: Dict) -> Dict:
        """Format error response."""
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
    """
    
    # Class-level constants
    HELPLINE_MESSAGE = (
        "I'm not trained to answer this question yet. "
        "Please visit https://www.comsats.edu.pk/ for more details."
    )
    CONFIDENCE_THRESHOLD = 0.4
    
    def __init__(self, faq_data: List[Dict], matcher: MatcherStrategy):
        """Initialize FAQ database with data and matcher strategy."""
        self.faq_data = faq_data
        # Polymorphism: accepts any MatcherStrategy subclass
        self.matcher = matcher
    
    def find_best_match(self, user_input: str) -> Tuple[Optional[Dict], float]:
        """Find the best matching FAQ for user input."""
        best_match = None
        best_score = 0.0
        
        for faq_item in self.faq_data:
            # Polymorphism: works with any MatcherStrategy subclass
            score = self.matcher.calculate_score(user_input, faq_item)
            
            if score > best_score:
                best_score = score
                best_match = faq_item
        
        return best_match, best_score
    
    def get_response(self, user_input: str) -> Dict:
        """Get response for user input."""
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
        """Get list of all FAQ questions."""
        return [faq["question"] for faq in self.faq_data]


# ============================================================================
# CHATBOT API CLASS
# ============================================================================

class ChatbotAPI:
    """
    Main API class that coordinates FAQ database and response handlers.
    Demonstrates composition and dependency injection.
    """
    
    def __init__(self, faq_database: FAQDatabase, response_handler: ResponseHandler):
        """Initialize API with database and response handler."""
        self.faq_database = faq_database
        # Polymorphism: accepts any ResponseHandler subclass
        self.response_handler = response_handler
    
    def process_query(self, user_input: str) -> Dict:
        """Process user query and return formatted response."""
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
# FAQ DATA
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
# MAIN CONSOLE INTERFACE
# ============================================================================

def main():
    """Main console interface."""
    # Create matcher and database
    matcher = HybridMatcher(similarity_weight=0.7, keyword_weight=0.3)
    faq_db = FAQDatabase(FAQ_DATA, matcher)
    response_handler = ConsoleResponseHandler()
    chatbot = ChatbotAPI(faq_db, response_handler)
    
    print_separator()
    print("  🚁 Drone FAQ Chatbot - Console Mode")
    print_separator()
    print("\nOOP Features:")
    print("  ✓ Classes: Multiple classes with clear responsibilities")
    print("  ✓ Inheritance: Base classes with derived classes")
    print("  ✓ Polymorphism: Same interface, different implementations")
    print("  ✓ Functions: Utility functions and methods")
    print("  ✓ Comments: Comprehensive documentation")
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


if __name__ == "__main__":
    main()

