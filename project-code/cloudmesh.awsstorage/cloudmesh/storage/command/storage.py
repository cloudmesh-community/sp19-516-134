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
                storage [--storage=SERVICE] create dir DIRECTORY
                storage [--storage=SERVICE] gett SOURCE DESTINATION [--recursive]
                storage [--storage=SERVICE] put SOURCE DESTINATION [--recursive]
                storage [--storage=SERVICE] list SOURCE [--recursive]
                storage [--storage=SERVICE] delete SOURCE
                storage [--storage=SERVICE] search DIRECTORY FILENAME [--recursive]

          This command does some useful things.

          Arguments:
              SOURCE        SOURCE can be a directory or file
              DESTINATION   DESTINATION can be a directory or file
              DIRECTORY     DIRECTORY refers to a folder on the cloud service

          Options:
              --storage=SERVICE  specify the cloud service name like aws or azure or box or google

          Description:
                commands used to upload, download, list files on different cloud storage services.

                storage put [options..]
                    Uploads the file specified in the filename to specified cloud from the SOURCEDIR.

                storage gett [options..]
                    Downloads the file specified in the filename from the specified cloud to the DESTDIR.

                storage delete [options..]
                    Deletes the file specified in the filename from the specified cloud.

                storage list [options..]
                    lists all the files from the container name specified on the specified cloud.

                storage create dir [options..]
                    creates a folder with the directory name specified on the specified cloud.

                storage search [options..]
                    searches for the source in all the folders on the specified cloud.

          Example:
            set storage=aws
            storage put SOURCE DESTINATION --recursive
            is the same as
            storage --storage=aws put SOURCE DESTINATION --recursive
        """

        pprint(arguments)
        m = Manager()

        service = None

        try:
            arguments.storage = arguments["--storage"]
            arguments.recursive = arguments["--recursive"]
        except Exception as e:
            try:
                v = Variables()
                service = v['storage']
            except Exception as e:
                service = None

        if arguments.storage is None:
            Console.error("storage service not defined")

        if arguments.gett:
            m.get(arguments.storage, arguments.SOURCE, arguments.DESTINATION,
                  arguments.recursive)
        elif arguments.put:
            m.put(arguments.storage, arguments.SOURCE, arguments.DESTINATION,
                  arguments.recursive)
        elif arguments.list:
            print('in list')
            m.list(arguments.storage, arguments.SOURCE, arguments.recursive)
        elif arguments.create and arguments.dir:
            m.createdir(arguments.storage, arguments.DIRECTORY)
        elif arguments.delete:
            m.delete(arguments.storage, arguments.SOURCE)
        elif arguments.search:
            m.search(arguments.storage, arguments.DIRECTORY, arguments.FILENAME,
                     arguments.recursive)
        else:
            print("Command not recognized.")
