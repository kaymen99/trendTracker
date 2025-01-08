import asyncio
from src.trend_tracker import TrendTracker
from dotenv import load_dotenv

load_dotenv()

# Create an instance of TrendTracker
trend_tracker = TrendTracker(communication_channel="slack") # can use "telegram"

async def main():
    sources = trend_tracker.get_relevant_sources()
    scraped_headlines = await trend_tracker.scrape_sources_async(sources)
    message = await trend_tracker.analyze_and_get_trends(scraped_headlines)
    await trend_tracker.send_message(message)

if __name__ == "__main__":
    asyncio.run(main())


