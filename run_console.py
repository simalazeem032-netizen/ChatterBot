"""
Standalone console runner - No Flask required!
Run this directly: py run_console.py
Perfect for online terminals.
"""

# Import only what we need (no Flask)
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional
from abc import ABC, abstractmethod

# Import chatbot classes from app.py
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import chatbot components
try:
    from app import (
        FAQ_DATA,
        ChatbotFactory,
        print_separator,
        format_confidence
    )
except ImportError:
    print("Error: Could not import from app.py")
    print("Make sure app.py is in the same directory")
    sys.exit(1)


def main():
    """Main console interface."""
    # Create console chatbot using factory
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


if __name__ == "__main__":
    main()

