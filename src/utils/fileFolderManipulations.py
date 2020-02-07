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
