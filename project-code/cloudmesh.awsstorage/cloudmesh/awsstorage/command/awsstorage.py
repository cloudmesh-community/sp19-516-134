from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.awsstorage.api.manager import Manager
from cloudmesh.common.console import  Console
from cloudmesh.common.util import path_expand
from pprint import pprint


class AwsstorageCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_awsstorage(self, args, arguments):
        """
        ::
          Usage:
                awsstorage [--awsstorage=SERVICE] create dir DIRECTORY
                awsstorage [--awsstorage=SERVICE] gett SOURCE DESTINATION [--recursive]
                awsstorage [--awsstorage=SERVICE] put SOURCE DESTINATION [--recursive]
                awsstorage [--awsstorage=SERVICE] list SOURCE [--recursive]
                awsstorage [--awsstorage=SERVICE] delete SOURCE
                awsstorage [--awsstorage=SERVICE] search DIRECTORY FILENAME [--recursive]

          This command does some useful things.

          Arguments:
              SOURCE        SOURCE can be a directory or file
              DESTINATION   DESTINATION can be a directory or file
              DIRECTORY     DIRECTORY refers to a folder on the cloud service

          Options:
              --awsstorage=SERVICE  specify the cloud service name like aws or azure or box or google

          Description:
                commands used to upload, download, list files on different cloud storage services.

                awsstorage put [options..]
                    Uploads the file specified in the filename to specified cloud from the SOURCEDIR.

                awsstorage gett [options..]
                    Downloads the file specified in the filename from the specified cloud to the DESTDIR.

                awsstorage delete [options..]
                    Deletes the file specified in the filename from the specified cloud.

                awsstorage list [options..]
                    lists all the files from the container name specified on the specified cloud.

                awsstorage create dir [options..]
                    creates a folder with the directory name specified on the specified cloud.

                awsstorage search [options..]
                    searches for the source in all the folders on the specified cloud.

          Example:
            set awsstorage=aws
            awsstorage put SOURCE DESTINATION --recursive
            is the same as
            awsstorage --awsstorage=aws put SOURCE DESTINATION --recursive
        """

        pprint(arguments)
        m = Manager()

        service = None

        try:
            arguments.storage = arguments["--awsstorage"]
            arguments.recursive = arguments["--recursive"]
        except Exception as e:
            try:
                v = Variables()
                service = v['awsstorage']
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