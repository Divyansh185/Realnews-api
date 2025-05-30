# # from fastapi import FastAPI, HTTPException
# # from pydantic import BaseModel
# # import datetime
# # import httpx
# # import os
# # from dotenv import load_dotenv
# # from typing import List, Optional

# # # Load environment variables from .env file
# # load_dotenv()

# # # --- Define Data Structures for the "Cleaned" Response ---
# # class CleanedNewsArticle(BaseModel):
# #     source: Optional[str] = None
# #     headline: str # Changed from 'title' to 'headline' for clarity if you prefer
# #     summary: Optional[str] = None # Changed from 'description'
# #     date: Optional[str] = None # Changed from 'published_at'

# # class AccountCleanedNewsResponse(BaseModel):
# #     account_name: str
# #     retrieved_at: str
# #     news_items: List[CleanedNewsArticle] # Changed field name from 'articles'
# #     search_query_used: str
# #     data_source_comment: str

# # # --- Initialize the FastAPI app ---
# # app = FastAPI(
# #     title="Account External Cleaned News API (POC - NewsAPI.org)",
# #     description="Provides cleaned news articles related to an account name using NewsAPI.org.",
# #     version="0.3.2", # Version updated
# # )

# # # --- Get API Key ---
# # NEWSAPI_API_KEY = os.getenv("NEWSAPI_KEY")

# # if not NEWSAPI_API_KEY:
# #     print("ERROR: NEWSAPI_KEY not found. Please ensure it's set in your .env file.")

# # # --- API Endpoint: /account_external_data ---
# # @app.get("/account_external_data", response_model=AccountCleanedNewsResponse)
# # async def get_account_news_data(account_name: str):
# #     if not NEWSAPI_API_KEY:
# #         raise HTTPException(status_code=500, detail="API Key for news service is not configured.")

# #     if account_name.lower() == "sony":
# #         search_query = f'"{account_name} Corporation" OR "{account_name} Group" OR "{account_name} business" OR "{account_name} financials" OR "{account_name} strategy" OR "{account_name} innovations" NOT (PlayStation OR PS5 OR PS4 OR "Spider-Man" OR movie OR music OR gaming)'
# #     else:
# #         search_query = f'"{account_name}" AND (business OR corporate OR financial OR product OR partnership OR strategy)'

# #     newsapi_url = "https://newsapi.org/v2/everything"
    
# #     params = {
# #         "q": search_query,
# #         "apiKey": NEWSAPI_API_KEY,
# #         "pageSize": 7,
# #         "sortBy": "relevancy",
# #         "language": "en"
# #     }

# #     cleaned_news_items = []
# #     data_source_comment = "News data from NewsAPI.org."
# #     actual_query_sent = params["q"] 

# #     try:
# #         async with httpx.AsyncClient() as client:
# #             response = await client.get(newsapi_url, params=params, timeout=10.0)
# #             response.raise_for_status()
        
# #         news_data = response.json()

# #         if news_data.get("status") == "ok":
# #             for article_data in news_data.get("articles", []):
# #                 item = CleanedNewsArticle(
# #                     source=article_data.get("source", {}).get("name") if article_data.get("source") else None,
# #                     headline=article_data.get("title", "No title available"),
# #                     summary=article_data.get("description"), # Using description as summary
# #                     date=article_data.get("publishedAt")
# #                 )
# #                 cleaned_news_items.append(item)
# #         else:
# #             api_error_message = news_data.get('message', 'Unknown error from NewsAPI.org')
# #             print(f"NewsAPI.org error for '{account_name}' with query '{actual_query_sent}': {api_error_message}")
# #             data_source_comment = f"Could not fetch news from NewsAPI.org: {api_error_message}"
        
# #         if not cleaned_news_items and news_data.get("status") == "ok":
# #             data_source_comment = f"No news articles found for '{account_name}' with query '{actual_query_sent}' via NewsAPI.org."

# #     except httpx.RequestError as exc:
# #         print(f"HTTP Exception for '{account_name}' with NewsAPI.org: {exc}")
# #         data_source_comment = f"Could not fetch news for '{account_name}' due to a network error with NewsAPI.org."
# #     except Exception as e:
# #         print(f"An unexpected error occurred for '{account_name}' with NewsAPI.org: {e}")
# #         data_source_comment = f"An error occurred while processing news for '{account_name}' from NewsAPI.org."

# #     return AccountCleanedNewsResponse(
# #         account_name=account_name,
# #         retrieved_at=datetime.datetime.utcnow().isoformat() + "Z",
# #         news_items=cleaned_news_items, # Using the new field name
# #         search_query_used=actual_query_sent,
# #         data_source_comment=data_source_comment
# #     )

# # # Root endpoint
# # @app.get("/")
# # async def read_root():
# #     return {"message": "Welcome to the Account External Cleaned News API (NewsAPI.org)! Access news at /account_external_data"}

# # # Main execution for Uvicorn
# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
import httpx
import os
from dotenv import load_dotenv
from typing import List, Optional

# Load environment variables from .env file
load_dotenv()

# --- Define Data Structures to MATCH THE ORIGINAL DUMMY JSON ---
class OriginalMarketNewsItem(BaseModel):
    source: Optional[str] = None # Renamed from source_name for consistency
    headline: str
    # summary: Optional[str] = None # Original dummy didn't have summary here
    date: Optional[str] = None
    # url: Optional[str] = None # Original dummy didn't have url here

class OriginalCompetitorActivity(BaseModel): # Placeholder
    competitor_x: str = "Data not available from current news source"
    competitor_y: str = "Data not available from current news source"

class OriginalIndustryOutlook(BaseModel): # Placeholder
    sector: str = "Data not available from current news source"
    trend: str = "Data not available from current news source"
    sentiment: str = "Data not available from current news source"

class OriginalExternalDataPoints(BaseModel):
    market_news: List[OriginalMarketNewsItem]
    competitor_activity: OriginalCompetitorActivity
    industry_outlook: OriginalIndustryOutlook

class OriginalAccountResponse(BaseModel): # Main response model
    account_name: str
    retrieved_at: str
    external_data_points: OriginalExternalDataPoints
    data_source_comment: str
    # We will omit search_query_used to match the original more closely

# --- Initialize the FastAPI app ---
app = FastAPI(
    title="Account External Data API (POC - NewsAPI.org - Original Structure)",
    description="Provides news articles using NewsAPI.org, formatted like the original dummy JSON.",
    version="0.4.0", # Version updated
)

# --- Get API Key ---
NEWSAPI_API_KEY = os.getenv("NEWSAPI_KEY")

if not NEWSAPI_API_KEY:
    print("ERROR: NEWSAPI_KEY not found. Please ensure it's set in your .env file.")

# --- API Endpoint: /account_external_data ---
@app.get("/account_external_data", response_model=OriginalAccountResponse) # Use the new response model
async def get_account_news_data(account_name: str):
    if not NEWSAPI_API_KEY:
        raise HTTPException(status_code=500, detail="API Key for news service is not configured.")

    if account_name.lower() == "sony":
        search_query = f'"{account_name} Corporation" OR "{account_name} Group" OR "{account_name} business" OR "{account_name} financials" OR "{account_name} strategy" OR "{account_name} innovations" NOT (PlayStation OR PS5 OR PS4 OR "Spider-Man" OR movie OR music OR gaming)'
    else:
        search_query = f'"{account_name}" AND (business OR corporate OR financial OR product OR partnership OR strategy)'

    newsapi_url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": search_query,
        "apiKey": NEWSAPI_API_KEY,
        "pageSize": 7, # Let's stick to 5 for market_news as in dummy
        "sortBy": "relevancy",
        "language": "en"
    }

    market_news_items = []
    data_source_comment = "Market news from NewsAPI.org. Other sections are placeholders."
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(newsapi_url, params=params, timeout=10.0)
            response.raise_for_status()
        
        news_data = response.json()

        if news_data.get("status") == "ok":
            for article_data in news_data.get("articles", []):
                item = OriginalMarketNewsItem(
                    source=article_data.get("source", {}).get("name") if article_data.get("source") else None,
                    headline=article_data.get("title", "No title available"),
                    # summary is not in OriginalMarketNewsItem
                    date=article_data.get("publishedAt")
                    # url is not in OriginalMarketNewsItem
                )
                market_news_items.append(item)
        else:
            api_error_message = news_data.get('message', 'Unknown error from NewsAPI.org')
            print(f"NewsAPI.org error for '{account_name}' with query '{search_query}': {api_error_message}")
            data_source_comment = f"Could not fetch news from NewsAPI.org: {api_error_message}"
        
        if not market_news_items and news_data.get("status") == "ok":
            data_source_comment = f"No market news articles found for '{account_name}' with query '{search_query}' via NewsAPI.org."

    except httpx.RequestError as exc:
        print(f"HTTP Exception for '{account_name}' with NewsAPI.org: {exc}")
        data_source_comment = f"Could not fetch market news for '{account_name}' due to a network error with NewsAPI.org."
    except Exception as e:
        print(f"An unexpected error occurred for '{account_name}' with NewsAPI.org: {e}")
        data_source_comment = f"An error occurred while processing market news for '{account_name}' from NewsAPI.org."

    # Create placeholder for other sections of the original dummy data
    placeholder_competitor_activity = OriginalCompetitorActivity()
    placeholder_industry_outlook = OriginalIndustryOutlook()

    external_data = OriginalExternalDataPoints(
        market_news=market_news_items,
        competitor_activity=placeholder_competitor_activity,
        industry_outlook=placeholder_industry_outlook
    )

    return OriginalAccountResponse(
        account_name=account_name, # Use the input account_name, or Sony's proper cased name if matched
        retrieved_at=datetime.datetime.utcnow().isoformat() + "Z",
        external_data_points=external_data,
        data_source_comment=data_source_comment
    )

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Account External Data API (Original Structure)! Access data at /account_external_data"}

# Main execution for Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# import datetime
# import httpx
# import os
# from dotenv import load_dotenv
# from typing import List, Optional

# # Load environment variables from .env file
# load_dotenv()

# # --- Define Data Structures to MATCH THE ORIGINAL DUMMY JSON (with summary and URL added back) ---
# class OriginalMarketNewsItem(BaseModel):
#     source: Optional[str] = None
#     headline: str
#     summary: Optional[str] = None # <<<<----- ADDED THIS BACK
#     date: Optional[str] = None
#     url: Optional[str] = None   # <<<<----- ADDED THIS BACK

# class OriginalCompetitorActivity(BaseModel): # Placeholder
#     competitor_x: str = "Data not available from current news source"
#     competitor_y: str = "Data not available from current news source"

# class OriginalIndustryOutlook(BaseModel): # Placeholder
#     sector: str = "Data not available from current news source"
#     trend: str = "Data not available from current news source"
#     sentiment: str = "Data not available from current news source"

# class OriginalExternalDataPoints(BaseModel):
#     market_news: List[OriginalMarketNewsItem]
#     competitor_activity: OriginalCompetitorActivity
#     industry_outlook: OriginalIndustryOutlook

# class OriginalAccountResponse(BaseModel): # Main response model
#     account_name: str
#     retrieved_at: str
#     external_data_points: OriginalExternalDataPoints
#     data_source_comment: str

# # --- Initialize the FastAPI app ---
# app = FastAPI(
#     title="Account External Data API (POC - NewsAPI.org - Original Structure with Summary)",
#     description="Provides news articles using NewsAPI.org, formatted like the original dummy JSON, now including summary and URL.",
#     version="0.4.1", # Version updated
# )

# # --- Get API Key ---
# NEWSAPI_API_KEY = os.getenv("NEWSAPI_KEY")

# if not NEWSAPI_API_KEY:
#     print("ERROR: NEWSAPI_KEY not found. Please ensure it's set in your .env file.")

# # --- API Endpoint: /account_external_data ---
# @app.get("/account_external_data", response_model=OriginalAccountResponse)
# async def get_account_news_data(account_name: str):
#     if not NEWSAPI_API_KEY:
#         raise HTTPException(status_code=500, detail="API Key for news service is not configured.")

#     if account_name.lower() == "sony":
#         search_query = f'"{account_name} Corporation" OR "{account_name} Group" OR "{account_name} business" OR "{account_name} financials" OR "{account_name} strategy" OR "{account_name} innovations" NOT (PlayStation OR PS5 OR PS4 OR "Spider-Man" OR movie OR music OR gaming)'
#     else:
#         search_query = f'"{account_name}" AND (business OR corporate OR financial OR product OR partnership OR strategy)'

#     newsapi_url = "https://newsapi.org/v2/everything"
    
#     params = {
#         "q": search_query,
#         "apiKey": NEWSAPI_API_KEY,
#         "pageSize": 7, 
#         "sortBy": "relevancy",
#         "language": "en"
#     }

#     market_news_items = []
#     data_source_comment = "Market news from NewsAPI.org. Other sections are placeholders."
    
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(newsapi_url, params=params, timeout=10.0)
#             response.raise_for_status()
        
#         news_data = response.json()

#         if news_data.get("status") == "ok":
#             for article_data in news_data.get("articles", []):
#                 item = OriginalMarketNewsItem(
#                     source=article_data.get("source", {}).get("name") if article_data.get("source") else None,
#                     headline=article_data.get("title", "No title available"),
#                     summary=article_data.get("description"), # <<<<----- ADDED THIS MAPPING
#                     date=article_data.get("publishedAt"),
#                     url=article_data.get("url")            # <<<<----- ADDED THIS MAPPING
#                 )
#                 market_news_items.append(item)
#         # ... (rest of the error handling and response construction remains the same) ...
#         else:
#             api_error_message = news_data.get('message', 'Unknown error from NewsAPI.org')
#             print(f"NewsAPI.org error for '{account_name}' with query '{search_query}': {api_error_message}")
#             data_source_comment = f"Could not fetch news from NewsAPI.org: {api_error_message}"
        
#         if not market_news_items and news_data.get("status") == "ok":
#             data_source_comment = f"No market news articles found for '{account_name}' with query '{search_query}' via NewsAPI.org."

#     except httpx.RequestError as exc:
#         print(f"HTTP Exception for '{account_name}' with NewsAPI.org: {exc}")
#         data_source_comment = f"Could not fetch market news for '{account_name}' due to a network error with NewsAPI.org."
#     except Exception as e:
#         print(f"An unexpected error occurred for '{account_name}' with NewsAPI.org: {e}")
#         data_source_comment = f"An error occurred while processing market news for '{account_name}' from NewsAPI.org."

#     placeholder_competitor_activity = OriginalCompetitorActivity()
#     placeholder_industry_outlook = OriginalIndustryOutlook()

#     external_data = OriginalExternalDataPoints(
#         market_news=market_news_items,
#         competitor_activity=placeholder_competitor_activity,
#         industry_outlook=placeholder_industry_outlook
#     )

#     return OriginalAccountResponse(
#         account_name=account_name,
#         retrieved_at=datetime.datetime.utcnow().isoformat() + "Z",
#         external_data_points=external_data,
#         data_source_comment=data_source_comment
#     )

# # Root endpoint
# @app.get("/")
# async def read_root():
#     return {"message": "Welcome to the Account External Data API (Original Structure with Summary)! Access data at /account_external_data"}

# # Main execution for Uvicorn
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
