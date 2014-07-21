import numpy as np
from lsst.sims.maf.stackers import BaseStacker
from lsst.sims.maf.stackers import wrapRA, wrapDec

class SingleFieldDitherStacker(BaseStacker):
    """
    Repurpose LSST to only look at one field - 'dither' all pointings to single RA/Dec value.
    """
    def __init__(self, fixedRA=0.0, fixedDec=0.0):
        """
        fixedRA and fixedDec are the RA/Dec values for the new columns (in radians).
        """
        self.fixedRA = fixedRA
        self.fixedDec = fixedDec
        # Required lines:
        # List of the names of the columns generated by the Stacker.
        self.colsAdded = ['fixedRA', 'fixedDec']
        # List of the names of the columns required from the database (to generate the Stacker columns).
        self.colsReq = []
        # Optional: provide a list of units for the columns defined in colsAdded.
        self.units = ['rad', 'rad']

    def run(self, simData):
        # Add new columns defined by self.colsAdded to simData
        #  (this is where we'll put our new data)
        simData = self._addStackers(simData)
        # Calculate the values for your columns
        simData['fixedRA'] = self.fixedRA
        simData['fixedDec'] = self.fixedDec
        # Return the updated simData array
        return simData


class YearlyDitherStacker(BaseStacker):
    """
    Add a dither of half the FOV depending on the year of the survey.
    """
    def __init__(self, expMJDCol='expMJD', raCol='fieldRA', decCol='fieldDec'):
        # Names of columns we want to add.
        self.colsAdded = ['yearlyDitherRA', 'yearlyDitherDec']
        # Names of columns we need from database.
        self.colsReq = [expMJDCol, raCol, decCol]
        # List of units for our new columns.
        self.units = ['rad', 'rad']
        # Set our dither offset.
        self.ditherOffset = 1.75/180.*np.pi
        # And save the column names.
        self.expMJDCol = expMJDCol
        self.raCol = raCol
        self.decCol = decCol
                
    def run(self, simData):
        # Add new columns to simData.
        simData = self._addStackers(simData)
        # What 'year' is each visit in?
        year = np.floor((simData[self.expMJDCol] - simData[self.expMJDCol][0]) / 365.25)
        # Define dither based on year. 
        ditherRA = np.zeros(len(simData[self.raCol]))
        ditherDec = np.zeros(len(simData[self.decCol]))
        # In y1, y3, y5, y6, y8 & y10 ra dither = 0.
        # In y2 & y7, ra dither = +ditherOffset
        # In y4 & y9, ra dither = -ditherOffset    
        condition = ((year == 2) | (year == 7))
        ditherRA[condition] = self.ditherOffset
        condition = ((year == 4) | (year == 9))
        ditherRA[condition] = -1.*self.ditherOffset
        simData['yearlyDitherRA'] = wrapRA(simData[self.raCol] + ditherRA)
        # In y1, y2, y4, y6, y7 & y9, dec dither = 0
        # In y3 & y8, dec dither = -ditherOffset
        # In y5 & y10, dec dither = ditherOffset
        condition = ((year == 3) | (year == 8))
        ditherDec[condition] = -1.*self.ditherOffset
        condition = ((year == 5) | (year == 10))
        ditherDec[condition] = self.ditherOffset
        simData['yearlyDitherDec'] = wrapDec(simData[self.decCol] + ditherDec)
        return simData
                                            

