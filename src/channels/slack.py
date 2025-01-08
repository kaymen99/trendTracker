import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_slack_message(message):
    client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
    try:
        response = client.chat_postMessage(
            channel=os.getenv("SLACK_CHANNEL"),
            text=message
        )
        return response["ok"], response["ts"]  # Return status and timestamp of message
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")
        return False, None

# Example usage
if __name__ == "__main__":
    slack_message = "Hello from Python!"

    success, timestamp = send_slack_message(slack_message)
    if success:
        print(f"Message sent successfully at {timestamp}")
    else:
        print("Failed to send message")
