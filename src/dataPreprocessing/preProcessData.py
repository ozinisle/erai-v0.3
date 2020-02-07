from utils import *
from dataPreparation import *

traceback_template = '''Traceback (most recent call last):
  File "%(filename)s", line %(lineno)s, in %(name)s
%(type)s: %(message)s\n'''  # Skipping the "actual line" item


def preProcessData(dataName, dataFrequency, outputFileName = "processedRawData.csv"):
    import os
    import sys
    import traceback

    import pandas as pd
    import glob

    from utils.errorHandler import handleError
    from utils.common import getProjectRootFolderPath

    from utils.fileFolderManipulations import getParentFolder
    from utils.fileFolderManipulations import createFolder

    from config.config import getAppConfigData
    from config.config import setAppConfigData

    from fastai.tabular import add_datepart

    from dataPreparation.simpleFeatures import getFollowingHolidaysDaysStamp
    from dataPreparation.simpleFeatures import getPriorHoliDaysStamps

    print(' data pre-processing >> imported dependencies')

    relativeDataFolderPath = 'data/'+dataName+'/raw/' + dataFrequency

    # Variable to hold the original source folder path which is calculated from the input relative path of the source folder (relativeDataFolderPath)
    # using various python commands like os.path.abspath and os.path.join
    projectRootFolderPath = None

    # Variable to hold a dataframe created with the data from input data files in the relativeDataFolderPath provided
    inputRawDataDF = None

    # Variable to hold the original source folder path which is calculated from the input relative path of the source folder (relativeDataFolderPath)
    # using various python commands like os.path.abspath and os.path.join
    dataFolderPath = None

    # Variable to hold query like value of python to query all json file names in the source folder (dataFolderPath).
    # Will be used in the glob function to execute the query
    json_pattern = None

    # Variable to contain the list of all input json file names in the source folder (dataFolderPath)
    file_list = None

    # return values of this method
    # -------------------------------------------------------------------------------
    # Current methods return value initialized to false. Will be maked as true
    # after every single line in the method has been executed with out errors
    returnValue = False
    # complete filepath of the csv file with the processed raw data
    outputFilePath = None
    outputFolderName = None

    # -------------------------------------------------------------------------------
    try:
        # caluclate the deployment directory path of the current juypter node in the operating system
        projectRootFolderPath = getProjectRootFolderPath()

        # TO BE MODIFIED - NOT SURE WHY I USED THIS - WILL HAVE TO CHECK
        pd.set_option('display.max_columns', None)

        # creating pandas dataframe references for further modification
        inputRawDataDF = pd.DataFrame()

        # calculating the complete data folder path of the relative path provided as parameter
        dataFolderPath = projectRootFolderPath + '/'+relativeDataFolderPath

        # creating OS queryable object for python to work with to find json files in the dataFolderPath calcuated in the previous step
        json_pattern = os.path.join(dataFolderPath, '*.json')

        # store all the json file paths in the dataFolderPath for further processing
        file_list = glob.glob(json_pattern)

        # execution assertion/ui progress update info
        print('looping through all the files to create input data')
        # loop through all the files in the folder and create inputRawDataDF pandas datafram
        for file in file_list:
            print("reading input file >>> " + file + " ...")
            data=None
            try:
                # read json data from unformatted json file
                data = pd.read_json(file, lines=True)
                
                if isinstance(data, str):
                    data = data['data'][0]['candles']
                else:
                    data = data.values[0][0]['candles']
            
            except ValueError:
                # read data from formatted / json linted json file
                data = pd.read_json(file)

                data = data['data'][0]
            

            inputRawDataDF = inputRawDataDF.append(data, ignore_index=True)
            print("File read - SUCCESS")

        #assign column names
        inputRawDataDF.columns = ['date-time', 'open',
                                  'high', 'low', 'close', 'quantity', 'dont-know']

        
        buffer = inputRawDataDF['date-time']
        add_datepart(inputRawDataDF, 'date-time')

        inputRawDataDF = pd.concat([buffer, inputRawDataDF], axis=1)

        # remove duplicate data - can happend due to json files having overlapping data
        # index by data time column - helps identify duplicates
        inputRawDataDF=inputRawDataDF.set_index(keys=['date-time'])
        # identify duplicates, keep the latest data and drop the others
        inputRawDataDF=inputRawDataDF.drop_duplicates(keep='last')
        # reset index to its old state
        inputRawDataDF.reset_index(drop=True, inplace=True)        


        # create prior_holidays feature
        priorHolidaysStamps = getPriorHoliDaysStamps(
            inputRawDataDF['date-timeDayofyear'])
        priorHolidaysStamps_df = pd.DataFrame(
            {'prior_holidays': priorHolidaysStamps[:]})

        inputRawDataDF = pd.concat(
            [inputRawDataDF, priorHolidaysStamps_df], axis=1)
        print('added prior_holidays feature in pre-processed data')

        # create following_holidays feature
        followingHolidaysStamps = getFollowingHolidaysDaysStamp(
            inputRawDataDF['date-timeDayofyear'])
        followingHolidaysStamps_df = pd.DataFrame(
            {'following_holidays': followingHolidaysStamps[:]})

        inputRawDataDF = pd.concat(
            [inputRawDataDF, followingHolidaysStamps_df], axis=1)
        print('added following_holidays feature in pre-processed data')

        '''
        w  write mode
        r  read mode
        a  append mode

        w+  create file if it doesn't exist and open it in (over)write mode
            [it overwrites the file if it already exists]
        r+  open an existing file in read+write mode
        a+  create file if it doesn't exist and open it in append mode
        '''

        processFolderName = getParentFolder(
            dataFolderPath, 2) + '/processed/'+dataFrequency
        print('Attempting to create folder if it does not exist >>>' +
              processFolderName)
        createFolder(processFolderName)

        outputFolderName = processFolderName + '/preProcessedData'
        print('Attempting to create folder if it does not exist >>>' + outputFolderName)
        createFolder(outputFolderName)

        outputFilePath = outputFolderName+'/'+outputFileName
        print('Attempting to create/update file >>>' + outputFilePath)

        inputRawDataDF.to_csv(outputFilePath, sep=',', index=False)

        print('created raw easy to use csv data to be used for preparing training data in the location  >>>'+outputFilePath)

        print(' creating/updating config file')
        setAppConfigData(dataName,dataFrequency,'preProcessedDataFilePath',outputFilePath.replace(projectRootFolderPath, ''))

        returnValue = True
    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

def getPreprocessedData(dataName,dataFrequency):
    import pandas as pd
    import numpy as np
    
    from utils.common import getProjectRootFolderPath    
    from config.config  import getAppConfigData
   
    # Variable to hold the original source folder path which is calculated from the input relative path of the source folder (relativeDataFolderPath)
    # using various python commands like os.path.abspath and os.path.join
    projectRootFolderPath = None
    configFilePath = None    

    # holds data from input data file - Truth source, should be usd only for reference and no updates should happen to this variable
    inputRawProcessedDataDF = None    

    #caluclate the deployment directory path of the current juypter node in the operating system
    projectRootFolderPath = getProjectRootFolderPath()
    print("projectRootFolderPath >>> "+projectRootFolderPath)

    autoConfigData = getAppConfigData()

    preProcessedDataFilePath=autoConfigData[dataName][dataFrequency]['preProcessedDataFilePath']

    # read the raw processed data from csv file
    inputRawProcessedDataDF = pd.read_csv(projectRootFolderPath+'/'+preProcessedDataFilePath) 
    
    return inputRawProcessedDataDF