#!/usr/bin/env python

# =============================================================================
#
#           classes and functions to manage the configuration objects
#
# =============================================================================

import calendar
import datetime 
import time
import urllib2

import pyconfidence
# NOTE:
# to avoid problems due the circular imports
# between modules, we 
#   "import pyconfidence" 
# instead
#   "from pyconfidence import foo" 


class Mgmt(object):
    def __init__(self):
        pass


    def getConfig(self, sources=None, configdir=None):
        """ returns a Config object.

        Args:
            sources (split by comma string): each item points to the info 
                to feed the object:
                    - path to physical file on disk
                    - an URL
            configdir(string): path to a directory with a set of 
                configuration files, all of them to be processed.

        """
        
        try:
            config = pyconfidence.Config()
            if sources:
                for src in sources.split(','):
                    src = src.strip()
                    newconfig = self.__getConfig(src)
                    if newconfig:
                        config.merge(newconfig)
                        # IMPORTANT NOTE:
                        # because we create here the final configloader object
                        # by merge() of each config object (one per source)
                        # with an empty one, the 'defaults' dictionary {...} of each one
                        # is lost. 
                        # Therefore, the final configloader object has empty 'defaults' dictionary {}
            elif configdir:
                if os.path.isdir(configdir):
                    conffiles = [os.path.join(configdir, f) for f in os.listdir(configdir) if f.endswith('.conf')]
                    config.read(conffiles)
                    # IMPORTANT NOTE:
                    # here, as we use the native python method read()
                    # the configloader object still keeps the 'defaults' dictionary {...}
                else:
                    raise pyconfidence.ConfigFailure('configuration directory %s does not exist' %configdir)
            config.fixpathvalues()
            return config
        except:
            raise pyconfidence.ConfigFailure('creating config object from source %s failed' %sources)


    def __getConfig(self, src):
        '''
        returns a new ConfigParser object 
        '''

        data = self.__getContent(src)
        if data:
            tmpconfig = Config()
            tmpconfig.readfp(data)
            return tmpconfig
        else:
            return None


    def __getContent(self, src):
        '''
        returns the content to feed a new ConfigParser object
        '''
        
        sourcetype = self.__getsourcetype(src)
        if sourcetype == 'file':
            return self.__dataFromFile(src)
        if sourcetype == 'uri':
            return self.__dataFromURI(src)


    def __getsourcetype(self, src):
        '''
        determines if the source is a file on disk on an URI
        '''
        
        sourcetype = 'file'  # default
        uritokens = ['file://', 'http://']
        for token in uritokens:
            if src.startswith(token):
                sourcetype = 'uri'
                break
        return sourcetype


    def __dataFromFile(self, path):
        '''
        gets the content of an config object from  a file
        '''
        
        try:
            f = open(path)
            return f
        except:
            raise pyconfidence.ConfigurationFailure("Problem with config file %s" % path)


    def __dataFromURI(self, uri):
        '''
        gets the content of an config object from an URI.
        '''
        
        opener = urllib2.build_opener()
        urllib2.install_opener(opener)
        try:
            uridata = urllib2.urlopen(uri)
            return uridata
        except:
            raise pyconfidence.ConfigurationFailure("Problem with URI source %s" % uri)


    def json(self, source):
        config = pyconfidence.Config()
        import json
        doc = json.load(source)
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


    def getSingleSectionConfig(self):
        pass
