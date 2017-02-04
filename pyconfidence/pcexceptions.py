#!/usr/bin/env python

# =============================================================================
#
#           Exception classes for pyconfidence
#
# =============================================================================



class ConfigurationFailure(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value


class ConfigurationFailureMandatoryAttr(Exception):
    def __init__(self, option, section):
        self.value = 'Mandatory option %s in section %s not present.' %(option, section)
    def __str__(self):
        return self.value

