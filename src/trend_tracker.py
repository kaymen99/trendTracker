import asyncio
from src.channels.slack import send_slack_message
from src.channels.telegram import send_telegram_message 
from src.scrapers.web_scraper import scrape_headlines_from_webpage
from src.scrapers.twitter import scrape_tweets_from_user
from src.scrapers.youtube import scrape_youtube_channel
from src.utils import invoke_llm, get_current_date
from src.constants import MAIN_SOURCES 
from src.structured_outputs import Trends

class TrendTracker:
    def __init__(self, communication_channel):
        self.communication_channel = communication_channel # "slack" or "telegram"
        
    def get_relevant_sources(self):
        return MAIN_SOURCES

    async def scrape_sources_async(self, sources: list) -> list:
        tasks = [self.scrape_source_async(source) for source in sources]
        results = await asyncio.gather(*tasks)

        all_headlines = []
        for headlines in results:
            all_headlines.extend(headlines)
            
        all_headlines = self.format_headlines(all_headlines)

        return all_headlines
    
    async def scrape_source_async(self, source: str) -> list:
        if "x.com" in source:
            return await asyncio.to_thread(scrape_tweets_from_user, source)
        elif "youtube.com" in source:
            return await asyncio.to_thread(scrape_youtube_channel, source)
        else:
            return await asyncio.to_thread(scrape_headlines_from_webpage, source)

    async def analyze_and_get_trends(self, scraped_headlines):
        print(f"Generating a post draft with raw stories ({len(scraped_headlines)} characters)...")

        try:
            system_prompt = (
                "You are an AI Trend Analyst. Your primary role is to analyze recent headlines and news from various sources in the AI space, including Twitter, YouTube, and popular AI companies. "
                "You will identify emerging trends, noteworthy launches, and interesting examples within this information. "
                "You must respond with valid JSON that matches the provided schema without any extra keys."
            )

            user_message = (
                f"Analyze the following collection of recent headlines and news from Twitter, YouTube, and prominent AI companies:\n\n{scraped_headlines}\n\n"
                f"Identify and extract noteworthy items that indicate emerging trends, significant launches, or interesting applications within the AI and LLM domain.\n"
                f"Strive to identify the most noteworthy items and for each return a descriptive headline and the associated link."
            )

            response = invoke_llm(
                system_prompt=system_prompt,
                user_message=user_message,
                model='gemini/gemini-2.0-flash-exp',
                response_format=Trends
            )

            header = f"🚀 AI and LLM Trends for {get_current_date()}\n\n"
            draft_post = header + '\n\n'.join(
                f"• {trend.description}\n  {trend.link}"
                for trend in response.interestingTrends
            )

            return draft_post

        except Exception as error:
            print("Error generating draft post", error)
            return "Error generating draft post."

    async def send_message(self, message):
        # Async message sending logic based on communication channel
        if self.communication_channel == "slack":
            # Async Slack message sending logic if API allows
            send_slack_message(message)  
        elif self.communication_channel == "telegram":
            # Async Telegram message sending logic if API allows
            send_telegram_message(message)
            
    def format_headlines(self, headlines):
        """
        Formats a list of headlines into a single string.
        """
        formatted_string = ""
        for headline in headlines:
            if headline:
                formatted_string += f"- **{headline['headline']}**\n"
                formatted_string += f"  {headline['link']}\n"
                if "description" in headline:
                    formatted_string += f"{headline['description']}\n" 
                formatted_string += "\n"

        return formatted_string