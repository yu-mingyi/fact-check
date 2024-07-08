#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import importlib
from typing import List

# Libs
from pymilvus import MilvusClient


# Custom
from .base_source import BaseSource

##################
# Configurations #
##################


#############
# Functions #
#############


###########
# Classes #
###########

class MilvusVDB(BaseSource):
    """ Connects to a Milvus server and performs search queries.
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self._source_type = "milvus_vdb"
        self._search_params = config["search_params"]

        # initialize Milvus client
        # requires Milvus server to be running and accessible at specified config
        try: 
            self._client = MilvusClient(**config["init_params"])
        except Exception as e:
            print(f"Error connecting to Milvus: {e}")

        # initialize embeddings
        self._model = self._load_embedding_model(config["embedding_params"])

    @property
    def source_type(self) -> str:
        return self._source_type

    def query(self, search_text: str) -> List[dict]:
        """ Perform a search query using the given `search_text`.

        Args:
            search_text (str): The text to search for.

        Returns:
            List[dict]: A list of entities that match the search query.
                Each dictionary should contain the following keys:
                - "title": The title of the entity.
                - "text": The text of the entity.
        """
        search_results = self._client.search(
            data = [self._model.embed_query(search_text)],
            **self._search_params
        )[0]
        return [r["entity"] for r in search_results]


    def _load_embedding_model(self, embedding_params: dict) -> object:
        """ Load an embedding model based on the provided configuration.

        Args:
            embedding_params (dict): The configuration for loading the embedding model.
                It should contain the following keys:
                - "load_params" (dict): The parameters for loading the embedding model.
                    It should contain the following keys:
                    - "module" (str): The module name for importing the embedding model.
                    - "class" (str): The class name for importing the embedding model.
                - "init_params" (dict): The initialization parameters for the embedding model.
                    It should contain the following keys:
                    - "model_name" (str): The name of the embedding model, e.g., "BAAI/bge-small-en-v1.5"
                    Other keys may be defined based on the API specification.

        Returns:
            object: The loaded embedding model object.
                As currently implemented, this should adhere to the 
                langchain_community.embeddings API

        Raises:
            Exception: If there is an error loading the embedding model.

        """
        try:
            emb_load_module = embedding_params["load_params"]["module"]
            emb_load_class = embedding_params["load_params"]["class"]
            return getattr(
                importlib.import_module(emb_load_module), 
                emb_load_class
            )(**embedding_params["init_params"])
        except Exception as e:
            print(f"Error loading embedding model: {e}")

##########
# Script #
##########


if __name__ == '__main__':
    pass