from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from api.schemas.search_input import SearchInput
from api.services.search.retriever import QuranRetriever

app = FastAPI(title="Quran Semantic Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever = QuranRetriever()

@app.post("/search")
async def search_quran(params: SearchInput):
    try:
        result = await retriever.search(params)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
