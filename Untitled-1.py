# iot_chatbot.py

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# -----------------------------
# 1. Create ChatBot instance
# -----------------------------
bot = ChatBot(
    "IoT_Foresight_Bot",
    logic_adapters=[
        "chatterbot.logic.BestMatch"
    ]
)

trainer = ListTrainer(bot)

# -----------------------------
# 2. Training data (8 Q&A)
# -----------------------------
faq_conversations = [
    [
        "What is the IoT Innovation Centre?",
        "The IoT Innovation Centre focuses on research, prototyping and training in Internet of Things and embedded systems."
    ],
    [
        "What is the Foresight Microfactory?",
        "The Foresight Microfactory is a small-scale production facility where we build and test electronics and IoT products."
    ],
    [
        "What is the Embedded Systems Design Lab?",
        "The Embedded Systems Design Lab is a lab space, organised in phases, used for designing and testing embedded hardware and software."
    ],
    [
        "Who are your partners?",
        "Our main partners are Quectel, Innovista and Foresight."
    ],
    [
        "Do you work on commercial products?",
        "Yes, we develop commercial IoT and embedded solutions for different industries."
    ],
    [
        "Do you work on defence products?",
        "Yes, we also work on defence-oriented embedded and IoT projects where required."
    ],
    [
        "Where can I find more information?",
        "For more information, please visit our website or contact us through the official contact channels."
    ],
    [
        "What is your website?",
        "Our website is: www.innovista.pk"
    ],
]

# Train the bot on each Q&A pair
for conv in faq_conversations:
    trainer.train(conv)

# -----------------------------
# 3. Console chat loop
# -----------------------------

HELPLINE_MESSAGE = (
    "I'm not trained to answer this question yet.\n"
    "Please visit our website www.innovista.pk or contact the support/helpline for more details."
)

def main():
    print("========================================")
    print("  IoT Innovation Centre FAQ Chatbot")
    print("  Type 'exit' to quit.")
    print("========================================\n")

    print("You can ask things like:")
    print("- What is the IoT Innovation Centre?")
    print("- What is the Foresight Microfactory?")
    print("- What is the Embedded Systems Design Lab?")
    print("- Who are your partners?")
    print("- Do you work on commercial products?")
    print("- Do you work on defence products?")
    print("- Where can I find more information?")
    print("- What is your website?\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Bot: Thank you for visiting. Goodbye!")
            break

        # Get response from ChatterBot
        response = bot.get_response(user_input)

        # Use confidence to decide: FAQ vs helpline
        # confidence is between 0 and 1
        if float(response.confidence) < 0.6:
            print("Bot:", HELPLINE_MESSAGE)
        else:
            print("Bot:", response)


if __name__ == "__main__":
    main()
