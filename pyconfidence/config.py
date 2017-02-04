#!/usr/bin/env python

import calendar
import datetime 
import time

import ConfigParser

import pyconfidence
# NOTE:
# to avoid problems due the circular imports
# between modules, we 
#   "import pyconfidence" 
# instead
#   "from pyconfidence import foo" 


class Config(ConfigParser.SafeConfigParser, object):
    """
    custom class to read configuration files,
    and more. 

    Documentation on ConfigParser can be found here:
        https://docs.python.org/2/library/configparser.html
    """

    def __init__(self):
        ConfigParser.SafeConfigParser.__init__(self)

    def getlist(self, section, option, conv=str):
        '''
        converts the value into a list.
        If needed, converts each item in the list
        '''
        value = super(Config,self).get(section, option)
        return [conv(i.strip()) for i in value.split(',')]


    def getSection(self, section):
        '''
        creates and returns a new Config object, 
        with the content of a single section
        '''
    
        conf = pyconfidence.single.SingleSectionConfig(section)
        if self.has_section(section):
            for item in self.items(section, raw=True):
                conf.set(item[0], item[1])
        return conf


    def __str__(self):
        # FIXME
        # I am not sure __str__ is for this
        """
        returns a string with the content of the config file.
        Mostly for logging and testing.
        It does not checks type (int, float, boolean),
        just returns a raw string.
        """
        
        out = ''
        for section in self.sections():
            out += '[%s]\n' %section
            for item in self.items(section):
                out += '%s = %s\n' %item
        out = out[:-1]
        return out


    def getraw(self):
        """
        returns the raw content of the entire object
        """
        import StringIO
        io = StringIO.StringIO()
        self.write(io)
        out = io.getvalue()
        io.close()
        return out


    def sectionisequal(self, config, section):
        '''
        this method checks if a given section is equal in two configloader objects
        '''
    
        # probably it can be done simply by 
        #   return ( self.items(section) == config.items(section) )
        # it is not done like that, yet, because I am not sure if items() would return the dictionary sorted in the same way,
        # or if that matters when comparing dictionaries
        # so, meanwhile, we just compare variable by variable
    
        options1 = self.options(section)
        options2 = config.options(section)
        options1.sort()
        options2.sort()
        if options1 != options2:
            return False
    
        # else...
        for option in self.options(section):
            if self.get(section, option) != config.get(section, option):
                return False
        else:
            return True



    def compare(self, config):
        '''
        compares the current Config object with a new one.
        It returns an structure saying 
            -- the list of SECTIONS that are equal,
            -- the list of SECTIONS that have changed,
            -- the list of SECTIONS that have been removed,
            -- the list of SECTIONS that have been added,
        The output is a dictionary of lists:
        
            out = {'EQUAL': ['SEC1', ..., 'SECn'],
                   'MODIFIED': ['SEC1', ..., 'SECn'],
                   'REMOVED': ['SEC1', ..., 'SECn'],
                   'ADDED': ['SEC1', ..., 'SECn'],
                  }
        '''
    
        out = {'EQUAL': [],
               'MODIFIED': [],
               'REMOVED': [],
               'ADDED': [],
              }
    
        sections1 = self.sections()
        sections1.sort()
        sections2 = config.sections()
        sections2.sort()
    
        # first, we check for the SECTIONS that have been removed
        for section in sections1:
            if section not in sections2:
                out['REMOVED'].append(section)
        # it could be done in a single line like  
        # out = [section for section in sections1 if section not in sections2]
    
    
        # second, we check for the SECTIONS that have been added 
        for section in sections2:
            if section not in sections1:
                out['ADDED'].append(section)
        # it could be done in a single line like  
        # out = [section for section in sections2 if section not in sections1]
    
        # finally we search for the SECTIONS that are equal or modified
        for section in sections1:
            if section in sections2:
                if self.sectionisequal(config, section):
                    out['EQUAL'].append(section)
                else:
                    out['MODIFIED'].append(section)
    
        return out


    def getdict(self, section):
        '''
        converts a given section into a dictionary
        '''
        d = {}
        for i in self.items(section):
            key = i[0]
            value = i[1]
            d[key] = value
        return d


    def mapkeys(self, keys_dict):
        for sect in self.sections():
            for oldk, newk in keys_dict.iteritems():
                if self.has_option(sect, oldk):
                    v = self.get(sect, oldk)
                    self.set(sect, newk, v)
                    self.remove_option(sect, oldk)
