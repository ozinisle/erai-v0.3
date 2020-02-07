from utils import *

traceback_template = '''Traceback (most recent call last):
  File "%(filename)s", line %(lineno)s, in %(name)s
%(type)s: %(message)s\n'''  # Skipping the "actual line" item


def getAppConfigData():
    import json

    from utils.common import getProjectRootFolderPath
    from utils.errorHandler import handleError

    data = None
    try:
        projectRootDirectory = getProjectRootFolderPath()
        configFilePath = projectRootDirectory + "/src/config/config.json"
        print(' retrieving values configured in >>> ' + configFilePath)
        with open(configFilePath) as json_data_file:
            data = json.load(json_data_file)

    except:
        print(' error retrieving values configured in >>> ' + configFilePath)
        print(' creating new configuration file >>> ' + configFilePath)
        data = {}
        f = open(configFilePath, 'a+')  # open file in append mode
        f.write('{}')
        f.close()

    finally:
        return data


def setAppConfigData(dataName, dataFrequency, key, value):

    import json
    import sys
    import traceback

    from utils.common import getProjectRootFolderPath
    from utils.errorHandler import handleError

    returnValue = False
    data_string = ''
    try:

        projectRootDirectory = getProjectRootFolderPath()
        configFilePath = projectRootDirectory + "/src/config/config.json"

        autoConfigData = getAppConfigData()

        if not autoConfigData.get(dataName):
            autoConfigData[dataName] = {}

        if not autoConfigData[dataName].get(dataFrequency):
            autoConfigData[dataName][dataFrequency] = {}

        autoConfigData[dataName][dataFrequency].update({key: value})

        print(' updating config file >>> ' + configFilePath)
        data_string = json.dumps(autoConfigData)
        with open(configFilePath, 'a+') as json_data_file:
            json_data_file.seek(0)
            json_data_file.write('')
            json_data_file.truncate()
            json_data_file.write(data_string)
        print(' successfully updated config file >>> (try block) ' +
              configFilePath + ' with data >>>' + data_string)

        returnValue = True
    except FileNotFoundError:

        print('creating and updating config file')
        f = open(configFilePath, 'a+')  # open file in append mode
        f.write(data_string)
        f.close()
        print(' successfully created config file >>>  (except block)' +
              configFilePath + ' with data >>>' + data_string)
        returnValue = True
    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise
    finally:
        return returnValue
