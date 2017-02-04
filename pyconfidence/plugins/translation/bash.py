#!/usr/bin/env python


import pyconfidence

class Bash(object):
# FIXME


    def __init__(self):
        pass

    def load(self, fp, delimiter='='):
        """
        reads a config file from a bash file with no sections
        """

        conf = pyconfidence.SingleSectionConfig()

        # NOTE:
        # there are other implementations. For example:
        #       http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788
        # but this one allows for different delimiters
        # 
        for line in fp.readlines():
            line = line[:-1]
            if '#' in line:
                line = line.split('#')[0]
                line.strip()
            if line:
                fields = line.split(delimiter)
                c.set(fields[0].strip(), fields[1].strip())

        return conf

