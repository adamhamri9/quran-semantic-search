from langdetect import detect
from api.schemas.search_input import SearchInput
from api.schemas.search_response import SearchResponse
from api.services.search.retriever import QuranRetriever
from api.services.search.context import QuranContextBuilder

async def search(
    quran_retriever: QuranRetriever, 
    context_builder: QuranContextBuilder, 
    params: SearchInput
) -> SearchResponse:
    
    try:
        detected_lang = detect(params.query)
    except Exception:
        detected_lang = "en"

    if params.settings.translation_lang == "auto":
        params.settings.translation_lang = detected_lang
    if params.settings.tafsir_lang == "auto":
        params.settings.tafsir_lang = detected_lang

    primary_lang = params.settings.translation_lang
    use_arabic_first = primary_lang in ["en", "fr"]

    index = quran_retriever._get_resource("ar" if use_arabic_first else primary_lang, "index")
    if not index:
        index = quran_retriever._get_resource("ar", "index")

    results = await quran_retriever._search_with_index(params, index)

    if use_arabic_first:
        avg_score = sum(r.score for r in results) / max(len(results), 1)
        if avg_score < 0.5:
            index_fb = quran_retriever._get_resource(primary_lang, "index")
            if index_fb:
                results = await quran_retriever._search_with_index(params, index_fb)

    if params.context.enable_context_links and results:
        for r in results:
            r.context_links = context_builder.build_context(
                surah=r.surah,
                ayah=r.ayah,
                index=index,
                window=params.context.context_window,
                similarity_threshold=params.context.similarity_threshold,
                max_links=params.context.max_context_links
            )

    return SearchResponse(
        query=params.query,
        detected_lang=detected_lang,
        results=results
    )