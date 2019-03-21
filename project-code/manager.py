import cloudmesh.storage.provider.gdrive.Provider
import cloudmesh.storage.provider.box.Provider
import cloudmesh.storage.provider.aws.Provider


class Manager(object):

    def __init__(self):
        print("init {name}".format(name=self.__class__.__name__))

    def _provider(self, service):
        provider = None
        if service == "gdrive":
            provider = cloudmesh.storage.provider.gdrive.Provider.Provider()
        elif service == "box":
            provider = cloudmesh.storage.provider.box.Provider.Provider()
        elif service == "aws":
            provider = cloudmesh.storage.provider.aws.Provider.Provider()
        return provider


    def createDir(self, service, dirName):
        print("createDir", service, dirName)
        provider = self._provider(service)
        provider.createDir(dirName)

    def listDirFiles(self, service, dirName):
        print("listDirFiles", service, dirName)
        provider = self._provider(service)
        provider.listDirFiles(dirName)

    def deleteDir(self, service, dirName):
        print("deleteDir", service, dirName)
        provider = self._provider(service)
        provider.deleteDir(dirName)

    def putFile(self, service, sourceFilename, sourceDir, destFilename, destDir):
        print("putFile", service, sourceFilename, sourceDir, destFilename, destDir)
        provider = self._provider(service)
        provider.putFile(sourceFilename, sourceDir, destFilename, destDir)

    def getFile(self, service, sourceFilename, sourceDir, destFilename, destDir):
        print("getFile", service, sourceFilename, sourceDir, destFilename, destDir)
        provider = self._provider(service)
        provider.getFile(sourceFilename, sourceDir, destFilename, destDir)

    def deleteFile(self, service, fileName, dirName):
        print("deleteFile", service, fileName, dirName)
        provider = self._provider(service)
        provider.deleteFile(fileName, dirName)

    def searchFile(self, service, fileName, dirName):
        print("searchFile", service, fileName, dirName)
        provider = self._provider(service)
        provider.searchFile(fileName, dirName)

    def listFileInfo(self, service, fileName, dirName):
        print("listFileInfo", service, fileName, dirName)
        provider = self._provider(service)
        provider.listFileInfo(fileName, dirName)


