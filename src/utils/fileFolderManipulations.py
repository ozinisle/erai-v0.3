import os
import errno
import traceback
import sys

from utils import *
from pathlib import Path

traceback_template = '''Traceback (most recent call last):
  File "%(filename)s", line %(lineno)s, in %(name)s
%(type)s: %(message)s\n'''  # Skipping the "actual line" item


def getParentFolder(folderPath, parentLevel=1):
    from utils.common import getProjectRootFolderPath
    from utils.errorHandler import handleError

    osParentFolderPath = None

    try:
        # caluclate the deployment directory path of the current juypter node in the operating system
        projectRootFolderPath = getProjectRootFolderPath()

        rootFolderPathIndex = -1
        try:
            rootFolderPathIndex = folderPath.index(projectRootFolderPath)
        except ValueError:
            pass

        if rootFolderPathIndex != 0:
            folderPath = projectRootFolderPath+'/'+folderPath

        osFolderPath = Path(folderPath)

        for parentItr in range(parentLevel):
            osFolderPath = osFolderPath.parent

        # type(osFolderPath) = 'pathlib.WindowsPath'
        # hence we need to convert it into a string before returning it
        osParentFolderPath = str(osFolderPath).replace('\\', '/')

    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

    finally:
        return osParentFolderPath


def createFolder(folderPath):
    import os
    from utils.common import getProjectRootFolderPath
    from utils.errorHandler import handleError

    success = False
    createNewFolderFlag = False
    try:
        # caluclate the deployment directory path of the current juypter node in the operating system
        projectRootFolderPath = getProjectRootFolderPath()

        rootFolderPathIndex = -1
        try:
            rootFolderPathIndex = folderPath.index(projectRootFolderPath)
        except ValueError:
            pass

        if rootFolderPathIndex != 0:
            folderPath = projectRootFolderPath+'/'+folderPath

        print(" checking if folder existis >>>" + folderPath)
        if not os.path.exists(folderPath):
            os.makedirs(folderPath, exist_ok=True)
            createNewFolderFlag = True
            print(folderPath + " >>> Folder created")
        success = True
    except FileExistsError:
        # directory already exists
        print(folderPath + " >>> Folder already exists")
        success = True
        pass

    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

    finally:
        return [success, createNewFolderFlag]


def deleteFile(filePath):
    import os
    from utils.common import getProjectRootFolderPath
    from utils.errorHandler import handleError

    success = False
    try:

        # caluclate the deployment directory path of the current juypter node in the operating system
        projectRootFolderPath = getProjectRootFolderPath()

        rootFolderPathIndex = -1
        try:
            rootFolderPathIndex = filePath.index(projectRootFolderPath)
        except ValueError:
            pass

        if rootFolderPathIndex != 0:
            filePath = projectRootFolderPath+'/'+filePath

        os.remove(filePath)
        print("File deleted >>> "+filePath)
        success = True
    except FileNotFoundError:
        print('cannot delete file as the file does not exist >>'+filePath)
    except:
        raise

    finally:
        return success

def archiveFileInRawDataFolder(dataName,dataFrequency,filePathList):
    import os,sys
    from utils.common import getProjectRootFolderPath
    from utils.errorHandler import handleError
    from shutil import copyfile
    import time

    success = False
    
    # Variable to hold the original source folder path which is calculated from the input relative path of the source folder (relativeDataFolderPath)
    # using various python commands like os.path.abspath and os.path.join

    projectRootFolderPath = None

    
    try:
        print ( ' debug >>> archiveFileInRawDataFolder >>> into method')
        # caluclate the deployment directory path of the current juypter node in the operating system
        projectRootFolderPath = getProjectRootFolderPath()

        relativeDataFolderPath = 'data/'+dataName+'/raw/' + dataFrequency

        archiveRootFolderPath = projectRootFolderPath +'/'+ relativeDataFolderPath + '/archive'

        # create the archive root folder if it does not exist
        createFolder(archiveRootFolderPath)

        # create sub archive folder with current time stamp _ avoid overwritting of archive file and hence averting loss of archived data
        archiveFolderPath = archiveRootFolderPath + '/archive_' + str(time.time())

        # create the archive root folder if 
        createFolder(archiveFolderPath)
        print ( ' debug >>> archiveFileInRawDataFolder >>> about to loop through filelist')
        for filePath in filePathList:
            filePathArr = filePath.split('/')
            fileName = filePathArr[len(filePathArr)-1] 

            print ( ' debug >>> archiveFileInRawDataFolder >>> attempting to copy file >>> '+ filePath + '\nto location >>> '+archiveFolderPath + '/' + fileName)
            copyfile(filePath, archiveFolderPath + '/' + fileName)
            deleteFile(filePath)

        success = True
        print ( ' debug >>> archiveFileInRawDataFolder >>> completed method')
    except:
        print ( ' debug >>> archiveFileInRawDataFolder >>> error in method')
        handleError(sys.exc_info(), traceback, traceback_template)
        raise

    finally:
        print ( ' debug >>> archiveFileInRawDataFolder >>> returning value >>> ' + str(success))
        return success

def isFileExists(filePath):
    import os,sys
    from utils.common import getProjectRootFolderPath
    from utils.errorHandler import handleError
    from os.path import exists

    success = False
    
    try:
        print ('Debug >>> start >>> isFileExists method')
        
        # caluclate the deployment directory path of the current juypter node in the operating system
        projectRootFolderPath = getProjectRootFolderPath()
        print ('Debug >>> isFileExists >>> projectRootFolderPath = '+ projectRootFolderPath)
        rootFolderPathIndex = -1
        try:
            rootFolderPathIndex = filePath.index(projectRootFolderPath)
        except ValueError:
            print ('Debug >>> isFileExists >>> valueError')
            pass
        
        print('DEBUG >>> isFileExists >>> rootFolderPathIndex = '+ str(rootFolderPathIndex))
        if rootFolderPathIndex != 0:
            filePath = projectRootFolderPath+'/'+filePath

        print ('Debug >>> check if file path exists >>> ' + filePath)
        success = exists(filePath)
        
    except:
        handleError(sys.exc_info(), traceback, traceback_template)
        raise
        
    finally:
        print ('Debug >>> end >>> isFileExists method')
        
        return success


