#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Literal
from generator import BlackpillGenerator
from retriever import DualModeRetriever
from visual_kb import VisualKnowledgeBase
from image_handler import ImageHandler
from config import VISUAL_KB_CONFIG, IMAGE_CONFIG
import uvicorn
import time

app = FastAPI(
    title="Alternative Lifestyle AI API",
    description="Comprehensive AI for alternative diet, looksmaxxing, pharmacology, and blackpill knowledge",
    version="3.0.0"
)

retriever = DualModeRetriever()
generator = BlackpillGenerator()
visual_kb = VisualKnowledgeBase(VISUAL_KB_CONFIG)
image_handler = ImageHandler(IMAGE_CONFIG)

@app.on_event("startup")
async def startup():
    try:
        retriever.load_vector_store()
    except Exception as e:
        print(f"Error: {e}")


class QueryRequest(BaseModel):
    query: str
    mode: Literal["fast", "deep", "youtube"] = "fast"
    max_results: Optional[int] = 8
    max_tokens: Optional[int] = 512
    filter_source: Optional[str] = None


class QueryResponse(BaseModel):
    query: str
    answer: str
    mode: str
    sources: List[Dict]
    model: str
    processing_time: Optional[float] = None
    used_last_resort: bool = False


class ImageResponse(BaseModel):
    id: str
    url: str
    local_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    category: str
    source: str
    width: Optional[int] = None
    height: Optional[int] = None


@app.get("/")
async def root():
    return {
        "name": "Alternative Lifestyle AI API",
        "version": "3.0.0",
        "modes": ["fast", "deep", "youtube"],
        "philosophy": "Terrain Theory: Bernard was right. The microbe is nothing, the terrain is everything."
    }


@app.post("/query")
async def query(request: QueryRequest):
    start = time.time()
    try:
        used_last_resort = False
        if request.mode == "fast":
            context, mode, used_last_resort = retriever.retrieve_with_fallback(
                request.query, k=request.max_results, filter_source=request.filter_source
            )
        elif request.mode == "deep":
            context, mode = retriever.deep_retrieve(request.query, max_results=request.max_results)
        else:
            context, mode = retriever.youtube_retrieve(request.query, max_results=request.max_results)
        
        answer = generator.generate(
            request.query, context, mode, request.max_tokens, use_last_resort=used_last_resort
        )
        
        sources = []
        for item in context:
            md = item.get('metadata', {})
            sources.append({
                'source': md.get('source', 'Unknown'),
                'title': md.get('title', ''),
                'url': md.get('url', ''),
                'category': item.get('category', md.get('category', 'general')),
                'last_resort': md.get('is_last_resort', False)
            })
        
        return QueryResponse(
            query=request.query,
            answer=answer,
            mode=mode,
            sources=sources,
            model=generator.model_name,
            processing_time=round(time.time() - start, 3),
            used_last_resort=used_last_resort
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sources")
async def list_sources():
    from config import SOURCES, WIKI_PAGES, REDDIT_SOURCES, ADDITIONAL_REDDIT_SOURCES, SCRIBD_DOCUMENTS, SOCIAL_MEDIA_SOURCES
    return {
        "sources": list(SOURCES.keys()) + ["wikipedia", "reddit", "scribd", "social_media"],
        "last_resort_sources": ["incels_is", "schaduw"],
        "last_resort_policy": "Used only when primary sources provide insufficient information. AI acknowledges their right to exist but maintains a Faustian approach."
    }


@app.get("/images", response_model=List[ImageResponse])
async def list_images(category: Optional[str] = None, source: Optional[str] = None, limit: int = 20):
    if category:
        images = visual_kb.get_images_by_category(category)
    elif source:
        images = visual_kb.get_images_by_source(source)
    else:
        images = visual_kb.image_index['images']
    return [ImageResponse(**img) for img in images[:limit]]


@app.get("/images/stats")
async def image_stats():
    return visual_kb.get_statistics()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)