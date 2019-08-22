from libcloud.storage.types import ObjectDoesNotExistError
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.util import HEADING
from pprint import pprint
import subprocess

cls = get_driver(Provider.S3)

class Provider(object):

    def __init__(self, name=None, configuration="~/.cloudmesh/cloudmesh.yaml"):
        config = Config()
        credentials = config['cloudmesh.storage.aws.credentials']
        pprint(credentials)
        access_key_id = credentials['access_key_id']
        secret_access_key = credentials['secret_access_key']
        region = credentials['region']
        #cls = get_driver(Provider.S3)
        s3Resource = cls(access_key_id, secret_access_key)
        self.container_name = credentials['container']
        self.s3Resource = s3Resource
        self.container = self.s3Resource.get_container(container_name=self.container_name)

# function trim s3 filename
    def trimFileNamePath(self, fileNamePath):
        trimmedFileNamePath = ''
        if (len(fileNamePath) > 0 and fileNamePath.strip()[0] == '/'):
            trimmedFileNamePath = fileNamePath.strip()[1:].replace('\\', '/')
        else:
            trimmedFileNamePath = fileNamePath.strip().replace('\\', '/')
        return trimmedFileNamePath

# Function to join file name dir to get full file path
    def joinFileNameDir(self, fileName, dirName):
        fullFilePath = ''
        if (len(self.trimFileNamePath(dirName)) > 0):
            fullFilePath = self.trimFileNamePath(dirName) + '/' + self.trimFileNamePath(fileName)
        else:
            fullFilePath = self.trimFileNamePath(fileName)
        return fullFilePath

# Function to split string to list based on delimiter

    def splitToList(self, string):
        delimter = '/'
        return string.split(delimter)

    def createDir(self, dirName):
        fileContent = ""
        filePath = self.joinFileNameDir('marker.txt', dirName)
        pipe = subprocess.Popen(dirName, bufsize=0, shell=True, stdout=subprocess.PIPE)
        return_code = pipe.poll()
        try:
            objs = self.s3Resource.get_object(self.container_name,filePath)
        except ObjectDoesNotExistError:
            while return_code is None:
                # Compress data in our directory and stream it directly to CF
               obj = self.container.upload_object_via_stream(iterator=pipe.stdout,object_name=filePath)
               return_code = pipe.poll()
            print('Directory created')
            pass
        else:
            print('Directory already present')

 #function to delete a directory

    def deleteDir(self, dirName):
        objects = self.s3Resource.list_container_objects(self.container)

        dirFilesList = []
        for objs in objects:
            if objs.name.startswith(self.trimFileNamePath(dirName)):
                self.s3Resource.delete_object(obj=objs)
                dirFilesList.append(objs.name)

        if len(dirFilesList) == 0:
            print("Directory not found")
        else:
            print('Directory deleted')


# function to delete a file
    def deleteFile(self, fileName, dirName):
        HEADING()
        filePath = self.joinFileNameDir(fileName, dirName)
        try:
            objs = self.s3Resource.get_object(self.container_name, filePath)
        except ObjectDoesNotExistError:
            print("File does not exist")
        else:
            delete_file_object = self.s3Resource.get_object(container_name=self.container_name, object_name=filePath)
            self.s3Resource.delete_object(obj=delete_file_object)
            print('File deleted')


 # function to upload a file to cloud from local storage
    def putFile(self, sourceFilename, sourceDir, destFilename, destDir):
        HEADING()
        sourceFilePath = self.joinFileNameDir(sourceFilename,sourceDir)
        targetFilePath = self.joinFileNameDir(destFilename,destDir)

        self.s3Resource.upload_object(sourceFilePath, self.container, targetFilePath, extra=None, verify_hash=True)
        print('File uploaded')

 # function to download a file from a cloud to local storage
    def getFile(self, sourceFilename, sourceDir, destFilename, destDir):
        HEADING()
        sourceFilePath = self.joinFileNameDir(sourceFilename,sourceDir)
        targetFilePath = self.joinFileNameDir(destFilename,destDir)

        file_object = self.s3Resource.get_object(container_name=self.container_name, object_name=sourceFilePath)
        self.s3Resource.download_object(file_object, targetFilePath, overwrite_existing=True, delete_on_failure=True)

        print('File downloaded')

# function to list files in a directory

    def listDirFiles(self, dirName):
        objects = self.s3Resource.list_container_objects(self.container)

        dirFilesList = []
        for objs in objects:
            if objs.name.startswith(self.trimFileNamePath(dirName)):
                #print("File found in directory")
                print(objs.name)
                dirFilesList.append(objs.name)

        if len(dirFilesList) == 0:
            print("No files found in directory")

# function to search a file
    def searchFile(self, fileName, dirName):
            HEADING()
            filePath = self.joinFileNameDir(fileName, dirName)
            dirFilesList = []
            try:
                if (len(dirName)>0):
                   objs = self.s3Resource.get_object(self.container_name, filePath)
                   print(objs.name)
                else:
                   objs = self.s3Resource.list_container_objects(self.container)
                   for obj in objs:
                     if self.splitToList(obj.name)[-1] == fileName:
                        print(obj.name)
                        dirFilesList.append(obj.name)
                   if len(dirFilesList) == 0:
                       print("File does not exist")
            except ObjectDoesNotExistError:
                print("File does not exist")


# function to list file info
    def listFileInfo(self, fileName, dirName):
        HEADING()
        filePath = self.joinFileNameDir(fileName, dirName)

        dirFilesList = []
        infoList = []
        try:
            if (len(dirName) > 0):
                objs = self.s3Resource.get_object(self.container_name, filePath)
                print(objs.name)
                info = {
                    "fileName": objs.name,
                    "hash": objs.hash,
                    "contentLength": objs.size
                }
                infoList.append(info)
            else:
                objs = self.s3Resource.list_container_objects(self.container)
                for obj in objs:
                    if self.splitToList(obj.name)[-1] == fileName:
                        info = {
                            "fileName": obj.name,
                            "hash": obj.hash,
                            "contentLength": obj.size
                        }
                        dirFilesList.append(obj.name)
                        infoList.append(info)
                if len(dirFilesList) == 0:
                    print("File does not exist")
        except ObjectDoesNotExistError:
            print("File does not exist")

        pprint(infoList)
        return infoList