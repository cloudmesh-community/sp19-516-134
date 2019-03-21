import boto3
from cloudmesh.management.configuration.config import Config
import os
from cloudmesh.common.util import path_expand
from cloudmesh.common.util import HEADING
from pprint import pprint

class Provider(object):

    def __init__(self):
        config = Config()
        access_key_id = config['cloudmesh.storage.aws.credentials.access_key_id']
        secret_access_key = config['cloudmesh.storage.aws.credentials.secret_access_key']
        region = config['cloudmesh.storage.aws.credentials.region']
        self.container_name = config['cloudmesh.storage.aws.credentials.container']

        self.s3Resource = boto3.resource('s3',
                                    aws_access_key_id=access_key_id,
                                    aws_secret_access_key=secret_access_key,
                                    region_name=region
                                    )

        self.s3Client = boto3.client('s3',
                                aws_access_key_id=access_key_id,
                                aws_secret_access_key=secret_access_key,
                                region_name=region
                                )


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

    # function to create a directory
    def createDir(self, dirName):
        fileContent = ""
        filePath = self.joinFileNameDir('marker.txt',dirName)

        obj = list(self.s3Resource.Bucket(self.container_name).objects.filter(Prefix=filePath))

        if len(obj) == 0:
            self.s3Resource.Object(self.container_name, filePath).put(Body=fileContent)
            print('Directory created')
        else:
            print('Directory already present')

    def list_files(self):

        data = dict()
        files = {}  # get files from boto
        for file in files:
            dictfile = files[file]
            dictfile['cloud'] = 'aws'
            dictfile['kind'] = 'storage'
            data.append(dictfile)

        return data

    # function to list files in a directory
    def listDirFiles(self, dirName):

        #
        #  each file must have the attibutes
        #  cloud = cloudname ("aws")
        #  kind = "storage"

        objs = list(self.s3Resource.Bucket(self.container_name).objects.all())

        dirFilesList = []
        #if len(objs) > 0:
        for obj in objs:
            if obj.key.startswith(self.trimFileNamePath(dirName)):
                print(obj.key)
                dirFilesList.append(obj.key)

        if len(dirFilesList) == 0:
            print("No files found in directory")
        #else:
        #    print("No files found in directory")

    # function to delete a directory
    def deleteDir(self, dirName):
        objs = list(self.s3Resource.Bucket(self.container_name).objects.all())

        dirFilesList = []
        #if len(objs) > 0:
        for obj in objs:
            if obj.key.startswith(self.trimFileNamePath(dirName)):
                self.s3Resource.Object(self.container_name,obj.key).delete()
                dirFilesList.append(obj.key)

        if len(dirFilesList) == 0:
            print("Directory not found")
        else:
            print('Directory deleted')


    # function to upload a file to cloud from local storage
    def putFile(self, sourceFilename, sourceDir, destFilename, destDir):
        HEADING()
        sourceFilePath = self.joinFileNameDir(sourceFilename,sourceDir)
        targetFilePath = self.joinFileNameDir(destFilename,destDir)

        self.s3Client.upload_file(sourceFilePath, self.container_name, targetFilePath)
        print('File uploaded')

    # function to download a file from a cloud to local storage
    def getFile(self, sourceFilename, sourceDir, destFilename, destDir):
        HEADING()
        sourceFilePath = self.joinFileNameDir(sourceFilename,sourceDir)
        targetFilePath = self.joinFileNameDir(destFilename,destDir)
        blob = self.s3Resource.Bucket(self.container_name).download_file(
            sourceFilePath, targetFilePath)
        print('File downloaded')

    # function to delete a file
    def deleteFile(self, fileName, dirName):
        HEADING()
        filePath = self.joinFileNameDir(fileName, dirName)
        objs = list(self.s3Resource.Bucket(self.container_name).objects.filter(Prefix=filePath))
        if len(objs) > 0:
            self.s3Resource.Object(self.container_name, filePath).delete()
            print('File deleted')
        else:
            print("File does not exist")

    # function to search a file
    def searchFile(self, fileName, dirName):
        HEADING()
        filePath = self.joinFileNameDir(fileName, dirName)

        obj = []
        #print(filePath)

        if(len(dirName) > 0):
            objs = list(self.s3Resource.Bucket(self.container_name).objects.filter(Prefix=filePath))
        else:
            objs = list(self.s3Resource.Bucket(self.container_name).objects.all())

        if len(objs) > 0:
            for obj in objs:
                if self.splitToList(obj.key)[-1] == fileName:
                    print(obj.key)
        else:
            print("File not found")

    # function to list file info
    def listFileInfo(self, fileName, dirName):
        HEADING()
        filePath = self.joinFileNameDir(fileName, dirName)

        obj = []
        #print(filePath)
        infoList = []

        if(len(dirName) > 0):
            objs = list(self.s3Resource.Bucket(self.container_name).objects.filter(Prefix=filePath))
        else:
            objs = list(self.s3Resource.Bucket(self.container_name).objects.all())

        if len(objs) > 0:
            for obj in objs:
                if self.splitToList(obj.key)[-1] == fileName:
                    #print(obj.key)
                    metadata = self.s3Client.head_object(Bucket=self.container_name, Key=obj.key)
                    # print(metadata)
                    info = {
                        "fileName": obj.key,
                        # "creationDate" : metadata['ResponseMetadata']['HTTPHeaders']['date'],
                        "lastModificationDate": metadata['ResponseMetadata']['HTTPHeaders']['last-modified'],
                        "contentLength": metadata['ResponseMetadata']['HTTPHeaders']['content-length']
                    }
                    #pprint(info)
                    infoList.append(info)
        else:
            print("File not found")

        pprint(infoList)
        return infoList
