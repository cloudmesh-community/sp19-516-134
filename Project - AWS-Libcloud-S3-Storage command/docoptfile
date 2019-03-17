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
                  
            This command does some useful things.
            Arguments:
                FILENAME   a file name
                DIRNAME   directory for uploads and downloads
                SOURCEFILENAME source file name to be copied over to destination
                SOURCEDIR  source dir from where file needs to be copied over to destination
                DESTFILENAME destination file name that can be differnt then the source file
                DESTDIR  dest dir to where file needs to be copied over
                                
            Options:
                -f      specify the file
            Example:
              set storage=aws
              storage put file FILENAME
              is the same as 
              storage  --storage=aws put FILENAME
   """
