from utils import *
from dataPreparation import *

traceback_template = '''Traceback (most recent call last):
  File "%(filename)s", line %(lineno)s, in %(name)s
%(type)s: %(message)s\n'''  # Skipping the "actual line" item


def createPlatform(dataName, dataFrequency, getNativeDataOnly=False):
    import os
    import sys
    import traceback
    from datetime import datetime, timedelta

    import pandas as pd
    import numpy as np

    from config.config import getAppConfigData
    from config.config import setAppConfigData

    from utils.common import getProjectRootFolderPath
    from utils.errorHandler import handleError

    print("into method doBasicOperation")

    inputRawProcessedDataDF = None

    try:

        # Variable to hold the original source folder path which is calculated from the input relative path of the source folder (relativeDataFolderPath)
        # using various python commands like os.path.abspath and os.path.join
        projectRootFolderPath = getProjectRootFolderPath()

        # holds data from input data file - Truth source, should be usd only for reference and no updates should happen to this variable
        inputRawProcessedDataDF = None

        autoConfigData = getAppConfigData()

        preProcessedDataFilePath = autoConfigData[dataName][dataFrequency]['preProcessedDataFilePath']

        if getNativeDataOnly:
            preProcessedDataFilePath = preProcessedDataFilePath.replace('.csv','') + '_native.csv'

        # read the raw processed data from csv file
        inputRawProcessedDataDF = pd.read_csv(
            projectRootFolderPath + '/'+preProcessedDataFilePath)

        print("before return statement of method doBasicOperation ")

    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise
    finally:
        return inputRawProcessedDataDF

def createFundamentalFeatures(rawDf):
    import traceback
    import sys
    import pandas as pd
    from utils.errorHandler import handleError

    df = None

    try:
        # initialize the straight forward input features
        df = pd.DataFrame({
            'open': rawDf['open'],
            'high': rawDf['high'],
            'low': rawDf['low'],
            'close': rawDf['close']
        })

        print("added INPUT FEATURES >>> 4 count >>> open-high-low-close")

    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise
    finally:
        return df

def createFundamentalPrevCurrDifferentBasedFeatures(rawDf):
    import traceback
    import sys
    import pandas as pd
    from utils.errorHandler import handleError

    df = None

    try:
        # initialize the straight forward input features
        df = pd.DataFrame({
            'dopen': rawDf['open']-rawDf['open'].shift(1),
            'dhigh': rawDf['high']-rawDf['high'].shift(1),
            'dlow': rawDf['low']-rawDf['low'].shift(1),
            'dclose': rawDf['close']-rawDf['close'].shift(1)
        })

        df = df.drop(0, axis=0).reset_index(drop=True)

        print("added INPUT FEATURES >>> 4 count >>> dopen-dhigh-dlow-dclose")

    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise
    finally:
        return df

def prepareDataVariation(featureDf,variation_degree = 20):
    
    import traceback
    import sys
    import pandas as pd    
    import numpy as np

    from tqdm import tqdm
    from utils.errorHandler import handleError
    from utils.pandaTools import suffixColumnsWithLabel

    cummulativeListOfFeatures = None
    
    try:
        # Create and register a new `tqdm` instance with `pandas`
        # (can use tqdm_gui, optional kwargs, etc.)
        tqdm.pandas()

        print ('attempt to prepare data variation of degree >>> variation_degree >>> ' + str(variation_degree))

        featureVariants=[[
                            np.exp(suffixColumnsWithLabel(featureDf,'_exp_'+str(iterator))*iterator), 
                            np.exp(suffixColumnsWithLabel(featureDf,'_exp_inv_'+str(iterator))*iterator*-1),
                            np.power(suffixColumnsWithLabel(featureDf,'_pow_'+str(iterator)),iterator),
                            np.power(suffixColumnsWithLabel(featureDf,'_pow_inv_'+str(iterator)).astype(float),iterator*-1)
        ] for iterator in range(1,variation_degree+1)]
        
        print ('data variation creation complete >>> attempting organizing them into single list of numpy array')
        segmentCount,rowCount, colCount = len(featureVariants),len(featureVariants[0]),len(featureVariants[0][0])

        cummulativeListOfFeatures = np.empty(segmentCount, dtype=list)
        
        print('organizing data varations created into a list of individual feature dataframe')
        for segmentItr in range(0,segmentCount-1):
            cummulativeListOfFeatures[segmentItr]=pd.DataFrame([])
            for rowItr in range(0,rowCount-1): 
                cummulativeListOfFeatures[segmentItr] = pd.concat([cummulativeListOfFeatures[segmentItr],featureVariants[segmentItr][rowItr]],axis=1)
        

        print('orgaining the individual list of feature dataframes into one single dataframe')
        cummulativeListOfFeatures=pd.concat(cummulativeListOfFeatures,axis=1)
        
        print ('data variation creation successful, returning values')
        
        
    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

    finally:
        return cummulativeListOfFeatures

def saveFeatureToDisk(dataName, dataFrequency, df, featureName, saveAsFileExtn='csv', withIndex=False):
    import pandas as pd
    import os
    import sys
    import traceback
    from config.config import getAppConfigData
    from config.config import setAppConfigData
    from utils.common import getProjectRootFolderPath
    from utils.fileFolderManipulations import createFolder
    from utils.errorHandler import handleError

    featureFilePath = None
    try:

        # To Do - When Time Permits - Adds stability and Ease of Maintenance
        #
        # Parameter Validation List
        # -------------------------------------
        # 1. dataName must be String 
        # 2. dataName should be one of available data in data folder
        #
        # 3. dataFrequency must be string
        # 4. dataFrequency must be one of available dataFequency in data folder
        #
        # 5. df must be of type pandas dataframe
        # 6. df must have valid data
        # 
        # 7. featureName must be string
        # 8. if a featureName file already exists should ask for confirmation on overwrite
        #
        # 9. saveAsFileExtn - validation already in place - No new code required
        #
        # 10. withIndex - should be a boolean value

        projectRootFolderPath = getProjectRootFolderPath()

        featureFolderPath = projectRootFolderPath + '/data/' + dataName + '/processed/'+ dataFrequency+ '/features' 
        createFolder(featureFolderPath)

        featureFilePath = featureFolderPath+ '/' + featureName + '.' + saveAsFileExtn

        if isinstance(saveAsFileExtn,str) :
            if saveAsFileExtn.lower() == 'csv':
                df.to_csv(featureFilePath, sep=',', index=withIndex)
            elif saveAsFileExtn.lower() == 'json':
                df.to_json(featureFilePath,index=withIndex)
            else:
                raise ValueError('Invalid saveAsFileExtn - must be csv or json')
        else:
            raise ValueError('Invalid saveAsFileExtn - must be a valid string value')
    
    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise
    finally:
        return featureFilePath

def getFeatureData(dataName, dataFrequency, featureFileName):
    import pandas as pd
    import os
    import sys
    import traceback

    from config.config import getAppConfigData
    from config.config import setAppConfigData
    
    from utils.common import getProjectRootFolderPath
    from utils.fileFolderManipulations import createFolder
    from utils.errorHandler import handleError

    featureDf = None
    try:

        # To Do - When Time Permits - Adds stability and Ease of Maintenance
        #
        # Parameter Validation List
        # -------------------------------------
        # 1. dataName must be String 
        # 2. dataName should be one of available data in data folder
        #
        # 3. dataFrequency must be string
        # 4. dataFrequency must be one of available dataFequency in data folder
        #
        # 5. df must be of type pandas dataframe
        # 6. df must have valid data
        # 
        # 7. featureName must be string
        # 8. if a featureName file already exists should ask for confirmation on overwrite
        #
        # 9. saveAsFileExtn - validation already in place - No new code required
        #
        # 10. withIndex - should be a boolean value

        projectRootFolderPath = getProjectRootFolderPath()

        featureFolderPath = projectRootFolderPath + '/data/' + dataName + '/processed/'+ dataFrequency+ '/features' 
        
        featureFilePath = featureFolderPath+ '/' + featureFileName 

        

        if isinstance(featureFileName,str) :
            if featureFileName.index('.csv') == len(featureFileName)-4:
                featureDf = pd.read_csv(featureFilePath)
            elif featureFileName.index('.json') == len(featureFileName)-4:
                featureDf = pd.read_json(featureFilePath)
            else:
                raise ValueError('Invalid saveAsFileExtn - must be csv or json')
        else:
            raise ValueError('Invalid saveAsFileExtn - must be a valid string value')
    
    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise
    finally:
        return featureDf

                