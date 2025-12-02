# iot_chatbot.py

from difflib import SequenceMatcher

# -----------------------------
# 1. FAQ Database
# -----------------------------
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

# -----------------------------
# 2. Simple matching function
# -----------------------------
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

# -----------------------------
# 3. Console chat loop
# -----------------------------

HELPLINE_MESSAGE = (
    "I'm not trained to answer this question yet.\n"
    "Please visit https://www.comsats.edu.pk/ for more details."
)

def main():
    print("========================================")
    print("  Drone FAQ Chatbot")
    print("  Type 'exit' to quit.")
    print("========================================\n")

    print("You can ask things like:")
    print("- What is the flight time of this drone?")
    print("- What is the maximum range?")
    print("- Does this drone have GPS?")
    print("- What camera resolution does it support?")
    print("- Is the camera removable or upgradeable?")
    print("- What is the payload capacity?")
    print("- What is the maximum speed?")
    print("- Is it waterproof or weather-resistant?\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Bot: Thank you for visiting. Goodbye!")
            break

        # Find best match
        match, confidence = find_best_match(user_input)

        # Use confidence threshold (similar to original 0.6)
        if match and confidence >= 0.4:
            print("Bot:", match["answer"])
        else:
            print("Bot:", HELPLINE_MESSAGE)


if __name__ == "__main__":
    main()
