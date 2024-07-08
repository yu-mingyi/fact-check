#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
from abc import ABC, abstractmethod

# Libs


# Custom


##################
# Configurations #
##################


#############
# Functions #
#############


###########
# Classes #
###########

class AbstractSource(ABC):
    """ Abstract class for all sources to inherit from.
    Defines interface through which orchestrator can interact with sources.
    """

    @abstractmethod
    def query(self, search_text: str):
        raise NotImplementedError

    @property
    @abstractmethod
    def id(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self):
        raise NotImplementedError

##########
# Script #
##########


if __name__ == '__main__':
    pass