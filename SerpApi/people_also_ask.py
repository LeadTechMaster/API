"""
SerpApi - People Also Ask
Get "People Also Ask" questions for keywords
"""

import os
import requests
from typing import Dict, List

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def get_people_also_ask(keyword: str) -> Dict:
    """
    Get People Also Ask questions related to a keyword
    
    Args:
        keyword: The keyword to get PAA questions for
        
    Returns:
        Dict with People Also Ask questions and answers
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": SERPAPI_API_KEY,
            "num": 10
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract People Also Ask data
        paa = data.get("related_questions", [])
        
        questions_list = []
        for item in paa:
            questions_list.append({
                "question": item.get("question", ""),
                "answer": item.get("snippet", ""),
                "title": item.get("title", ""),
                "link": item.get("link", "")
            })
        
        result = {
            "keyword": keyword,
            "total_questions": len(questions_list),
            "questions": questions_list,
            "status": "success"
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "keyword": keyword,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "keyword": keyword,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

