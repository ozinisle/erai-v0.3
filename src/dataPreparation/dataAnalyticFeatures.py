
from utils import *
from dataPreparation import *

traceback_template = '''Traceback (most recent call last):
  File "%(filename)s", line %(lineno)s, in %(name)s
%(type)s: %(message)s\n'''  # Skipping the "actual line" item


def getSimpleMovingAverageFeatures(df):
    import os
    import sys
    import traceback

    import pandas as pd
    import numpy as np

    from utils.errorHandler import handleError

    simpleMovingAverageDf = None

    try:

        historicalMeansDf = pd.concat([df],axis=1)
        for itr in range(1,61):
            #print (str(itr))
            historicalMeansDf = pd.concat([historicalMeansDf,df[['close']].shift(itr).add_prefix('prev_'+str(itr)+'_')],axis=1)

        historicalMeansDf.fillna(0, inplace=True)
        
        colNames=[[colName,colName.replace('_close','').replace('prev_','')] for colName in historicalMeansDf.columns.values if colName.endswith('_close') ]
        closeAttrib_HistoricalMeansDf = historicalMeansDf[np.array(colNames)[:,0]]

        closeAttrib_mean60_HistoricalMeansDf = np.mean(closeAttrib_HistoricalMeansDf,axis=1)
        closeAttrib_HistoricalMeansDf.columns = np.array(colNames)[:,1]

        closeAttrib_mean50_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:50]],axis=1)
        closeAttrib_mean40_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:40]],axis=1)
        closeAttrib_mean30_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:30]],axis=1)
        closeAttrib_mean20_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:20]],axis=1)
        closeAttrib_mean10_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:10]],axis=1)


        historicalMeansDf = pd.concat([
                                    closeAttrib_mean60_HistoricalMeansDf.rename('close_mean60'),
                                    closeAttrib_mean50_HistoricalMeansDf.rename('close_mean50'),
                                    closeAttrib_mean40_HistoricalMeansDf.rename('close_mean40'),
                                    closeAttrib_mean30_HistoricalMeansDf.rename('close_mean30'),
                                    closeAttrib_mean20_HistoricalMeansDf.rename('close_mean20'),
                                    closeAttrib_mean10_HistoricalMeansDf.rename('close_mean10')
                                    ],axis=1)

        simpleMovingAverageDifferenceDf = pd.DataFrame({
            'simpleMovingAverageDifference':historicalMeansDf['close_mean60'] - historicalMeansDf['close_mean10'] 
        })

        simpleMovingAverageDf = pd.concat([historicalMeansDf,simpleMovingAverageDifferenceDf],axis=1)

    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

    finally:
        return simpleMovingAverageDf
