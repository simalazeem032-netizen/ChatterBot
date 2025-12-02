# app.py
from flask import Flask, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Initialize Flask app
app = Flask(__name__)

# Initialize chatbot
bot = ChatBot(
    "IoT_Foresight_Bot",
    logic_adapters=["chatterbot.logic.BestMatch"]
)

# Train chatbot with predefined Q&A
trainer = ListTrainer(bot)

faq_data = [
    ("What is the IoT Innovation Centre?", "The IoT Innovation Centre focuses on IoT research, prototyping, and training."),
    ("What is the Foresight Microfactory?", "The Foresight Microfactory is a small-scale production facility for IoT products."),
    ("What is the Embedded Systems Design Lab?", "The lab is used for embedded hardware and software design in phases I, II, and III."),
    ("Who are your partners?", "We partner with Quectel, Innovista, and Foresight."),
    ("Do you work on commercial products?", "Yes, we develop commercial IoT and embedded solutions."),
    ("Do you work on defence products?", "Yes, we also develop defence-grade IoT products."),
    ("Where can I find more information?", "You can visit our website or contact us directly."),
    ("What is your website?", "Our website is www.innovista.pk."),
]

for conv in faq_data:
    trainer.train(conv)

# Set up a route to interact with the bot via HTTP
@app.route("/chat", methods=["GET"])
def chat():
    user_input = request.args.get("user_input")
    if user_input:
        response = bot.get_response(user_input)
        # Check for confidence and return appropriate response
        if response.confidence < 0.5:
            return jsonify({"response": "Sorry, I don't have an answer for that. Please visit our website or contact support."})
        else:
            return jsonify({"response": str(response)})
    else:
        return jsonify({"response": "Please ask a question."})

if __name__ == "__main__":
    app.run(debug=True)
