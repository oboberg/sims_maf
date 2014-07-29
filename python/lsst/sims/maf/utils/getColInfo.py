import inspect
import numpy as np
import lsst.sims.maf.stackers as stackers 

class ColInfo(object):
    def __init__(self):
        """Set up the unit and source dictionaries.
        """
        self.defaultDataSource = None
        self.defaultUnit = ''
        self.unitDict = {'fieldID': '#',
                        'filter': 'filter',
                        'seqnNum' : '#',
                        'expMJD': 'MJD',
                        'expTime': 's',
                        'slewTime': 's',
                        'slewDist': 'rad',
                        'rotSkyPos': 'rad',
                        'rotTelPos': 'rad',
                        'rawSeeing': 'arcsec',
                        'finSeeing': 'arcsec', 
                        'seeing': 'arcsec',
                        'airmass': 'airmass',
                        'night': 'days',
                        'fieldRA': 'rad',
                        'fieldDec': 'rad', 
                        'moonRA': 'rad',
                        'moonDec': 'rad',
                        'moonAlt': 'rad',
                        'dist2Moon': 'rad',
                        'filtSkyBrightness': 'mag/sq arcsec',
                        'VskyBright': 'mag/sq arcsec',
                        'fiveSigmaDepth':'mag',
                        'ditheredRA':'rad',
                        'ditheredDec':'rad'}
        # Go through the available stackers and add any units, and identify their
        #   source methods.
        self.sourceDict = {}
        for stackerClass in stackers.BaseStacker.registry.itervalues():
            stacker = stackerClass()
            for col, units in zip(stacker.colsAdded, stacker.units):
                self.sourceDict[col] = stackerClass
                self.unitDict[col] = units
        # Note that a 'unique' list of methods should be built from the resulting returned
        #  methods, at whatever point the derived data columns will be calculated. (i.e. in the driver)

    def getUnits(self, colName):
        """Return the appropriate units for colName.
        """
        if colName in self.unitDict:
            return self.unitDict[colName]
        else:
            return self.defaultUnit

    def getDataSource(self, colName):
        """Given a column name to be added to simdata, identify appropriate source. 

        For values from database, this is self.defaultDataSource ('db'). 
        For values which are precalculated for a particular column, this should be a 
        method added to this class."""
        if colName in self.sourceDict:
            return self.sourceDict[colName]
        else:
            return self.defaultDataSource
