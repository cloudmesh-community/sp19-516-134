"""
# PROPOSED MAN PAGE
#            storage [--storage=<SERVICE>] create dir DIRECTORY
#            storage [--storage=<SERVICE>] list SOURCE [--recursive]
#            storage [--storage=<SERVICE>] put SOURCE DESTINATION [--recursive]
#            storage [--storage=<SERVICE>] get SOURCE DESTINATION [--recursive]
#            storage [--storage=<SERVICE>] delete SOURCE 
#            storage [--storage=<SERVICE>] search DIRECTORY FILENAME [--recursive]

#
# SOURCE CAN BE IN MOST CASES FILE OR DIRECTORY
# dependent on what you specify a action on a file or dir is executed
# see the command ls, cp, wget, rsync in linus
#

#
#  /a/1.txt
#  /a/b/2.txt
#
#  storage search /a 2.txt --recursive -> /a/b/2.txt 
#  storage search /a 2.txt  -> file not found 
          ::
            """
        ::
        Usage:
            storage [--storage=<SERVICE>] create dir DIRNAME
            storage [--storage=<SERVICE>] delete dir DIRNAME
            storage [--storage=<SERVICE>] list dir files [DIRNAME]
            storage [--storage=<SERVICE>] put file SOURCEFILENAME SOURCEDIR DESTFILENAME DESTDIR
            storage [--storage=<SERVICE>] get file SOURCEFILENAME SOURCEDIR DESTFILENAME DESTDIR
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
            storage get file
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
