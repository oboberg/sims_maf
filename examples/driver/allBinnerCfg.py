import numpy as np
from lsst.sims.operations.maf.driver.mafConfig import *

# Setup Database access
root.outputDir = './Plots'
root.dbAddress ='sqlite:///opsim.sqlite'
root.opsimNames = ['opsim3_61']


binList=[]
nside=128

constraints = ["filter = \'%s\'"%'r']

binner = BinnerConfig()
binner.name = 'HealpixBinner'
binner.kwargs = {"nside":nside}
m1 = makeMetricConfig('CountMetric', params=['expMJD'],plotDict={'percentileClip':80., 'plotLabel':'#'})
m2 = makeMetricConfig('Coaddm5Metric', plotDict={'zp':27., 'percentileClip':True, 'plotLabel':'Co-add m5 - %.1f'%27.} )           
binner.metricDict = makeDict(m1,m2)
binner.setupKwargs={ "leafsize":50000}
binner.setupParams=["fieldRA","fieldDec"]
binner.constraints=constraints
binList.append(binner)


binner= BinnerConfig()
binner.name='OneDBinner'
binner.setupParams=['slewDist']
m1 = makeMetricConfig('CountMetric', params=['slewDist'])
binner.metricDict=makeDict(m1)
binner.constraints=constraints
binList.append(binner)

binner=BinnerConfig()
binner.name='OpsimFieldBinner'
binner.setupParams=["fieldID","fieldRA","fieldDec"]
binner.constraints = constraints
m1 = makeMetricConfig('MinMetric', params=['airmass'])
m4 = makeMetricConfig('MeanMetric', params=['normairmass'])
m3 = makeMetricConfig('Coaddm5Metric')
m7 = makeMetricConfig('CountMetric', params=['expMJD'])
binner.metricDict = makeDict(m1,m3,m4,m7)
binList.append(binner)

binList=[]

binner= BinnerConfig()
binner.name='UniBinner'
m1 = makeMetricConfig('ObservEfficMetric')
binner.metricDict=makeDict(m1)
binner.constraints=['night < 750+49353']
binList.append(binner)



root.binners=makeDict(*binList)
