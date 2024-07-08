#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import os

# Libs
from tavily import TavilyClient

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

class TavilyWeb(BaseSource):
    """ Conducts web search queries through the Tavily API
    Requires Tavily API key. This should be defined in the environment variable "TAVILY_API_KEY"
    If not set, it will try to get it from the config.
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self._source_type = "tavily_web"
        self._search_params = config.get("search_params", {})

        try:
            # initialize Tavily client
            api_key = os.getenv("TAVILY_API_KEY") or config["init_params"]["api_key"]
            self._client = TavilyClient(api_key=api_key)
        except Exception as e:
            print(f"Error connecting to Tavily: {e}")
        

    @property
    def source_type(self):
        return self._source_type

    def query(self, search_text) -> List[dict]:
        """
        Perform a search query using the given `search_text`.
        
        Args:
            search_text (str): The text to search for.
        
        Returns:
            List[dict]: A list of search results.
                Each dictionary should contain the following keys:
                - "title": The title of the search result.
                - "text": The text of the search result.
        """
        response = self._client.search(
            query=search_text,
            **self._search_params
        )
        return [
            {"title": r["url"], "text": r["content"]}
            for r in response["results"]
        ]

##########
# Script #
##########


if __name__ == '__main__':
    pass