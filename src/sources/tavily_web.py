#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in


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

    def __init__(self, config: dict):
        super.__init__(config)
        self._source_type = "tavily_web"
        self._search_params = config.get("search_params", {})

        try:
            api_key = os.getenv("TAVILY_API_KEY") or config["init_params"]["api_key"]
            self._client = TavilyClient(api_key=api_key)
        except Exception as e:
            print(f"Error connecting to Tavily: {e}")
        

    @property
    def source_type(self):
        return self._source_type

    def query(self, search_text):
        response = self._client.search(
            query=f"Is there evidence to support this claim: '{search_text}'?",
            **self._search_params
        )
        return [
            {"title": r["url"], "text": r["content"]}
            for r in response
        ]

##########
# Script #
##########


if __name__ == '__main__':
    pass