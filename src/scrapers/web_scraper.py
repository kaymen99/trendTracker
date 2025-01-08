import re
import html2text
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from src.utils import get_current_date, invoke_llm
from src.structured_outputs import HeadlinesList

def scrape_website_to_markdown(url: str) -> str:
    with sync_playwright() as p:
        # Launch a headless browser (switch to headful if needed)
        browser = p.firefox.launch(headless=True)  # Use `headless=False` for debugging
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
            java_script_enabled=True
        )
        
        # Open a new page
        page = context.new_page()
        
        # Navigate to the URL with a custom timeout (e.g., 60 seconds)
        page.goto(url, timeout=60000)  # Timeout in milliseconds
        
        # Wait for the page to load completely with a custom timeout
        page.wait_for_load_state("domcontentloaded", timeout=60000)
        
        # Get the page content
        page_content = page.content()
        
        # Close the browser
        browser.close()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_content, "html.parser")
    html_content = soup.prettify()

    # Convert HTML to Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_tables = True
    markdown_content = h.handle(html_content)

    # Clean up excess newlines
    markdown_content = re.sub(r"\n{3,}", "\n", markdown_content)
    markdown_content = markdown_content.strip()

    return markdown_content

def extract_key_headlines(source, content):
    SCRAPER_PROMPT = f"""
    Analyze the content of the scraped web page and return only today's AI or LLM related story or post headlines and links in JSON format from the page content. 
    They must be posted today: {get_current_date()}. 
    If there are no AI or LLM stories from today, return [].
    The source link is: {source}. 
    If a story link is not absolute, prepend ${source} to make it absolute. 
    Return only pure JSON in the specified format (no extra text, no markdown, no \`\`\`). 
    """
    
    output = invoke_llm(
        system_prompt=SCRAPER_PROMPT,
        user_message=content,
        model="gemini/gemini-1.5-flash",
        response_format=HeadlinesList,
        json_output=True
    )

    return output["headlines"]

def scrape_headlines_from_webpage(source):
    scraped_content = scrape_website_to_markdown(source)
    headlines = []
    if scraped_content:
        headlines = extract_key_headlines(source, scraped_content)
    
    return headlines