from cloudmesh.storage.awslibcloud.Provider import \
    Provider as AwsLibcloudStorageProvider
from cloudmesh.storage.awsboto.Provider import Provider as AwsBotoStargeProvider
from cloudmesh.management.configuration.config import Config
from cloudmesh.common.console import Console
from cloudmesh.mongo.DataBaseDecorator import DatabaseUpdate
from cloudmesh.terminal.Terminal import VERBOSE


class Provider(object):

    def __init__(self, name=None,
                 configuration="~/.cloudmesh/.cloudmesh4.yaml"):
        self.kind = Config(configuration)["cloudmesh"]["storage"][name]["cm"][
            "kind"]
        self.name = name

        # Console.msg("FOUND Kind", self.kind)

        if self.kind in ["awsboto"]:
            self.p = wsLibcloudStorageProvider(name=name,
                                               configuration=configuration)
        elif self.kind in ["awslibcloud"]:
            self.p = AwsBotoStargeProvider(name=name,
                                           configuration=configuration)

    def cloudname(self):
        return self.name

    @DatabaseUpdate()
    def keys(self):
        return self.p.keys()

    @DatabaseUpdate()
    def list_files(self):
        return self.p.list_files()

    def add_colection(self, d, *args):
        if d is None:
            return None
        label = '-'.join(args)
        for entry in d:
            entry['collection'] = label
        return d

    @DatabaseUpdate()
    def images(self):
        return self.p.images()

    # name
    # cloud
    # kind
    @DatabaseUpdate()
    def flavors(self):
        return self.p.flavors()

    def start(self, name=None):
        return self.p.start(name=name)

    def stop(self, name=None):
        return self.p.stop(name=name)

    def info(self, name=None):
        return self.p.info(name=name)

    def resume(self, name=None):
        return self.p.resume(name=name)

    def reboot(self, name=None):
        return self.p.reboot(name=name)

    def create(self, name=None, image=None, size=None, timeout=360, **kwargs):
        self.p.create(
            name=name,
            image=image,
            size=size,
            timeout=360,
            **kwargs)

    def rename(self, name=None, destination=None):
        self.p.rename(name=name, destination=name)
