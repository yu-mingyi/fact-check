# maps source_type to source module and class name
SOURCE_MAPPING = {
    "milvus_vdb": ("milvus_vdb", "MilvusVDB"),
    "tavily_web": ("tavily_web", "TavilyWeb")
}

# maps llm module to env var for api key
API_MAPPING = {
    "langchain_google_genai": "GOOGLE_API_KEY",
    "langchain_openai": "OPENAI_API_KEY"
}