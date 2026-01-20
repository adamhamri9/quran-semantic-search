from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from api.schemas.search_input import SearchInput
from api.schemas.search_response import SearchResponse
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

@app.post("/search", response_model=SearchResponse)
async def search_quran(params: SearchInput):
    try:
        result = await search(retriever, context_builder, params)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        # Your OpenAPI document
        openapi_url=app.openapi_url,
        # Avoid CORS issues (optional)
        scalar_proxy_url="https://proxy.scalar.com",
)
