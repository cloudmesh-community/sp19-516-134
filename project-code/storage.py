from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.storage.api.manager import Manager
from cloudmesh.common.variables import Variables
from pprint import pprint
from cloudmesh.common.console import Console


# noinspection PyBroadException
class StorageCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_storage(self, args, arguments):
        """
        ::
        Usage:
            storage [--storage=<SERVICE>] create dir DIRNAME
            storage [--storage=<SERVICE>] delete dir DIRNAME
            storage [--storage=<SERVICE>] list dir files [DIRNAME]
            storage [--storage=<SERVICE>] put file SOURCEFILENAME SOURCEDIR DESTFILENAME DESTDIR
            storage [--storage=<SERVICE>] gett file SOURCEFILENAME SOURCEDIR DESTFILENAME DESTDIR
            storage [--storage=<SERVICE>] delete file FILENAME DIRNAME
            storage [--storage=<SERVICE>] search file FILENAME [DIRNAME]
            storage [--storage=<SERVICE>] list file info FILENAME DIRNAME

        Manage file storage on AWS S3 buckets and perform operations like put, get, delete on the files.

        Arguments:
            DIRNAME Name of the directory where file is to be created or searched or deleted.
            FILENAME Name of the file is to be created or searched or deleted.
            SOURCEFILENAME Name of the source file for put or get actions
            SOURCEDIR Name of the source file directory for put or get actions
            DESTFILENAME Name of the destination file for put or get actions
            DESTDIR Name of the destination file directory for put or get actions

        Options:
          -h --help
          --storage=<SERVICE>  Cloud storage service name like aws or azure or box or google

        Description:
            Commands to manage file storage on cloud

            storage create dir
                Creates directory with the given name.

            storage delete dir
                Deletes directory with the given name.

            storage list dir files
                Lists all files present in the input directory.
                If no dir is specified, it will list all files across directories.

            storage put file
                Uploads file to cloud storage from the local store.

            storage gett file
                Downloads file from cloud storage to the local store.

            storage delete file
                Deletes the input file from specified cloud storage directory.

            storage search file
                Searches and lists the input file from specified cloud storage directory.
                If no dir is specified, it will list all files across directories which match the filename.

            storage list file info
                Lists the file attributes for the input file.

        Example:
            set storage=aws
            storage put FILENAME DESTDIR

            is the same as
            storage  --storage=aws put FILENAME DESTDIR
        """

        pprint(arguments)

        m = Manager()

        service = None

        #filename = arguments.FILENAME[0]
        try:
            service = arguments["--storage"]
        except Exception as e:
            try:
                v = Variables()
                service = v['storage']
            except Exception as e:
                service = None

        if service is None:
            Console.error("storage service not defined")

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
