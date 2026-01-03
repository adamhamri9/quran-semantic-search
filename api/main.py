from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from api.schemas.search_input import SearchInput
from api.services.search.retriever import QuranRetriever
from api.services.search.context import QuranContextBuilder
from api.services.search.service import search

app = FastAPI(title="Quran Semantic Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever = QuranRetriever()
context_builder = QuranContextBuilder(retriever.verses)

@app.post("/search")
async def search_quran(params: SearchInput):
    try:
        result = await search(retriever, context_builder, params)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
