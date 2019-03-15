from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import yaml
from libcloud.compute.base import NodeImage


awscreds = yaml.load(open('config.yml'))

# Credentials load
ACCESS_ID = awscreds['EC2_ACCESS_ID']
SECRET_KEY = awscreds['EC2_SECRET_KEY']
REGION = awscreds['region']
AMI_ID = awscreds['image']
SIZE_ID = awscreds['size']
SECURITY_GROUP_NAMES = ['default']
NODE_NAME = 'Test_MS_Node1'


EC2Driver = get_driver(Provider.EC2)
conn = EC2Driver(ACCESS_ID, SECRET_KEY, REGION)
image1 = NodeImage(id=AMI_ID, name=None, driver=conn)
sizes = conn.list_sizes()
size1 = [s for s in sizes if s.id == SIZE_ID][0]

#Create Node
node = conn.create_node(name=NODE_NAME, image=image1, size=size1, ex_securitygroup=SECURITY_GROUP_NAMES)

#Start Node
node = [n for n in conn.list_nodes() if n.name == NODE_NAME][0]
conn.ex_start_node(node=node)
print(node)

#Stop Node
conn.ex_stop_node(node=node)


