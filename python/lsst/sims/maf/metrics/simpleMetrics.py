import numpy as np
from .baseMetric import BaseMetric

# A collection of commonly used simple metrics, operating on a single column and returning a float.

class Coaddm5Metric(BaseMetric):
    """Calculate the coadded m5 value at this gridpoint."""
    def __init__(self, m5Col = 'fiveSigmaDepth', metricName='CoaddM5', **kwargs):
        """Instantiate metric.
        
        m5col = the column name of the individual visit m5 data."""
        super(Coaddm5Metric, self).__init__(col=m5Col, metricName=metricName, **kwargs)
    def run(self, dataSlice, slicePoint=None):
        return 1.25 * np.log10(np.sum(10.**(.8*dataSlice[self.colname]))) 

        
class MaxMetric(BaseMetric):
    """Calculate the maximum of a simData column slice."""
    def run(self, dataSlice, slicePoint=None):
        return np.max(dataSlice[self.colname]) 


class MeanMetric(BaseMetric):
    """Calculate the mean of a simData column slice."""
    def run(self, dataSlice, slicePoint=None):
        return np.mean(dataSlice[self.colname]) 

class MedianMetric(BaseMetric):
    """Calculate the median of a simData column slice."""
    def run(self, dataSlice, slicePoint=None):
        return np.median(dataSlice[self.colname])

    
class MinMetric(BaseMetric):
    """Calculate the minimum of a simData column slice."""
    def run(self, dataSlice, slicePoint=None):
        return np.min(dataSlice[self.colname]) 

class FullRangeMetric(BaseMetric):
    """Calculate the range of a simData column slice."""
    def run(self, dataSlice, slicePoint=None):
        return np.max(dataSlice[self.colname])-np.min(dataSlice[self.colname]) 

class RmsMetric(BaseMetric):
    """Calculate the standard deviation of a simData column slice."""
    def run(self, dataSlice, slicePoint=None):
        return np.std(dataSlice[self.colname]) 

class SumMetric(BaseMetric):
    """Calculate the sum of a simData column slice."""
    def run(self, dataSlice, slicePoint=None):
        return np.sum(dataSlice[self.colname]) 

class CountMetric(BaseMetric):
    """Count the length of a simData column slice. """
    def run(self, dataSlice, slicePoint=None):
        return len(dataSlice[self.colname]) 

class RobustRmsMetric(BaseMetric):
    """Use the inter-quartile range of the data to estimate the RMS.  Robust since this calculation
    does not include outliers in the distribution"""
    def run(self, dataSlice, slicePoint=None):
        iqr = np.percentile(dataSlice[self.colname],75)-np.percentile(dataSlice[self.colname],25)
        rms = iqr/1.349 #approximation
        return rms
    
class BinaryMetric(BaseMetric):
    """Return 1 if there is data. """
    def run(self, dataSlice, slicePoint=None):
        if dataSlice.size > 0:
            return 1
        else:
            return self.badval

class FracAboveMetric(BaseMetric):
    def __init__(self, col=None, cutoff=0.5, **kwargs):
        # Col could just get passed in bundle with kwargs, but by explicitly pulling it out
        #  first, we support use cases where class instantiated without explicit 'col='). 
        super(FracAboveMetric, self).__init__(col, **kwargs)
        self.cutoff = cutoff
    def run(self, dataSlice, slicePoint=None):
        good = np.where(dataSlice[self.colname] >= self.cutoff)[0]
        fracAbove = np.size(good)/float(np.size(dataSlice[self.colname]))
        return fracAbove

class FracBelowMetric(BaseMetric):
    def __init__(self, col=None, cutoff=0.5, **kwargs):
        super(FracBelowMetric, self).__init__(col, **kwargs)
        self.cutoff = cutoff
    def run(self, dataSlice, slicePoint=None):
        good = np.where(dataSlice[self.colname] <= self.cutoff)[0]
        fracBelow = np.size(good)/float(np.size(dataSlice[self.colname]))
        return fracBelow