from textbase import bot, Message
from textbase.models import OpenAI
from typing import List
import googletrans  # For lang translation

# Load your OpenAI API key
OpenAI.api_key = ""

# Initialize the Google Translate API
translator = googletrans.Translator()

# Dummy product db
product_database = {
    "1": {"name": "Product A", "category": "Electronics"},
    "2": {"name": "Product B", "category": "Clothing"},
    # Add more product entries
}

# Function to recommend products based on user preferences
def recommend_products(user_preferences):
    category = user_preferences.get("category", None)
    recommendations = []

    for product_id, product_info in product_database.items():
        if category is None or product_info["category"] == category:
            recommendations.append(product_info["name"])

    return recommendations

# Function to translate text
def translate_text(text, target_language="en"):
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function to track user's mood
def track_mood(user_message, user_state):
    mood = user_message.lower()
    user_state["mood"] = mood
    return f"Your mood has been updated to {mood}."

@bot()
def on_message(message_history: List[Message], state: dict = None):
    # Generate GPT-3.5 Turbo response
    bot_response = OpenAI.generate(
        system_prompt=SYSTEM_PROMPT,
        message_history=message_history, # Assuming history is the list of user messages
        model="gpt-3.5-turbo",
    )

    user_message = message_history[-1].content.lower()

    if "recommend products" in user_message:
        # Recommend products based on user preferences
        user_preferences = state.get("user_preferences", {})
        recommended_products = recommend_products(user_preferences)
        bot_response = f"Here are some product recommendations: {', '.join(recommended_products)}"

    elif "translate to" in user_message:
        # Translate text to the specified language
        target_language = user_message.split("translate to ")[-1]
        text_to_translate = message_history[-2].content  # Assuming the text to translate is in the previous message
        translated_text = translate_text(text_to_translate, target_language)
        bot_response = f"Translation to {target_language}: {translated_text}"

    elif "track my mood" in user_message:
        # Track the user's mood
        mood_tracking_response = track_mood(user_message, state)
        bot_response = mood_tracking_response

    else:
        # Generate GPT-3.5 Turbo response
        bot_response = OpenAI.generate(
            system_prompt=SYSTEM_PROMPT,
            message_history=message_history,  # Assuming history is the list of user messages
            model="gpt-3.5-turbo",
        )

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }
