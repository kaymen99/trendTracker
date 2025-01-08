from typing import List
from pydantic import BaseModel, Field


class Headline(BaseModel):
    """
    Represents an individual Headline with a headline, link, and date posted.
    """
    headline: str = Field(..., description="The headline or title of the Headline.")
    link: str = Field(..., description="The URL linking to the full Headline.")
    description: str = Field(..., description="A short description of the headline (optional)")
    date_posted: str = Field(..., description="The date the Headline was posted, in YYYY-MM-DD format.")


class HeadlinesList(BaseModel):
    """
    Represents a response containing a list of headlines.
    """
    headlines: List[Headline] = Field(..., description="A list of headlines, where each Headline includes a headline, link, and posting date.")


class Trend(BaseModel):
    link: str = Field(..., description="The URL linking to the full story")
    description: str = Field(..., description="A short title/description of the story")


class Trends(BaseModel):
    interestingTrends: List[Trend] = Field(..., description="A list of interesting trends.")