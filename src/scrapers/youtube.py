import re
import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta


def extract_channel_name_from_url(url):
    """
    Extracts the YouTube channel name from a given channel URL.
    """
    print(url)
    match = re.search(r"@([A-Za-z0-9_-]+)", url)
    if match:
        return match.group(1)
    return None

def get_channel_id(channel_name):
    """
    Resolves a YouTube channel name to its channel ID.

    :param api_key: Your YouTube Data API key
    :param channel_name: YouTube channel name (as seen in the URL)
    :return: Channel ID (or None if not found)
    """
    youtube = build('youtube', 'v3', developerKey=os.getenv("YOUTUBE_API_TOKEN"))
    try:
        search_response = youtube.search().list(
            part="snippet",
            q=channel_name,
            type="channel",
            maxResults=1
        ).execute()
        return search_response['items'][0]['id']['channelId']
    except Exception as e:
        print(f"Error resolving channel name '{channel_name}': {e}")
        return None

def scrape_youtube_channel(channel_url, max_results=5):
    """
    Fetches videos published in the last 24 hours for the provided YouTube channel.
    """
    youtube = build('youtube', 'v3', developerKey=os.getenv("YOUTUBE_API_TOKEN"))
    
    # Calculate timestamp for 24 hours ago
    now = datetime.now()
    time_24_hours_ago = now - timedelta(hours=24)

    channel_name = extract_channel_name_from_url(channel_url)
    channel_id = get_channel_id(os.getenv("YOUTUBE_API_TOKEN"), channel_name)
    if not channel_id:
        print(f"Skipping channel '{channel_name}' due to missing ID.")

    try:
        # Fetch the channel's uploads playlist ID
        channel_response = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()

        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Fetch recent videos from the uploads playlist
        playlist_response = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=max_results
        ).execute()

        # Extract video details
        videos = []
        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            publish_date = item['snippet']['publishedAt']
            publish_datetime = datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%SZ")

            # Check if the video was published in the last 24 hours
            if publish_datetime >= time_24_hours_ago:
                videos.append({
                    'link': f"https://www.youtube.com/watch?v={video_id}",
                    'headline': title,
                    'description': description,
                    'date_posted': publish_date
                })

    except Exception as e:
        print(f"Error fetching videos for channel '{channel_name}': {e}")

    return videos

# Usage Example
if __name__ == "__main__":
    channel_url = "https://www.youtube.com/@TheAiGrid"

    videos = scrape_youtube_channel(channel_url)
    for video in videos:
        print(f" - {video['title']} ({video['publish_date']})")
        print(f" - Link: {video['link']}")
        print(f" - Description:\n{video['description']}")
