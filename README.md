# Trend Tracker ⚡️

**Discover trending content from top companies in AI and LLMs, along with insights from your preferred content creators on Twitter or YouTube — all customized for you.**

Trend Collector gathers and analyzes content from leading company websites, influential Twitter figures, and popular YouTube channels. Stay ahead with real-time notifications via Slack or Telegram, making this a must-have tool for creators, marketers, and industry professionals.

- **Save time** by automating data collection and analysis
- **Stay informed** with updates from your preferred content sources
- **Act fast** with instant notifications about trends and opportunities

This project was inspired by [trendFinder using FireCrawl](https://github.com/ericciarla/trendFinder)

---

## How It Works

1. **Data Collection** 📥
   - Scrapes news and updates directly from top company websites using Playwright.
   - Monitors tweets from influential figures on Twitter/X.
   - Tracks content from known YouTube channels.
   - Allows users to add custom companies, creators, or channels for personalized monitoring.

2. **AI Analysis** 🤖
   - Processes collected data with GPT-4o, Gemini or LLAMA3.3.
   - Identify emerging trends and relevant topics.
   - Craft tailored trend insights.

3. **Notification System** 📢
   - Sends notifications via Slack or Telegram when significant trends are detected.

---

## Features

- 🤖 **AI-powered trend detection**
- 🔍 **Website monitoring with Playwright**
- 🎥 **Monitor your loved YouTube channels**
- 🔤 **Follow influential Twitter**
- 💬 **Notifications on Slack or Telegram**

---

## Tech Stack

- **Runtime**: Python 3.10+
- **AI/LLM**: Litellm for multi-llm access (OpenAI, Gemini, Groq,...)
- **Data Sources**:
  - Website scraping with Playwright
  - Twitter/X API
  - YouTube Google Data API
- **Notifications**:
  - Slack Webhooks
  - Telegram Bot API

---

## Prerequisites

- Python (3.10 or higher)
- Virtual environment manager (e.g., `venv`, `conda`)
- API keys for required services

---

## Environment Variables

Copy `.env.example` to `.env` and configure the following variables:

```
# Required: API key from an LLM providers
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key

# Required if monitoring Twitter/X trends
X_API_BEARER_TOKEN=your_twitter_api_bearer_token_here

# Required for YouTube channel monitoring
YOUTUBE_API_KEY=your_youtube_api_key_here

# Optional: Slack bot token and channel name for sending slack messages
SLACK_BOT_TOKEN=your_slack_token
SLACK_CHANNEL=your_slack_channel

# Optional: Telegram Bot API token and chat ID
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

---

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kaymen99/trendTracker.git
   cd trendTracker
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application:**
   ```bash
   python main.py
   ```

---

## Project Structure

```
trend-collector/
├── src/
│   ├── channels/        # Notification handlers via Slack or Telegram
│   ├── scrapers/        # Scraping and data collection logic
│   ├── constants.py     # File containing all sources links
│   └── trend_tracker.py # Main class for content scraping and AI analysis  
├── .env.example         # Environment variables template
├── requirements.txt     # Python dependencies
└── main.py              # Application entry point
```

---

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

---

### Contact

If you have any questions or suggestions, feel free to contact me at `aymenMir1001@gmail.com`.

