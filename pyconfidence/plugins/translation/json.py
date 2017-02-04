#!/usr/bin/env python

import json
from pyconfidence import Config

class Json(object):
# FIXME: it should inherit from a TranslationInterface

    def __init__(self):
        pass

    def loads(self, source):
        #config = pyconfidence.Config()
        config = Config()
        doc = json.loads(source)
        # for now, we assume the json is a dictionary
        for k, v in doc.iteritems():
            config.add_section(str(k))
            for k2, v2 in v.iteritems():
                if type(v2) != dict:
                    config.set(str(k), str(k2), str(v2))
                else:
                    for k3, v3 in v2.iteritems():
                       config.set(str(k), '%s.%s' %(str(k2), str(k3)), str(v3))
        return config
