#################################################################
# nosetest -v --nopature
# nosetests -v --nocapture tests/test_data_s3.py
#################################################################

from pprint import pprint
import time
import subprocess
import sys
from cloudmesh.common.util import HEADING
from cloudmesh.storage.provider.aws.Provider import Provider
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.Printer import Printer
from cloudmesh.common.FlatDict import FlatDict, flatten
from cloudmesh.management.configuration.SSHkey import SSHkey
from cloudmesh.management.configuration.name import Name
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.common.util import banner


class TestName:

    def setup(self):
        banner("setup", c="-")
        self.user = Config()["cloudmesh.profile.user"]

        self.p = Provider(name="aws")

    def test_01_connection(self):
        HEADING()
        print('in test conn')
        #assert self.p.list() == None
        #self.p.createDir('test')
        #self.p.putFile('cloudmeshv4.pptx','c:/Users/shrut/Downloads/','cloudmeshv.pptx','/upload')
        #self.p.getFile('cloudmeshv.pptx','/upload','cloudmeshv_downloaded.pptx','c:/Users/shrut/Downloads/')
        #self.p.deleteFile('cloudmeshv.pptx','/upload')
        #self.p.putFile('cloudmeshv4.pptx','c:/Users/shrut/Downloads/','cloudmeshv.pptx','/upload')
        #self.p.putFile('cloudmeshv4.pptx', 'c:/Users/shrut/Downloads/', 'manjunath.pptx', '/upload')
        #self.p.putFile('cloudmeshv4.pptx', 'c:/Users/shrut/Downloads/', 'shruthi.pptx', '/upload')
        #self.p.searchFile('shruthi.pptx','upload')
        #self.p.searchFile('manjunath.pptx','')
        self.p.listFileInfo('manjunath.pptx','/upload')
        #self.p.listDirFiles('/upload')
        #self.p.listDirFiles('')
        #self.p.deleteDir('/test')
