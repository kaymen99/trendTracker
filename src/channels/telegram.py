import os
import requests

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    
    payload = {
        "chat_id": os.getenv("TELEGRAM_CHAT_ID"),
        "text": message
    }
    
    try:
        response = requests.post(url, json=payload)
        response_data = response.json()
        if response_data["ok"]:
            return response_data["ok"], response_data["result"]["message_id"]
        else:
            print(f"Error sending message: {response_data['description']}")
            return False, None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return False, None

# Example usage
if __name__ == "__main__":
    telegram_message = "Hello from Python (Telegram)!"

    success, message_id = send_telegram_message(telegram_message)
    if success:
        print(f"Message sent successfully with ID {message_id}")
    else:
        print("Failed to send message")
