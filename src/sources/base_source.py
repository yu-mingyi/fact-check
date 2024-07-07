#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in


# Libs


# Custom
from .abstract_source import AbstractSource

##################
# Configurations #
##################


#############
# Functions #
#############


###########
# Classes #
###########

class BaseSource(AbstractSource):

    def __init__(self, config: dict):
        super.__init__()
        self._id = config['id']
        self._description = config['description']

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

##########
# Script #
##########


if __name__ == '__main__':
    pass