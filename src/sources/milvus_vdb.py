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
    def source_type(self):
        return self._source_type

    def query(self, search_text: str) -> List:
        search_results = self._client.search(
            data = [self._model.embed_query(search_text)],
            **self._search_params
        )[0]
        return [r["entity"] for r in search_results]


    def _load_embedding_model(self, embedding_params):
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