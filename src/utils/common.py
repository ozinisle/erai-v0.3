def getProjectRootFolderPath():

    import os

    projectRootFolderPath = os.path.abspath(os.path.join('.'))

    projectRootFolderPath = projectRootFolderPath.replace('\\', '/')

    _index = projectRootFolderPath.index('/src/')

    return projectRootFolderPath[0:_index].replace("\\", '/')
