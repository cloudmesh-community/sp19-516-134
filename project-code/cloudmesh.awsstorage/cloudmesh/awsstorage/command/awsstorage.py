from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.awsawsstorage.api.manager import Manager
from cloudmesh.common.console import  Console
from cloudmesh.common.util import path_expand
from pprint import pprint


class AwsawsstorageCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_awsawsstorage(self, args, arguments):
      """
        ::
        Usage:
            awsstorage [--awsstorage=<SERVICE>] create dir DIRNAME
            awsstorage [--awsstorage=<SERVICE>] delete dir DIRNAME
            awsstorage [--awsstorage=<SERVICE>] list dir files [DIRNAME]
            awsstorage [--awsstorage=<SERVICE>] put file SOURCEFILENAME SOURCEDIR DESTFILENAME DESTDIR
            awsstorage [--awsstorage=<SERVICE>] gett file SOURCEFILENAME SOURCEDIR DESTFILENAME DESTDIR
            awsstorage [--awsstorage=<SERVICE>] delete file FILENAME DIRNAME
            awsstorage [--awsstorage=<SERVICE>] search file FILENAME [DIRNAME]
            awsstorage [--awsstorage=<SERVICE>] list file info FILENAME DIRNAME

        Manage file awsstorage on AWS S3 buckets and perform operations like put, get, delete on the files.

        Arguments:
            DIRNAME Name of the directory where file is to be created or searched or deleted.
            FILENAME Name of the file is to be created or searched or deleted.
            SOURCEFILENAME Name of the source file for put or get actions
            SOURCEDIR Name of the source file directory for put or get actions
            DESTFILENAME Name of the destination file for put or get actions
            DESTDIR Name of the destination file directory for put or get actions

        Options:
          -h --help
          --awsstorage=<SERVICE>  Cloud awsstorage service name like aws or azure or box or google

        Description:
            Commands to manage file awsstorage on cloud

            awsstorage create dir
                Creates directory with the given name.

            awsstorage delete dir
                Deletes directory with the given name.

            awsstorage list dir files
                Lists all files present in the input directory.
                If no dir is specified, it will list all files across directories.

            awsstorage put file
                Uploads file to cloud awsstorage from the local store.

            awsstorage gett file
                Downloads file from cloud awsstorage to the local store.

            awsstorage delete file
                Deletes the input file from specified cloud awsstorage directory.

            awsstorage search file
                Searches and lists the input file from specified cloud awsstorage directory.
                If no dir is specified, it will list all files across directories which match the filename.

            awsstorage list file info
                Lists the file attributes for the input file.

        Example:
            set awsstorage=aws
            awsstorage put FILENAME DESTDIR

            is the same as
            awsstorage  --awsstorage=aws put FILENAME DESTDIR
        """

        pprint(arguments)

        m = Manager()

        service = None

        #filename = arguments.FILENAME[0]
        try:
            service = arguments["--awsstorage"]
        except Exception as e:
            try:
                v = Variables()
                service = v['awsstorage']
            except Exception as e:
                service = None

        if service is None:
            Console.error("awsstorage service not defined")

        if arguments.create == True and arguments.dir == True:
            m.createDir(service, arguments.DIRNAME)
        elif arguments.gett == True and arguments.file == True:
            print('In service get file')
            m.getFile(service, arguments.SOURCEFILENAME, arguments.SOURCEDIR, arguments.DESTFILENAME, arguments.DESTDIR)
        elif arguments.delete == True and arguments.dir == True:
            m.deleteDir(service, arguments.DIRNAME)
        elif arguments.list == True and arguments.dir == True and arguments.files == True:
            if arguments.DIRNAME is not None:
                m.listDirFiles(service, arguments.DIRNAME)
            else:
                m.listDirFiles(service, '')
        elif arguments.put == True and arguments.file == True:
            m.putFile(service, arguments.SOURCEFILENAME, arguments.SOURCEDIR, arguments.DESTFILENAME, arguments.DESTDIR)
        elif arguments.delete and arguments.file == True:
            m.deleteFile(service, arguments.FILENAME, arguments.DIRNAME)
        elif arguments.search == True and arguments.file == True:
            if arguments.DIRNAME is not None:
                m.searchFile(service, arguments.FILENAME, arguments.DIRNAME)
            else:
                m.searchFile(service, arguments.FILENAME, '')
        elif arguments.list == True and arguments.file == True and arguments.info == True:
            m.listFileInfo(service, arguments.FILENAME, arguments.DIRNAME)
        else:
            print("Command not recognized.")

