from utils import *
from visualization import *

traceback_template = '''Traceback (most recent call last):
  File "%(filename)s", line %(lineno)s, in %(name)s
%(type)s: %(message)s\n'''  # Skipping the "actual line" item

def displayMovingAverageChart(movingAverageDf):
    import os
    import sys
    import traceback

    import pandas as pd
    import numpy as np
    import pylab as pl

    from utils.errorHandler import handleError
    from matplotlib import collections  as mc

    isExecutionSuccess = False

    try:
        # build moving average graph
        # we need to build a collection of lines, where each line  with starting point x1,y1 and ending point x2,y2
        # is represented by the set of tuple [(x1,x2),(y1,y2)] in the matplotlib.collection.lineCollection class

        # hence for a given Moving Average (MA) data, the lineCollection should be represented by
        # Array of [(MA.previous.index,MA.current.index),(MA.previous,MA.current)]

        # Modifying the input Moving Average (MA) data accordingly to build a line collection 
        movingAverage_modifiedDf = pd.concat([movingAverageDf],axis=1)
        for column in movingAverageDf.columns:
            movingAverage_modifiedDf[column+'_prev'] = movingAverageDf[column].shift(1)

        #movingAverage_modifiedDf['SMA_3'].index[0]
        firstColumn = movingAverageDf.columns[0]
        ma_chart_df = movingAverageDf[[firstColumn]]
        ma_chart_df['curr_index'] = ma_chart_df.index 
        ma_chart_df = ma_chart_df.drop(firstColumn,axis=1)
        ma_chart_df['prev_index'] = ma_chart_df['curr_index'].shift(1) 

        for column in movingAverage_modifiedDf.columns:
            ma_chart_df[column+'_curr'] = movingAverage_modifiedDf[column]
            ma_chart_df[column+'_prev'] = movingAverage_modifiedDf[column].shift(1)

        # drop the first row as it will have a nan value pointing due to it trying to contain its previous value
        ma_chart_df = ma_chart_df.reset_index()
        ma_chart_df = ma_chart_df.drop(0,axis=0)    

        # since we have droped a few rows with undesirable values, reset the index of the dataframe again 
        # so that the index starts from 0 again sequentially
        ma_chart_df = ma_chart_df.reset_index()

        # construct line collection
        ma_lineCollection = []
        colorMap = []

        green = (0,1,0,1)
        red = (1,0,0,1)

        for itr in range(ma_chart_df.shape[0]):
            for column in movingAverage_modifiedDf.columns:
                y1 = ma_chart_df[column+'_prev'][itr]
                y2 = ma_chart_df[column+'_curr'][itr]

                x1 = ma_chart_df['prev_index'][itr]
                x2 = ma_chart_df['curr_index'][itr]

                # a single line data is represented by [(MA.previous.index,MA.current.index),(MA.previous,MA.current)]
                ma_lineCollection.append([(x1,y1),(x2, y2)])

                diff = y2 - y1
                if diff > 0:
                    # green color
                    colorMap.append(green)
                elif diff < 0:
                    # red color
                    colorMap.append(red)
                else:
                    # previous color
                    if itr == 0:
                        colorMap.append(green)
                    else:
                        colorMap.append(colorMap[itr-1])
        
        # line = [(x1,x2),(y1,y2)]
        # lines = [line1, line2]

        lc = mc.LineCollection(ma_lineCollection, colors=colorMap, linewidths=2)
        fig, ax = pl.subplots()
        ax.add_collection(lc)
        #ax.autoscale()

        y=ma_chart_df.drop(['level_0','index','curr_index','prev_index'],axis=1).to_numpy()
        y=np.nan_to_num(y)


        x=ma_chart_df[['curr_index','prev_index']].to_numpy()
        x=np.nan_to_num(x)

        xmin = 0
        ymin = 0

        ax.set(xlim=(xmin, x.max()), ylim=(ymin, y.max()))

        ax.margins(0.1)

        isExecutionSuccess = True
    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

    finally:
        return isExecutionSuccess


