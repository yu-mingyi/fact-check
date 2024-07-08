# fact-check

## Overview
FactCheckOrchestrator is a tool designed to perform automated fact-checking on a given text. It breaks down the input text into individual claims, queries multiple information sources, evaluates the claims against the retrieved information, and if necessary, drafts a revised version of the original text. This process is coordinated through the `FactCheckOrchestration` module defined in `src`, utilizing an agentic workflow implemented via LangGraph.

### Key Features
- **Orchestration**: FactCheckOrchestrator coordinates the entire fact-checking process, ensuring that each claim is properly routed, verified, and revised if needed.
- **Information Sources**: The tool currently supports web search through the Tavily API and semantic search over a Milvus vector database. Additional sources can be added, provided they conform to the `src.sources.AbstractSource` interface.
- **Agentic Workflow**: Implemented through LangGraph, the workflow includes multiple nodes (analyst, verifier, summarizer, reviser) that perform specific tasks in the fact-checking process.

### Information Sources
- **Web Search**: Utilizes the Tavily API for up-to-date information on general topics.
- **Semantic Search**: Uses a Milvus vector database to search over documents. 

New information source types can be added by implementing the interface defined in `src.sources.AbstractSource`.

## How to Run
1. **Set Required Environment Variables**: Ensure that the necessary API keys are set as environment variables. Keys include:
    - `OPENAI_API_KEY` (if running the OpenAI API)
    - `GOOGLE_API_KEY`(if running the Google API)
    - `TAVILY_API_KEY` (if including Tavily web search as an infromation source)

2. **Setup Development Environment**: Install the required dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Script**: Execute the script to perform verification on an example article located at `sample_text.txt`:
    ```bash
    python main.py
    ```

## Configuration

The `config.yaml` file is the central configuration for the project, allowing users to flexibly define specifications based on their requirements. Below are the required fields and their descriptions:

### agent_config
- **max_checks**: This parameter limits the number of claims to check to prevent excessive API calls. 

### llm
- **load_params**: Configuration for loading the language model (LLM).
  - **module**: The module name of the LLM.
  - **class**: The class name of the LLM.
  - **api_key**: (Optional) The API key for the LLM. If an API key is not defined as an environment variable, it will be loaded from the config.
- **init_params**: Initialization parameters for the LLM.
  - **model**: The model name of the LLM.
  - Other parameters specifying model settings (e.g., **temperature**) should be defined here. 

### sources
A list of information sources to be used in the fact-checking process. Each source requires the following configuration:
- **source_type**: The type of the source. This maps to a module in the sources package via `SOURCE_MAPPING` as defined in `src/mappings.py`. Currently supported `source_type`s are: `milvus_vdb` and `tavily_web`.
- **config**: The configuration details for the source.
  - **id**: The unique identifier for the source.
  - **description**: A brief description of the source, used by the analyst agent to route the claim to the appropriate sources.
  - Other parameters may be required based on the `source_type`:
    - **init_params**: (Required for vdb) Initialization parameters specific to the source type.
    - **search_params**: Parameters for querying the source, such as the collection name and limit.
    - **embedding_params**: (Required for vdb) Parameters for the embedding model, including the model and query instructions.
