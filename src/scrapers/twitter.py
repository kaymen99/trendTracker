import os
import re
import requests
from datetime import datetime, timedelta


async def scrape_tweets_from_user(source):
    tweets_list = []
    username_match = re.search(r"x\.com/([^/]+)", source)
    if username_match:
        username = username_match.group(1)

        # Build the search query for tweets
        query = f"from:{username} has:media -is:retweet -is:reply"
        encoded_query = query.replace(" ", "%20")

        # Get tweets from the last 24 hours
        start_time = (datetime.now() - timedelta(hours=24)).isoformat() + "Z"
        encoded_start_time = start_time.replace(" ", "%20")

        # x.com API URL
        api_url = f"https://api.x.com/2/tweets/search/recent?query={encoded_query}&max_results=10&start_time={encoded_start_time}"

        # Fetch recent tweets from the Twitter API
        headers = {
            "Authorization": f"Bearer {os.getenv('X_API_BEARER_TOKEN')}"
        }

        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch tweets for {username}: {response.reason}")

        tweets = response.json()
        if tweets.get("meta", {}).get("result_count", 0) == 0:
            print(f"No tweets found for username {username}.")
        elif isinstance(tweets.get("data"), list):
            print(f"Tweets found from username {username}")
            headlines = [
                {
                    "headline": tweet["text"],
                    "link": f"https://x.com/i/status/{tweet['id']}",
                    "date_posted": start_time,
                }
                for tweet in tweets["data"]
            ]
            tweets_list.extend(headlines)
        else:
            print("Expected tweets.data to be an array:", tweets.get("data"))

    return tweets_list

# Example usage
if __name__ == "__main__":
    sources = "https://x.com/OpenAIDevs"
    result = scrape_tweets_from_user(sources)
    print(result)
    


