#!/usr/bin/env python

# =============================================================================
#
#           central services for the pyconfidence project
#
# =============================================================================

import logging


class NullHandler(logging.Handler):

    # Adding NullHandler so this lib can have logging
    # NullHandler is available since python 2.7
    # it is include here for python 2.6

    def handle(self, record):
        pass

    def emit(self, record):
        pass

    def createLock(self):
        self.lock = None

