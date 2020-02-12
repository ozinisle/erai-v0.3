
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
        """
        # Simple Moving Average SMA is calculaed with the following formula
        # Simple moving average= 
        # Simple Moving Average = (N:period sum)/N
        ​#	 	 
        # where:
        # N=number of days in a given period
        # period sum=sum of stock closing prices in that period
        #
        """
        historicalMeansDf = pd.concat([df],axis=1)
        for itr in range(1,201):
            #print (str(itr))
            historicalMeansDf = pd.concat([historicalMeansDf,df[['close']].shift(itr).add_prefix('prev_'+str(itr)+'_')],axis=1)

        historicalMeansDf.fillna(0, inplace=True)
        
        colNames=[[colName,colName.replace('_close','').replace('prev_','')] for colName in historicalMeansDf.columns.values if colName.endswith('_close') ]
        closeAttrib_HistoricalMeansDf = historicalMeansDf[np.array(colNames)[:,0]]

        closeAttrib_mean200_HistoricalMeansDf = np.mean(closeAttrib_HistoricalMeansDf,axis=1)
        closeAttrib_HistoricalMeansDf.columns = np.array(colNames)[:,1]

        # declare time periods (N) 
        # NOTE: Period 200 is added to the end result and HENCE SHOULD NOT BE ADDED TO THE FOLLOWING LIST
        periods = np.array([3,5,8,10,12,13,15,20,26,30,35,40,45,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190])
        
        #closeAttrib_mean200_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:200]],axis=1)
        buffer_sma_df = None
        simpleMovingAverageDf = df[['close']]
        for time_period in periods:
            buffer_sma_df = np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:time_period]],axis=1)

            simpleMovingAverageDf = pd.concat([simpleMovingAverageDf,buffer_sma_df.rename('SMA_'+str(time_period))],axis=1)

        simpleMovingAverageDf = simpleMovingAverageDf.drop(['close'],axis=1)

        # closeAttrib_mean190_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:190]],axis=1)
        # closeAttrib_mean180_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:180]],axis=1)
        # closeAttrib_mean170_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:170]],axis=1)
        # closeAttrib_mean160_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:160]],axis=1)
        # closeAttrib_mean150_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:150]],axis=1)
        # closeAttrib_mean140_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:140]],axis=1)
        # closeAttrib_mean130_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:130]],axis=1)
        # closeAttrib_mean120_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:120]],axis=1)
        # closeAttrib_mean110_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:110]],axis=1)
        # closeAttrib_mean100_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:100]],axis=1)
        # closeAttrib_mean90_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:90]],axis=1)
        # closeAttrib_mean80_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:80]],axis=1)
        # closeAttrib_mean70_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:70]],axis=1)
        # closeAttrib_mean60_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:60]],axis=1)
        # closeAttrib_mean50_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:50]],axis=1)
        # closeAttrib_mean40_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:40]],axis=1)
        # closeAttrib_mean30_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:30]],axis=1)
        # closeAttrib_mean26_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:26]],axis=1)
        # closeAttrib_mean20_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:20]],axis=1)
        # closeAttrib_mean13_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:13]],axis=1)
        # closeAttrib_mean12_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:12]],axis=1)
        # closeAttrib_mean10_HistoricalMeansDf=np.mean(closeAttrib_HistoricalMeansDf[closeAttrib_HistoricalMeansDf.columns[0:10]],axis=1)


        # historicalMeansDf = pd.concat([
        #                             closeAttrib_mean200_HistoricalMeansDf.rename('SMA_200'),
        #                             closeAttrib_mean190_HistoricalMeansDf.rename('SMA_190'),
        #                             closeAttrib_mean180_HistoricalMeansDf.rename('SMA_180'),
        #                             closeAttrib_mean170_HistoricalMeansDf.rename('SMA_170'),
        #                             closeAttrib_mean160_HistoricalMeansDf.rename('SMA_160'),
        #                             closeAttrib_mean150_HistoricalMeansDf.rename('SMA_150'),
        #                             closeAttrib_mean140_HistoricalMeansDf.rename('SMA_140'),
        #                             closeAttrib_mean130_HistoricalMeansDf.rename('SMA_130'),
        #                             closeAttrib_mean120_HistoricalMeansDf.rename('SMA_120'),
        #                             closeAttrib_mean110_HistoricalMeansDf.rename('SMA_110'),
        #                             closeAttrib_mean100_HistoricalMeansDf.rename('SMA_100'),
        #                             closeAttrib_mean90_HistoricalMeansDf.rename('SMA_90'),
        #                             closeAttrib_mean80_HistoricalMeansDf.rename('SMA_80'),
        #                             closeAttrib_mean70_HistoricalMeansDf.rename('SMA_70'),
        #                             closeAttrib_mean60_HistoricalMeansDf.rename('SMA_60'),
        #                             closeAttrib_mean50_HistoricalMeansDf.rename('SMA_50'),
        #                             closeAttrib_mean40_HistoricalMeansDf.rename('SMA_40'),
        #                             closeAttrib_mean30_HistoricalMeansDf.rename('SMA_30'),
        #                             closeAttrib_mean26_HistoricalMeansDf.rename('SMA_26'),
        #                             closeAttrib_mean20_HistoricalMeansDf.rename('SMA_20'),
        #                             closeAttrib_mean13_HistoricalMeansDf.rename('SMA_13'),
        #                             closeAttrib_mean12_HistoricalMeansDf.rename('SMA_12'),
        #                             closeAttrib_mean10_HistoricalMeansDf.rename('SMA_10')
        #                             ],axis=1)

        # simpleMovingAverageDifferenceDf = pd.DataFrame({
        #     'simpleMovingAverageDifference':historicalMeansDf['SMA_60'] - historicalMeansDf['SMA_10'] 
        # })

        # simpleMovingAverageDf = pd.concat([historicalMeansDf],axis=1)

    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

    finally:
        return simpleMovingAverageDf

"""
    @Funtion:  getExponentialMovingAverageFeatures
    @Param: dataDf - Pandas date frame with basic stock related data - open /close/high/low values

    # The formula for calculating the weighting multiplier looks like this:
    # 
    # Weighted multiplier  = 2 / (N+1)
    # where , N = Selected time period say 10, 20 etc over which the SMA or EMA is being calulated
    #
    #  So for a period of 10 day or the past 10 entries, N=10
    #  Weighted multiplier (k) = 2÷(10+1)
    #  => k = 0.1818
    #  => k = 18.18%

    # Exponential Moving Average, EMA is calculated as follows
    # EMA = [ Price(t) × k ] + [ EMA(y) × (1−k)]
    #
    # where:
    # t = today
    # y = yesterday
    # N = number of days in EMA
    # k = 2 ÷ (N+1)
​"""
def getExponentialMovingAverageFeatures(dataDf):
    import os
    import sys
    import traceback

    import pandas as pd
    import numpy as np

    from utils.errorHandler import handleError

    exponentialMovingAverageDf = None
    try:
        import numpy as np
        import pandas as pd

        # declare time periods (N)
        periods = np.array([3,5,8,10,12,13,15,20,26,30,35,40,45,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200])
        
        # calculate weighted multipliers (k = 2/(N+1)), were N is time period
        weightedMultiplier = np.divide(2,np.add(periods,1))

        emaDf = pd.concat([dataDf],axis=1)
        iterIndex = 0
        for time_period in periods:
            # print (str(time_period))
            
            # calculate [ Price(t) × k ] were  k = 2 / (N+1) which is 'WeightedMultiplier' in this case
            ema_col_df = np.multiply( emaDf['close'] , weightedMultiplier[iterIndex] )
            # calculate  EMA = [ Price(t) × k ] + [ EMA(y) × (1−k)]
            ema_col_df= np.add(
                            ema_col_df ,
                            np.multiply( ema_col_df.shift(1) , (1 - weightedMultiplier[iterIndex]) )
                        )
            ema_col_df = ema_col_df.rename('ema_'+str(time_period))
                    
            emaDf = pd.concat([
                                emaDf,
                                ema_col_df
                            ],axis=1)
            
            iterIndex += 1
        
        exponentialMovingAverageDf = emaDf.drop(['open','high','low','close'],axis=1)

    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

    finally:
        return exponentialMovingAverageDf

"""
    The Formula for the Linearly Weighted Moving Average (LWMA) Is:
    ​	  
    LWMA= (P(n)*W(1) + P(n-1)*W(2) + P(n-2)*W(3) + .... ) / (SIGMA (W))
    ​	 
    where:
    P(n) = Price for the period 'n'
    n = The most recent period, n-1 is the prior period,
    and n-2 is two periods prior
    W = The assigned weight to each period, with the
    highest weight going first and then descending linearly
    based on the number of periods being used
    ​example W(5)=5, w(4)=4, ... W(1)=1	
"""
def getLinearWeightedMovingAverageFeatures(dataDf) :
    import sys, traceback
    import numpy as np
    import pandas as pd
        
    from utils.errorHandler import handleError

    linearWeightedMovingAvgDf = None
    try:

        # declare time periods (N)
        periods = np.array([10,12,13,20,26,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200])

        iterIndex = 0
        lwmaDf = pd.concat([dataDf],axis=1)
        for time_period in periods:
            # print (str(time_period))
            price = dataDf['close']

            lwma_priceWeightSum = np.multiply(price,0)
            sigma_W =  np.multiply(price,0)

            for time_period_itr in range(time_period):
                #LWMA= (P(n)*W(1) + P(n-1)*W(2) + P(n-2)*W(3) + .... ) / (SIGMA (W))
                lwma_priceWeightSum = np.add( 
                                        lwma_priceWeightSum, 
                                        np.multiply(
                                            dataDf['close'].shift(time_period_itr),
                                            time_period-time_period_itr
                                        ))
                sigma_W = np.add( sigma_W, time_period - time_period_itr )

            lwma = lwma_priceWeightSum / sigma_W

            lwmaDf = pd.concat([
                                lwmaDf,
                                lwma.rename('lwma_'+str(time_period))
                            ],axis=1)

            iterIndex += 1

        linearWeightedMovingAvgDf = lwmaDf.drop(['open','high','low','close'],axis=1)

    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

    finally:
        return linearWeightedMovingAvgDf
      
"""
    @Funtion:  getGuppyMultipleMovingAverageFeatures
    @Param: dataDf - Pandas date frame with basic stock related data - open /close/high/low values

    EMA = [ Close_price − EMA_previous ] * M + EMA_previous
    SMA = Sum_of_N_closing_prices / N
    M = 2/(N + 1)

    were,
    EMA = exponential moving average
    EMA_Previous = exponential moving average for previous period - SMA can substitute for EMA of first calculation
    N = number of periods
​"""
def getGuppyMultipleMovingAverageFeatures(dataDf,smaDf):
    import os
    import sys
    import traceback

    import pandas as pd
    import numpy as np

    from utils.errorHandler import handleError

    gmmaDf = None
    try:
        # declare time periods (N)
        periods = np.array([3,5,8,10,12,15,20,30,35,40,45,50,60])
        
        # calculate weighted multipliers (k = 2/(N+1)), were N is time period
        weightedMultiplier = np.divide(2,np.add(periods,1))

        import pandas as pd
        import numpy as np
            
        # declare time periods (N)
        periods = np.array([3,5,8,10,12,15,20,30,35,40,45,50,60])

        # calculate weighted multipliers (k = 2/(N+1)), were N is time period
        weightedMultiplier = np.divide(2,np.add(periods,1))

        gmmaDf = pd.concat([dataDf[['close']]],axis=1)
        gmmaDf = gmmaDf.drop(0,axis=0)

        iterIndex = 0
        for time_period in periods:
            gmmaDf['GMMA_'+str(time_period)] = 0

            #1. Calculate the SMA for N
            SMA = smaDf['SMA_'+str(time_period)]
            SMA.drop(0,axis=0)

            #2. Calculate the Multiplier using the same N value.
            M =  weightedMultiplier[iterIndex]

            # 3. Use the most recent closing price, the multiplier, and SMA to calculate the EMA. 
            # The SMA is placed in the EMA Previous Day spot in the calculation. Once the EMA has been calculated, 
            # the SMA is no longer needed since the EMA calculation can be used in the EMA Previous Day spot for the next calculation.
            gmmaDf['GMMA_'+str(time_period)][1] = ( gmmaDf['close'][1] - SMA[1] ) * M + SMA[1]  
            EMA = gmmaDf['GMMA_'+str(time_period)]
            EMA = np.add(np.multiply(np.subtract(gmmaDf['close'],EMA.shift(1)), float(M)) , EMA.shift(1))

            #4. Repeat the process for the next N value, until you have the EMA reading for all 12 moving averages.
            gmmaDf['GMMA_'+str(time_period)] = EMA

            iterIndex += 1

        gmmaDf = gmmaDf.drop(['close'],axis=1)

    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

    finally:
        return gmmaDf
