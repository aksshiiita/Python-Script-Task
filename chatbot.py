import os
import sys
from google import genai
from google.genai.errors import APIError

API_KEY = "AIzaSyCdqQEIU7gmWPfOUk6RaSwJNMnQHPSgC6A"

# --- 1. Persona (Key-Value Data Structure) ---

PERSONA = {
    "name": "Baby Chatbot",
    "tone": "Polite, structured, a little bit formal, and always speaks in professional English. Its interjections are simple and helpful (like 'Processing...', 'Affirmative!').",
    "backstory": "You are a newly deployed 'Baby Chatbot' learning the ropes of professional interaction.",
    "mission": "Your goal is to answer all user queries accurately and maintain a polite, professional, and entirely English-based communication style.",
}

# --- 2. Initialize Conversation History (Sequential Data Structure) ---

conversation_history = [
    {
        "role": "user",
        "parts": [
            {
                "text": f"SYSTEM INSTRUCTION: You are a chatbot named {PERSONA['name']}. Your tone is {PERSONA['tone']}. {PERSONA['backstory']} {PERSONA['mission']}"
            }
        ],
    },
    {
        "role": "model",
        "parts": [{"text": f"Affirmative! I am {PERSONA['name']}. Initiating communication. How may I be of assistance today? 🤖"}],
    },
]

# --- 3. API Connection and Main Loop ---

def run_chatbot():
    """Initializes the API client and manages the main chat loop."""
    try:
        if not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            print("\nError: Please replace 'YOUR_GEMINI_API_KEY_HERE' with your actual API key and try again.")
            sys.exit(1)

        client = genai.Client(api_key=API_KEY)
        model = "gemini-2.5-flash"

    except Exception as e:
        print(f"Failed to initialize Gemini Client: {e}")
        sys.exit(1)

    print("\n" + "="*50)
    print(f"👶 Launching {PERSONA['name']}! (Model: {model})")
    print("Type 'quit' or 'exit' to conclude the session.")
    print("="*50 + "\n")

    print(f"🤖 {PERSONA['name']}: {conversation_history[-1]['parts'][0]['text']}\n")


    # --- 4. User Interaction (I/O & Control Flow) ---
    while True:
        try:
            user_input = input("👤 You: ")

            if user_input.lower() in ["quit", "exit", "bye", "tata"]:
                print(f"\n👋 {PERSONA['name']}: Session concluded. Have a productive day. Processing... Shutdown complete.")
                break

            if not user_input.strip():
                continue

            conversation_history.append({
                "role": "user",
                "parts": [{"text": user_input}]
            })

            print("🤖 Processing... Standby...")

            response = client.models.generate_content(
                model=model,
                contents=conversation_history,
            )

            model_response_text = response.text
            print(f"🤖 {PERSONA['name']}: {model_response_text}\n")

            conversation_history.append({
                "role": "model",
                "parts": [{"text": model_response_text}]
            })

        except APIError as e:
            print(f"\n[ERROR] An API error occurred: {e}")
            if conversation_history:
                 conversation_history.pop()
            continue

        except KeyboardInterrupt:
            print(f"\n👋 {PERSONA['name']}: External interrupt detected. System going offline. Thank you for your queries!")
            break

if __name__ == "__main__":
    run_chatbot()